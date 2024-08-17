"""
LDA의 최적 topic paramer 구하기 위한 시각화 코드
실행하면 한 2~3분뒤에 브라우저에 topic개수에 따른 coherence 그래프창이 띄워집니다
"""
import os.path

import plotly.graph_objects as go
import pyLDAvis.gensim_models
from gensim import corpora
from gensim.models import LdaMulticore
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from main import *


def compute_cv(dictionary, corpus, texts, limit, start=2, step=1):
    coherence_values = []
    model_list = []
    for num_topics in tqdm(range(start, limit, step), "calculate coherence"):
        model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


if __name__ == '__main__':
    # 전처리
    refined_data_cache_path: str = './cache/refined-data.csv'
    refined_data = []
    if not os.path.isfile(refined_data_cache_path):
        data: list[str] = importData()
        data = split_s(data)
        data = reduce_repeats(data)
        refined_data: list[list[str]] = extract_nouns(data)
        print(f"save refined_data csv in {refined_data_cache_path}")
        save_refined_data(refined_data, refined_data_cache_path)
    else:
        print(f"found refined_data csv in {refined_data_cache_path}")
        refined_data = load_refined_data(refined_data_cache_path)

    dictionary = corpora.Dictionary(refined_data)
    dictionary.filter_extremes(no_below=10, no_above=0.9)  ## no_below는 정수, no_above는 비율

    corpus = [dictionary.doc2bow(text) for text in refined_data]
    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    # coherence 탐색할 토픽 개수 범위 설정
    limit = 10
    start = 3
    step = 1

    # 각 토픽개수에 따른 LDA모델, 기여도값 리스트로 가져오기
    model_list, coherence_values = compute_cv(dictionary=dictionary, corpus=corpus, texts=refined_data, start=start,
                                              limit=limit, step=step)

    # 시각화
    x = list(range(start, limit, step))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=coherence_values, mode='lines', name='coherence_values'))
    fig.update_layout(xaxis_title='Number of Topics', yaxis_title='Coherence value', showlegend=True)
    fig.show()
