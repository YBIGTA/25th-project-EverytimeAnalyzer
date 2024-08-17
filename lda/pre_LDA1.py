"""
doesn't work
"""
import logging
import re

import plotly.graph_objects as go
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
import pyLDAvis.gensim_models
from kiwipiepy import Kiwi
import gensim
from kss import Kss
from tqdm import tqdm

kiwi = Kiwi()

# 데이터 로드
import json
import pandas as pd

with open('data/sample.json', 'r', encoding='utf-8') as f:
    js = json.loads(f.read())

# DataFrame으로 변환

df = pd.DataFrame(js)
df_sim = pd.DataFrame({
    'lectureCode': df['lectureCode'],
    'year': df['lectureReview'].apply(lambda x: x['year']),
    'semester': df['lectureReview'].apply(lambda x: x['semester']),
    'content': df['lectureReview'].apply(lambda x: x['content']),
    'rate': df['lectureReview'].apply(lambda x: x['rate'])
})

# local에 csv로 저장
# df_sim.to_csv('./18406.csv', sep=',', na_rep='', header=True, encoding = 'utf-8-sig')


# 강의평 전체를 하나의 리스트로 저장
df_simlist = df_sim['content'].tolist()


# 문장 분리 (kss 이용)
def split_s(reviews: list[str]) -> list[str]:
    result = []
    split = Kss("split_sentences")
    for review in reviews:
        tmp = split(review)
        result.extend(tmp)
    return result


split = split_s(df_simlist)


# 반복 문자 제거
def reduce_repeats(reviews: list[str]) -> list[str]:
    result = []
    reduced = Kss('reduce_char_repeats')
    for review in tqdm(reviews):
        tmp = reduced(review)
        result.append(tmp)
    return result


split_rr = reduce_repeats(split)


# 유의어 통일
def replace(reviews: list[str]) -> list[str]:
    result = []
    pattern = r'(개꿀강|꿀강)|(a\+|에쁠|에이쁠|에이플)|(\&)'

    def replacement(match):
        if match.group(1):
            return '꿀 강의'
        elif match.group(2):
            return 'A+'
        elif match.group(3):
            return '과 '

    for review in reviews:
        modified = re.sub(pattern, replacement, review)
        result.append(modified)

    return result


split_rr_r = replace(split_rr)


# 토큰화1, 어근 추출 한 번에
## Okt 사용

# def tokenize_stem(reviews: list[str]) -> list[list[str]]:
#    result = []
#    okt = Okt()
#    for review in reviews:
#        tmp = okt.morphs(review, stem = True)
#        result.append(tmp)
#    return result

# split_rr_r_ts = tokenize_stem(split_rr_r)


# 불용어 제거

def filter_stopword(tokensList: list[list[str]], stopwords: list[str]) -> list[list[str]]:
    result: list[list[str]] = []
    for tokens in tokensList:
        sentence: list[str] = list(filter(lambda s: s not in stopwords, tokens))
        result.append(sentence)
    return result


# stopwords = pd.read_csv('./stopword_list.csv', encoding = 'cp949')['stopword'].tolist()
# final = filter_stopword(split_rr_r_ts, stopwords)


# 최종본 csv로 저장 
# final_df = pd.DataFrame(final)
# final_df[:50]
# final_df.to_csv('./preprocessed.csv', index = False, header = False, encoding = 'utf-8')


## LDA

# 명사 추출

def extract_nouns(reviews: list[str]) -> list[list[str]]:
    result: list[list[str]] = []
    for review in reviews:
        tokens = kiwi.tokenize(review)
        nouns = [token[0] for token in tokens if token[1] in ['NNG', 'NNP', 'NP', 'NR']]
        # nouns = [token[0] for token in tokens]
        result.append(nouns)

    return result


final = extract_nouns(split_rr_r)


# coherence value로 최적의 토픽 수 찾기

def compute_cv(dictionary, corpus, texts, limit, start=2, step=1):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


def find_optimal_number_of_topics(dictionary, corpus, processed_data):
    limit = 15;
    start = 4;
    step = 1;

    model_list, coherence_values = compute_cv(dictionary=dictionary, corpus=corpus, texts=processed_data, start=start,
                                              limit=limit, step=step)

    x = list(range(start, limit, step))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=coherence_values, mode='lines', name='coherence_values'))
    fig.update_layout(xaxis_title='Number of Topics', yaxis_title='Coherence value', showlegend=True)
    fig.show()


if __name__ == '__main__':
    dictionary = corpora.Dictionary(final)

    # 출현 빈도가 적거나 자주 등장하는 단어는 제거
    dictionary.filter_extremes(no_below=10, no_above=0.9)  ## no_below는 정수, no_above는 비율
    corpus = [dictionary.doc2bow(text) for text in final]
    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    # 최적의 토픽 수 찾기
    # find_optimal_number_of_topics(dictionary, corpus, final)

    # LDA 시각화
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=8, chunksize=1000, passes=5,
                                           alpha=0.1, eta=0.01)
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, './reviews_lda.html')
    # pyLDAvis.enable_notebook()
    # pyLDAvis.display(vis)
