import yaml

import evaluate
import numpy as np
from box import Box


def load_config(config_file):
    with open(config_file, 'r') as f:
        config = Box(yaml.safe_load(f))
    return config


def compute_metrics(eval_pred):
    f1 = evaluate.load('f1')
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return f1.compute(predictions=predictions, references=labels, average='macro')
