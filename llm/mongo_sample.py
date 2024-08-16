import os

from MongoRepository import MongoRepository

# host = os.getenv('MONGO_HOST')
# if host is None:
#     raise Exception("plese set env MONGO_HOST")

# 일단 그냥 host ip 하드코딩
repo: MongoRepository = MongoRepository("43.201.1.128", 27017)
lecture_data_list: list[dict] = repo.find_lecture_data()

for lecture_data in lecture_data_list:
    reviews = repo.find_reviews_by_lecture_code(lecture_data["code"])
    print("-----")
    print(f"lecture_name:{lecture_data['name']}")
    print(f"lecture_code:{lecture_data['code']}")
    for idx, review in enumerate(reviews):
        print(f"\t review({idx}): {review}")
