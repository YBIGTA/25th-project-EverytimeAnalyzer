import argparse
import os
import random
from datetime import datetime

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from transformers import (
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

from dataset import BERTDataset
from tokenization_kobert import KoBertTokenizer
from util import compute_metrics, load_config


def main():
    # Load config
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', type=str, default='config.yaml', nargs='?', help='The path to the config file')
    args = parser.parse_args()
    config = load_config(args.config_file)

    # Set Hyperparameters
    SEED = 1234
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)

    DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(DEVICE)

    current_file_path = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(current_file_path)
    DATA_DIR = os.path.join(BASE_DIR, 'src/data')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'src/output')
    PREDICTION_DIR = os.path.join(BASE_DIR, 'src/prediction')

    # Load tokenizer and model
    model_name = 'monologg/kobert'
    tokenizer = KoBertTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=6).to(DEVICE)

    # Load data
    data = pd.read_csv(os.path.join(DATA_DIR, 'dataset.csv'))
    dataset_train, dataset_valid = train_test_split(data, test_size=0.2, random_state=SEED)

    dataset_train = dataset_train.rename(columns={'review': 'text', 'y': 'target'})
    dataset_valid = dataset_valid.rename(columns={'review': 'text', 'y': 'target'})

    # Define dataset
    data_train = BERTDataset(dataset_train, tokenizer, config.dataset.max_seq_len)
    data_valid = BERTDataset(dataset_valid, tokenizer, config.dataset.max_seq_len)

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Train model
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=True,
        do_train=True,
        do_eval=True,
        do_predict=True,
        logging_strategy='steps',
        evaluation_strategy='steps',
        save_strategy='steps',
        logging_steps=100,
        eval_steps=100,
        save_steps=100,
        save_total_limit=2,
        learning_rate=2e-05,
        adam_beta1=0.9,
        adam_beta2=0.999,
        adam_epsilon=1e-08,
        weight_decay=0.01,
        lr_scheduler_type='linear',
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        num_train_epochs=3,
        load_best_model_at_end=True,
        metric_for_best_model='eval_f1',
        greater_is_better=True,
        seed=SEED,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=data_train,
        eval_dataset=data_valid,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    # Evaluate model
    dataset_test = pd.read_csv(os.path.join(DATA_DIR, 'reviews.csv'))
    dataset_test = dataset_test.rename(columns={'content_normalized': 'text'})

    model.eval()
    preds = []
    for _, sample in tqdm(dataset_test.iterrows(), total=len(dataset_test)):
        text = sample['text']
        if not isinstance(text, str):
            text = str(text)
        inputs = tokenizer(text, return_tensors='pt').to(DEVICE)
        with torch.no_grad():
            logits = model(**inputs).logits
            pred = torch.argmax(torch.nn.Softmax(dim=1)(logits), dim=1).cpu().numpy()
            preds.extend(pred)

    # Prediction
    PREDICTION_FILEPATH = os.path.join(PREDICTION_DIR, config.output_filename.prediction)
    os.makedirs(os.path.dirname(PREDICTION_FILEPATH), exist_ok=True)
    dataset_test['target'] = preds
    dataset_test.to_csv(PREDICTION_FILEPATH, index=False)

    # Validation set post-analysis
    dev_preds = []
    for _, sample in tqdm(dataset_valid.iterrows(), total=len(dataset_valid)):
        text = sample['text']
        if not isinstance(text, str):
            text = str(text)
        inputs = tokenizer(text, return_tensors='pt').to(DEVICE)
        with torch.no_grad():
            logits = model(**inputs).logits
            pred = torch.argmax(torch.nn.Softmax(dim=1)(logits), dim=1).cpu().numpy()
            dev_preds.extend(pred)

    VALID_PREDICTION_FILEPATH = os.path.join(PREDICTION_DIR, config.output_filename.validation_prediction)
    dataset_valid['pred'] = dev_preds
    dataset_valid = dataset_valid[['text', 'target', 'pred']]
    dataset_valid.to_csv(VALID_PREDICTION_FILEPATH, index=False)


if __name__ == '__main__':
    main()