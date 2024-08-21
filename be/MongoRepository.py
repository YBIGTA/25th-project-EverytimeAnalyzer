from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database


# TODO: embedding 값 전부 블러오는 로직 작성
class MongoRepository:
    def __init__(self, host: str, port: int, username: str, password: str):
        # TODO: add exception handling logic
        self.client: MongoClient = MongoClient(host=host, port=port, username=username, password=password)
        self.db: Database = self.client["everytime"]

    def find_lecture_info(self, lecture_code: str) -> Optional[dict]:
        lecture_info = self.db.lecture.find_one({'code': lecture_code})
        return lecture_info

    def find_reviews(self, lectureCode: str) -> list[str]:
        """
        pipeline 변수: 학정번호 주어졌을때 학정번호에 해당하는 수강평 가져오는 쿼리
        [
            {
                "_id": "BIZ1101-08-00",
                "reviews": ["강의평1", "강의평2", "강의평3"]
            }
        ]
        위와 같은 형태로 강의평 반환. 강의평은 1개의 리스트 형태.
        """
        pipeline = [
            {
                '$match': {
                    'lectureCode': f"{lectureCode}"
                }
            },
            {
                '$group': {
                    '_id': "$lectureCode",
                    'reviews': {'$push': '$lectureReview.content'}
                }
            }
        ]
        result = self.db.reviews.aggregate(pipeline)
        result = list(result)
        if len(result) == 1:
            return result[0]["reviews"]
        elif len(result) == 0:
            return []
        else:
            raise Exception(f"only one result expected. but got {len(result)} code:{lectureCode}")

    def find_syllabus(self, lecture_code: str) -> Optional[str]:
        syllabus = self.db.syllabus.find_one({'lectureCode': lecture_code})
        if syllabus is None:
            return None
        else:
            return syllabus["syllabus"]

    def get_all_lecture_codes(self) -> list[str]:
        pipeline = [
            {'$group':
                {
                    '_id': '$lectureCode',
                }
            }
        ]
        result = self.db.reviews.aggregate(pipeline)
        result = list(result)
        result = list(map(lambda x: x['_id'], result))
        return result

