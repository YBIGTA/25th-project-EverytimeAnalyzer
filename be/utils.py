from collections import defaultdict

from mock_functions import infer_topic
import numpy as np


def classify_query_by_topic(query: str):
    split_query_list = query.split(".")
    query_topic = defaultdict(str)
    for query_sentence in split_query_list:
        query_topic[infer_topic(query_sentence)] += (query_sentence + ".")
    return query_topic

topic_map = ["학점", "교수님 강의스타일 및 강의력", "수업 내용", "로드", "시험 출제 스타일"]

def cos_sim(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
