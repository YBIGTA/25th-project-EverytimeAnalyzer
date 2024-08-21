import pandas as pd
import random

from env import load_chroma_env_vars
from ChromaRepository import ChromaSentence, ChromaGroupbyTopic


def random_topic() -> str:
    """
    토픽 모델링 결과 나오기 전 임시 토픽 생성
    """
    topic_list = ['수업 내용', '로드', '교수님 강의스타일 및 강의력', '시험 출제 스타일', '학점']
    return random.choice(topic_list)

def group_by_topic(data_path: str) -> pd.DataFrame:
    """
    json 파일의 데이터를 강의, 토픽별로 그룹화
    """
    df = pd.read_json(data_path)
    df = df.drop(columns=['embedding'], axis=1)
    df['topic'] = df.apply(lambda topic: random_topic(), axis=1)
    grouped_df = df.groupby(['lectureCode', 'topic'])
    result = grouped_df['sentence'].apply(list).reset_index()
    return result

def load_data_to_collections(sentence_collection_name: str, groupby_collection_name: str, data_path: str):
    data = group_by_topic(data_path)

    env_vars = load_chroma_env_vars()

    repo_groupby = ChromaGroupbyTopic(env_vars["host"], env_vars["port"], groupby_collection_name)
    repo_groupby.load_data(data)
    print(f"{groupby_collection_name} 적재 완료!")

    repo_sentence = ChromaSentence(env_vars["host"], env_vars["port"], sentence_collection_name)
    repo_sentence.load_data(data_path)
    print(f"{sentence_collection_name} 적재 완료!")


if __name__ == "__main__":
    data_path = "/Users/jieunpark/Desktop/25th-project-EverytimeAnalyzer/sample/embedding_formatted.json"
    load_data_to_collections('test_sentence', 'test_groupby', data_path)