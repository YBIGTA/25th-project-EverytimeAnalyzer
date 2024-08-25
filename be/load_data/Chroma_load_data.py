import pandas as pd
import random

from env import load_chroma_env_vars
from ChromaRepository import ChromaSentence, ChromaGroupbyTopic


def prepare_group_data(data_path: str) -> pd.DataFrame:
    """
    csv 파일의 데이터를 강의, 토픽별로 그룹화
    Args:
        data_path (str): lectureCode, topic, content_split 컬럼을 포함하는 csv 파일 경로
    Returns:
        pd.DataFrame: 강의 및 토픽별로 강의평 문장들을 그룹화한 데이터프레임.
        sentence 컬럼은 각 강의평을 원소로 하는 리스트로 구성.
    """
    df = pd.read_csv(data_path)
    df = df[['lectureCode', 'topic', 'content_split']]
    grouped_df = df.groupby(['lectureCode', 'topic'])
    result = grouped_df['content_split'].apply(list).reset_index()
    result.rename(columns={'content_split': 'sentence'}, inplace=True)
    return result

def prepare_sentence_data(data_path: str) -> pd.DataFrame:
    """
    csv 파일의 데이터를 데이터프레임으로 반환.
    Args:
        data_path (str): lectureCode, topic, content_split 컬럼을 포함하는 csv 파일 경로
    Returns:
        pd.DataFrame: 강의평 문장들을 포함하는 데이터프레임.
    """
    df = pd.read_csv(data_path)
    df = df[['lectureCode', 'topic', 'content_split']]
    df.rename(columns={'content_split': 'sentence'}, inplace=True)
    return df

def load_data_to_collections(sentence_collection_name: str, groupby_collection_name: str, data_path: str):
    env_vars = load_chroma_env_vars()

    # 강의 및 토픽별로 그룹화한 데이터 적재
    data = prepare_group_data(data_path)
    repo_groupby = ChromaGroupbyTopic(env_vars["host"], env_vars["port"], groupby_collection_name)
    repo_groupby.load_data(data)
    print(f"{groupby_collection_name} 적재 완료!")

    # 강의평 문장 데이터 적재
    data = prepare_sentence_data(data_path)
    repo_sentence = ChromaSentence(env_vars["host"], env_vars["port"], sentence_collection_name)
    repo_sentence.load_data(data)
    print(f"{sentence_collection_name} 적재 완료!")


if __name__ == "__main__":
    data_path = "/Users/jieunpark/Desktop/25th-project-EverytimeAnalyzer/ds/topic_modeling/src/prediction/prediction.csv"
    load_data_to_collections('review_sentence', 'review_topic', data_path)