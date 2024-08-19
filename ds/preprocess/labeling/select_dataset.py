import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing import *
from text_processing import normalize_text
from embedding import load_model, generate_embedding


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


def process_review_sentences(input_file: str) -> pd.DataFrame:
    """
    강의평 문장들이 있는 json 파일 읽어와서 전처리
    """
    df = pd.read_json(input_file)

    # 중복 문장 제거 (학습 데이터는 학정번호 없어도 되니까 & 학습 데이터 중복 방지)
    df = df.drop_duplicates(subset=['sentence'])

    # 문장 길이가 10 이하인 문장 제거 (cf. 전체 학습 데이터 하위 5%의 문장길이가 9 이하)
    df = df[df['sentence'].apply(lambda x: len(x) > 10)].reset_index(drop=True)

    return df


def manhattan_distance(v1: list[float], v2: list[float]) -> float:
    """
    v1과 v2 사이의 manhattan distance 계산
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
    for i in range(review_sentences.shape[0]):
        distances = []
        for j in range(flag_sentences.shape[0]):
            distances.append(manhattan_distance(review_sentences.loc[i, 'embedding'], flag_sentences.loc[j, 'embedding']))
        distance_matrix.append(distances)
    return pd.DataFrame(distance_matrix, index=review_sentences.sentence, columns=flag_sentences.sentence)


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

    min_distance_matrix = pd.DataFrame(min_distance).transpose()
    min_distance_matrix.columns = ['수업 내용', '로드', '교수님 강의스타일 및 강의력', '시험 출제 스타일', '학점']
    
    return min_distance_matrix


def select_1000_sentences(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """
    각 토픽별로 200개씩 총 1000개의 문장 선택
    """
    df['sentence_index'] = df.index

    # 토픽별 유사도 순으로 정렬한 DataFrame 생성
    sorted_df = pd.DataFrame()
    column_list = ['수업 내용', '로드', '교수님 강의스타일 및 강의력', '시험 출제 스타일', '학점']
    for topic in column_list:
        sorted_df[topic] = df.sort_values(by=topic, ascending=True)['sentence_index'].values

    # 유사도 상위 1000개의 문장을 저장할 DataFrame 생성
    final_sentences = pd.DataFrame(columns=['sentence', 'topic', 'similarity'])

    # 문장 추출
    for _ in range(200):
        for topic in sorted_df.columns:
            for idx in sorted_df[topic]:
                # 이미 선택된 문장인지 확인
                if idx not in final_sentences['sentence'].values:
                    similarity = df.loc[df['sentence_index'] == idx, topic].values[0]
                    final_sentences = pd.concat([final_sentences, pd.DataFrame({'sentence': [idx], 'topic': [topic], 'similarity': [similarity]})])
                    break  # 다음 토픽으로 넘어감

        # 이미 1000개 문장을 선택했으면 종료
        if len(final_sentences) >= 1000:
            break

    final_sentences = final_sentences[['sentence', 'topic']].reset_index(drop=True)
    final_sentences.to_csv(output_path, index=False)

    return final_sentences