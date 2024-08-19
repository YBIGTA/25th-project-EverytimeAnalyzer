import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing import *
from text_processing import normalize_text
from embedding import load_model, generate_embedding

# TODO: flag_sentences 전처리 및 embedding vector 생성

def process_flag_sentences(input_file: str, output_file: str) -> pd.DataFrame:
    """
    flag 문장들이 있는 txt 파일 읽어와서 전처리 후 embedding vector 생성
    Args:
        - input_file: flag 문장들이 있는 txt 파일 경로
        - output_file: 출력 csv 파일 경로
    """
    data = []
    
    # 텍스트 파일을 읽어서 처리
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # 각 줄에서 첫 번째 쉼표만 기준으로 분리 (이후 쉼표는 문장부호로 사용된 쉼표)
            topic, sentence = line.split(',', 1)
            data.append([topic.strip(), sentence.strip()])

    # DataFrame으로 변환
    df = pd.DataFrame(data, columns=["topic", "sentence"])

    # 문장 정규화
    df['normalized_sentence'] = df['sentence'].apply(normalize_text)
    
    # 문장별 임베딩 생성
    model = load_model()
    df['embedding'] = df['normalized_sentence'].apply(
        lambda sentence: generate_embedding(model, sentence)
    )
    
    df.to_csv(output_file, index=False)
    
    return df


# TODO: 강의평 각 문장들과 flag_sentences의 5개 토픽 * 5개 문장 = 25개 문장 간의 manhattan distance 계산 -> 18000 * 25개의 distance matrix 생성
def manhattan_distance(v1: float, v2: float) -> float:
    """
    v1과 v2 사이의 맨하탄 거리 계산
    """
    return sum(abs(v1 - v2))

def calculate_distance_matrix(review_sentences: pd.DataFrame, flag_sentences: pd.DataFrame) -> pd.DataFrame:
    """
    강의평의 각 문장들과 flag 문장들 간의 manhattan distance 계산
    Args:
        - review_sentences: 강의평 문장 DataFrame
        - flag_sentences: flag 문장 DataFrame
    """
    distance_matrix = []
    for i in range(len(review_sentences)):
        distances = []
        for j in range(len(flag_sentences)):
            distances.append(manhattan_distance(review_sentences['embedding'][i], flag_sentences['embedding'][j]))
        distance_matrix.append(distances)
    return pd.DataFrame(distance_matrix, index=review_sentences.sentence, columns=flag_sentences.sentence)


# TODO: 각 문장들과 토픽별 5개 문장 간의 유사도 중 최소값을 각 문장의 토픽 유사도로 사용 -> 18000 * 5개의 similarity matrix 생성
def select_min_distance(df: pd.DataFrame) -> pd.DataFrame:
    """
    강의평의 각 문장들과 topic별 flag 문장들간의 manhattan distance 중 최솟값을 토픽 유사도로 사용
    """
    if df.shape[1] != 25:
        raise ValueError("원본 DataFrame의 컬럼 개수는 25개여야 합니다.")
    
    min_distance = []
    
    for i in range(0, df.shape[1], 5):
        group_min = df.iloc[:, i:i+5].min(axis=1)
        min_distance.append(group_min)
    
    return pd.DataFrame(min_distance).transpose()

# TODO: 토픽별로 유사도 상위 250개 문장 추출 후 중복 제거 -> max 1250개 문장과 해당 문장의 소속 토픽 유사도 저장