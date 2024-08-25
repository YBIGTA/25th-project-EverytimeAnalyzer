from typing import Optional

from chromadb import HttpClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

import utils
from LlamaClient import LlamaClient
from MongoRepository import MongoRepository
from VectorRepository import VectorRepository
from env import load_env_vars
from utils import *

app = FastAPI()
# cors setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경변수 로딩
env_vars = load_env_vars()

# embedding 모델
sentence_transformer = SentenceTransformer('jhgan/ko-sroberta-multitask')

mongo_repo = MongoRepository(env_vars["host"], env_vars["port"], env_vars["username"], env_vars["pw"])
vector_repo = VectorRepository(HttpClient(env_vars["host"], 48000), sentence_transformer)
llama_client = LlamaClient(env_vars["llama_token"], "./config/config.json")


# 학정번호가 주어졌을 때 강의 정보 반환
@app.get("/lecture/{lecture_code}")
def get_lecture(lecture_code: str):
    lecture: Optional[dict] = mongo_repo.find_lecture_info(lecture_code)
    del lecture["_id"]
    return lecture


# 쿼리가 주어졌을 때 학정번호 반환(5개)
@app.get("/model/")
def get_recommend_lecture(query: str) -> list:
    # 쿼리 문장을 topic에 따라 분류
    query_topic = utils.classify_query_by_topic(query)

    #key: 학정번호 value: distance합
    distance_sum = defaultdict(float)

    for topic_idx, query_sentences in query_topic.items():
        reviews = vector_repo.get_reviews_by_query(
            query_sentences,
            topic_idx,
            100
        )
        for review in reviews:
            distance_sum[review["code"]] += review["distance"]

    return sorted(distance_sum.items(), key=lambda item: item[1], reverse=True)[:5]


# 각 topic별 distance 평균 반환
@app.get("/model/sims/{lecture_code}/")
def get_sims_by_topic(lecture_code: str, query: str) -> dict:
    # TODO: input 형식 체크
    split_query:list[str] = query.split(".")
    if split_query[-1] == "":
        del split_query[-1]
    distance_avg_map=  vector_repo.get_reviews_distance_matrix(lecture_code, split_query)
    return distance_avg_map

    # # 쿼리 문장 topic에 따라 분류
    # query_topic = utils.classify_query_by_topic(query)
    #
    # # topic에 따라 분류된 embedded reviews
    # topic_reviews_dict = vector_repo.get_embedded_review(lecture_code)
    #
    # topic_sim_avg = dict()
    # for topic_idx, q in query_topic.items():
    #     embedded_reviews = topic_reviews_dict[topic_map[topic_idx]]
    #     sim_sum = 0
    #     for review in embedded_reviews:
    #         embedded_query = sentence_transformer.encode(q)
    #         sim = cos_sim(embedded_query, np.array(review))
    #         sim_sum += sim
    #     if len(embedded_reviews) == 0:
    #         continue
    #     topic_sim_avg[topic_idx] = sim_sum / len(embedded_reviews)
    #
    # return topic_sim_avg


@app.get("/reviews/{lecture_code}")
def get_reviews(lecture_code: str):
    return mongo_repo.find_reviews(lecture_code)


# 학정번호가 주어졌을 때 llm의 강의 요약 반환
@app.get("/llm/{lecture_code}")
def get_llm_summary(lecture_code: str):
    syllabus: str = mongo_repo.find_syllabus(lecture_code)
    reviews: list[str] = mongo_repo.find_reviews(lecture_code)
    lecture_info: dict = mongo_repo.find_lecture_info(lecture_code)

    summary = llama_client.request(
        lecture_info,
        reviews,
        syllabus
    )
    return {"summary": summary}
