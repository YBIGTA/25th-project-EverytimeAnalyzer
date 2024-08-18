import os
from dotenv import load_dotenv
from MongoRepository import MongoRepository

# 환경변수로 mongodb host, password, username 설정
load_dotenv()
host = os.getenv('MONGO_HOST')
port = int(os.getenv('MONGO_PORT'))
username = os.getenv('MONGO_USERNAME')
pw = os.getenv('MONGO_PW')

if host is None:
    raise Exception("please set env MONGO_HOST")
if port is None:
    raise Exception("please set env MONGO_PORT")
if pw is None:
    raise Exception("please set env MONGO_PW")
if username is None:
    raise Exception("please set env MONGO_USERNAME")

repo: MongoRepository = MongoRepository(
    host,
    port,
    username,
    pw
)

# 강의 정보 모두 가져오기
lecture_data_list: list[dict] = repo.find_all_lecture_data()

# 강의 코드와 교수님 이름으로 강의 선택
lecture_code = "UCE1105"
professor = "강철"

with open("./lecture_reviews.txt", "w", encoding="utf-8") as file:

    for lecture_data in lecture_data_list:
        if lecture_data['code'][:7] == lecture_code and professor in lecture_data['professorList']:
            syllabus: [dict | None] = repo.find_syllabus_by_code(lecture_data['code'])
            reviews: list[str] = repo.find_reviews_by_code(lecture_data["code"])

            if syllabus is None or len(reviews) == 0:
                file.write(f"can't find syllabus or reviews with code:{lecture_data['code']}\n")
                continue

            file.write("-----\n")
            file.write(f"code: {lecture_data['code']}\n")
            file.write(f"lecture_name:{lecture_data['name']}\n")
            file.write(f"professor: {', '.join(lecture_data['professorList'])}\n")
            file.write(f"syllabus:{syllabus['syllabus']}\n")
            for idx, review in enumerate(reviews):
                file.write(f"\t review({idx}): {review}\n")