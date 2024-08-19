from fastapi import FastAPI
from MongoRepository import MongoRepository
from typing import Optional
from env import load_env_vars

app = FastAPI()
env_vars = load_env_vars()
repo = MongoRepository(env_vars["host"], env_vars["port"], env_vars["username"], env_vars["pw"])
"""
학정번호가 주어졌을 때 강의 정보 반환

ex) /lecture/RUS3127-01-00
"""
@app.get("/lecture/{lecture_code}")
def get_lecture(lecture_code: str):
    # 임시
    lecture: Optional[dict] = repo.find_lecture_info(lecture_code)
    del lecture["_id"]
    return lecture

"""
각 토픽(아마 5개??)별 쿼리가 주어졌을 때 모델이 추천하는 n(아마 5개)강의의 학정번호 반환
ex) /model/?topic1="교수님 강의력이 좋은"&topic2="학점 잘주는"&topic3="블라블라블라~~"&topic4="블라~~"&topic5="블라블라~~"
"""
@app.get("/model/")
def get_recommend_lecture(topic1: str, topic2: str, topic3: str, topic4: str, topic5: str):
    # 임시
    return {"topic1": topic1, "topic2": topic2,"topic3": topic3,"topic4": topic4,"topic5": topic5,}

"""
학정번호가 주어졌을 때 llm의 강의 요약 반환
ex) /llm/RUS3127-01-00
"""
@app.get("/llm/{lecture_code}")
def get_llm_summary(lecture_code: str):
    # 임시
    return {"lecture_code": lecture_code}

