from typing import Optional

from chromadb import HttpClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from collections import defaultdict

from sentence_transformers import SentenceTransformer
from LlamaClient import LlamaClient
from MongoRepository import MongoRepository
from VectorRepository import VectorRepository
from env import load_env_vars

app = FastAPI()
# cors setting
app.add_middleware(
    CORSMiddleware,
    allow_origins= [
        "http://localhost:8080",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentence_transformer =  SentenceTransformer('jhgan/ko-sroberta-multitask')
# 환경변수 로딩
env_vars = load_env_vars()
repo = MongoRepository(env_vars["host"], env_vars["port"], env_vars["username"], env_vars["pw"])
vector_repo = VectorRepository(HttpClient(env_vars["host"], 48000), sentence_transformer)
llama_client = LlamaClient(env_vars["llama_token"], "./config/config.json")


# 학정번호가 주어졌을 때 강의 정보 반환
@app.get("/lecture/{lecture_code}")
def get_lecture(lecture_code: str):
    lecture: Optional[dict] = repo.find_lecture_info(lecture_code)
    del lecture["_id"]
    return lecture


# 쿼리가 주어졌을 때 학정번호 반환(5개)
@app.get("/model/")
def get_recommend_lecture(query: str):
    lecture_codes = []
    topics = ["학점", "교수님 강의스타일 및 강의력", "수업 내용", "로드", "시험 출제 스타일"]
    for topic in topics:
        result = vector_repo.find_top_similar_lecture(query, topic)
        lecture_codes.extend(
            list(map(lambda x: x['code'], result["metadatas"][0]))
        )
    lecture_code_count = defaultdict(int)
    for code in lecture_codes:
        lecture_code_count[code] += 1

    result = sorted(lecture_code_count.items(), key=lambda item: item[1], reverse=True)[:5]
    result = list(map(lambda x: x[0]), result)
    return result


@app.get("/reviews/{lecture_code}")
def get_reviews(lecture_code: str):
    return repo.find_reviews(lecture_code)


# 학정번호가 주어졌을 때 llm의 강의 요약 반환
@app.get("/llm/{lecture_code}")
def get_llm_summary(lecture_code: str):
    syllabus: str = repo.find_syllabus(lecture_code)
    reviews: list[str] = repo.find_reviews(lecture_code)
    lecture_info: dict = repo.find_lecture_info(lecture_code)

    summary = llama_client.request(
        lecture_info,
        reviews,
        syllabus
    )
    return {"summary": summary}
