from chromadb import HttpClient, ClientAPI

from MongoRepository import MongoRepository
from VectorRepository import VectorRepository
from env import load_env_vars
from collections import defaultdict
from sentence_transformers import SentenceTransformer


env_vars = load_env_vars()
sentence_transformer =  SentenceTransformer('jhgan/ko-sroberta-multitask')
repo = MongoRepository(env_vars["host"], env_vars["port"], env_vars["username"], env_vars["pw"])
vector_repo = VectorRepository(HttpClient(env_vars["host"], 48000))

# code_list: list[str] = repo.get_all_lecture_codes()
# for code in code_list:
#     distance_sum = vector_repo.calculate_similarity(code, "강의력 좋은")
#     print(f"{code}'s distance: {distance_sum}")


"""
학점
교수님 강의스타일 및 강의력
수업 내용
로드
시험 출제 스타일
"""
topics = ["학점", "교수님 강의스타일 및 강의력", "수업 내용", "로드", "시험 출제 스타일"]
query = "강의력 좋은"
codes = []
for topic in topics:
    result = vector_repo.find_top_similar_lecture(query, topic)
    codes.extend(
        list(map(lambda x: x['code'], result["metadatas"][0]))
    )

print(len(codes))
cnt_dict = defaultdict(int)
for code in codes:
    cnt_dict[code] += 1

for key, val in sorted(cnt_dict.items(), key= lambda item: item[1]):
    print(key, val)

sorted(cnt_dict.items(), key=lambda item: item[1])



"""
학점
교수님 강의스타일 및 강의력
수업 내용
로드
시험 출제 스타일
"""

"""
metadatas
    code
    topic
documents

"""
