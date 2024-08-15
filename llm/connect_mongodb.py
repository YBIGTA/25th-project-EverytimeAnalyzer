import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

# MongoDB 서버 연결
def connect_to_mongodb(host, port, db_name):
    try:
        client = MongoClient(host, port)
        db = client[db_name]
        return db
    except Exception as e:
        print(f"MongoDB 연결 실패: {e}")
        return None

# 데이터 조회
def fetch_data_from_collection(db, collection_name):
    try:
        collection = db[collection_name]
        data = collection.find()
        return list(data)
    except Exception as e:
        print(f"데이터 조회 실패: {e}")
        return None

# MongoDB 연결 정보
load_dotenv()
host = os.getenv('MONGODB_HOST')                        # EC2 인스턴스의 퍼블릭 IP 주소
port = int(os.getenv('MONGODB_PORT'))                   # MongoDB 포트 번호
db_name = os.getenv('MONGODB_DB')                       # MongoDB 데이터베이스 이름
collection_name = os.getenv('MONGODB_COLLECTION')       # 조회할 컬렉션 이름
# query = 

# MongoDB 연결 및 데이터 조회
db = connect_to_mongodb(host, port, db_name)
if db is not None:
    data = fetch_data_from_collection(db, collection_name)
    if data:
        for document in data[:30]:
            print(document)
    else:
        print("데이터가 없습니다.")