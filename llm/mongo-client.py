from pymongo import MongoClient, typings
from pymongo.database import Database, Collection
from pymongo.cursor import Cursor
import pprint

client: MongoClient = MongoClient(host='43.201.1.128', port=27017)
db: Database = client["everytime"]
reviews: Collection = db["reviews"]
lectures: Collection = db["lecture"]
docs: Cursor[typings._DocumentType] = reviews.find({"lectureCode": "UCE1105-01-00"})
reviewList: list[str] = []


def get_lecture_data_list() -> list[dict]:
    lecture_data_list: Cursor[typings._DocumentType] = reviews.find({})
    return list(lecture_data_list)

pprint.pprint(list(get_lecture_data_list()))

def get_reviews_by_lecture_code(code: str) -> list[str]:
    """
    pipeline변수: 학정번호 주어졌을때 학정번호에 해당하는 수강평 가져오는 쿼리
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
    result = list(reviews.aggregate(pipeline))
    assert (len(result) == 1)
    return result[0]["reviews"]


get_reviews_by_lecture_code('BIZ1101-08-00')
