from pymongo import MongoClient, typings
from pymongo.database import Database, Collection
from pymongo.cursor import Cursor
import pprint


class MongoRepository:
    def __init__(self, host: str, port: int):
        # TODO: add exception handling logic
        self.client: MongoClient = MongoClient(host=host, port=port)
        self.db: Database = self.client["everytime"]

    def find_lecture_data(self) -> list[dict]:
        """
        [
          {
            "_id": {"$oid": "66bf38cccac788770e09c22d"},
            "code": "RUS3127-01-00",
            "name": "러시아문학과젠더",
            "place": "위205",
            "professorList": ["김혜란"],
            "time": {
              "화": [1],
              "목": [2, 3]
            },
            "type": ["대교", "전선"]
         },
        ]
        이런 형태로 반환
        """
        lecture_data_list: Cursor[typings._DocumentType] = self.db.lecture.find({})
        return list(lecture_data_list)

    def find_reviews_by_lecture_code(self, code: str) -> list[str]:
        """
        pipeline 변수: 학정번호 주어졌을때 학정번호에 해당하는 수강평 가져오는 쿼리
        [
            {
                "_id": "BIZ1101-08-00",
                "reviews": ["강의평1", "강의평2", "강의평3"]
            }
        ]
        이런식으로 학정번호에 해당하는 강의평들을 리스트형식으로 리턴받는다.
        따라서 result의 원소 개수는 1개입니다.
        """
        pipeline = [
            {
                '$match': {
                    'lectureCode': f"{code}"
                }
            },
            {
                '$group': {
                    '_id': "$lectureCode",
                    'reviews': {'$push': '$lectureReview.content'}
                }
            }
        ]
        result = list(self.db.reviews.aggregate(pipeline))
        if len(result) == 1:
            return result[0]["reviews"]
        elif len(result) == 0:
            return []
        else:
            raise Exception(f"only one result expected. but got {len(result)} code:{code}")
