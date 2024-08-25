import csv
import json
import os.path

import pandas as pd
import pyLDAvis.gensim_models
from gensim import corpora
from gensim.models import LdaMulticore
from kiwipiepy import Kiwi
from kss import Kss
from tqdm import tqdm


# import file
def importData() -> list[str]:
    with open('./data/sample.json', 'r', encoding='utf-8') as f:
        js = json.loads(f.read())
    df = pd.DataFrame(js)
    df_sim = pd.DataFrame({
        'lectureCode': df['lectureCode'],
        'year': df['lectureReview'].apply(lambda x: x['year']),
        'semester': df['lectureReview'].apply(lambda x: x['semester']),
        'content': df['lectureReview'].apply(lambda x: x['content']),
        'rate': df['lectureReview'].apply(lambda x: x['rate'])
    })
    return df_sim['content'].tolist()


def split_s(reviews: list[str]) -> list[str]:
    result = []
    split = Kss("split_sentences")
    for review in tqdm(reviews, desc="split_sentences"):
        tmp = split(review)
        result.extend(tmp)
    return result


def reduce_repeats(reviews: list[str]) -> list[str]:
    result = []
    reduced = Kss('reduce_char_repeats')
    for review in tqdm(reviews, desc="reduce_repeats"):
        tmp = reduced(review)
        result.append(tmp)
    return result


def extract_nouns(reviews: list[str]) -> list[list[str]]:
    result: list[list[str]] = []
    kiwi = Kiwi()
    for review in tqdm(reviews, desc="extract_noun"):
        tokens = kiwi.tokenize(review)
        nouns = [token[0] for token in tokens if token[1] in ['NNG', 'NNP', 'NP', 'NR']]
        # nouns = [token[0] for token in tokens]
        result.append(nouns)

    return result


def save_refined_data(refined_data: list[list[str]], save_path: str):
    with open(save_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for sentence in refined_data:
            writer.writerow(sentence)


def load_refined_data(save_path: str) -> list[list[str]]:
    with open(save_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)


if __name__ == '__main__':
    refined_data_cache_path: str = './cache/refined-data.csv'

    refined_data = []
    if not os.path.isfile(refined_data_cache_path):
        # 전처리
        data: list[str] = importData()
        data = split_s(data)
        data = reduce_repeats(data)
        refined_data:list[list[str]] = extract_nouns(data)
        # 전처리된 자료 csv로 저장
        print(f"save refined_data csv in {refined_data_cache_path}")
        save_refined_data(refined_data, refined_data_cache_path)
    else:
        # 전처리된 자료 불러오기
        print(f"found refined_data csv in {refined_data_cache_path}")
        refined_data = load_refined_data(refined_data_cache_path)

    dictionary = corpora.Dictionary(refined_data)
    dictionary.filter_extremes(no_below=10, no_above=0.9)  ## no_below는 정수, no_above는 비율

    corpus = [dictionary.doc2bow(text) for text in refined_data]
    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=5, chunksize=1000, passes=7, alpha=0.1, eta=0.01)

    # 시각화 저장
    visualize_save_path: str = './results/result.html'
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, visualize_save_path)
