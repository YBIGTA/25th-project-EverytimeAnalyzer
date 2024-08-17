import os
from MongoRepository import MongoRepository

# 환경변수로 mongodb host, password, username 설정
# 임시로 주석처리하고 하드코딩해도 됩니다
host = os.getenv('MONGO_HOST')
pw = os.getenv('MONGO_PW')
username = os.getenv('MONGO_USERNAME')
if host is None:
    raise Exception("please set env MONGO_HOST")
if pw is None:
    raise Exception("please set env MONGO_PW")
if username is None:
    raise Exception("please set env MONGO_USERNAME")

# 일단 host ip 하드코딩
repo: MongoRepository = MongoRepository(
    host,
    27017,
    username,
    pw
)

# 강의 정보 모두 가져오기
lecture_data_list: list[dict] = repo.find_all_lecture_data()

for lecture_data in lecture_data_list:
    syllabus: [dict | None] = repo.find_syllabus_by_code(lecture_data['code'])
    reviews: list[str] = repo.find_reviews_by_code(lecture_data["code"])

    # 데이터 정합성이 맞지 않아 학정번호에 해당되는 강의개요, 후기들이 없을경우 우선 pass
    # 최대한 정합성을 맞추려고 노렸했당.
    if syllabus is None or len(reviews) == 0:
        print(f"can't find syllabus or reviews with code:{lecture_data['code']}")
        continue

    print("-----")
    print(f"code: {lecture_data['code']}")
    print(f"lecture_name:{lecture_data['name']}")
    print(f"syllabus:{syllabus['syllabus']}")
    for idx, review in enumerate(reviews):
        print(f"\t review({idx}): {review}")
