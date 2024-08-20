import random
import uuid
import ijson
from tqdm import tqdm
from chromadb import HttpClient, ClientAPI, Collection


class ChromaRepository:
    def __init__(self, host: str, port: int):
        self.client: ClientAPI = HttpClient(host=host, port=port)
        self.collection: Collection = self.client.get_or_create_collection("reviews")

    def random_topic(self) -> str:
        """
        토픽 모델링 결과 나오기 전 임시 토픽 생성
        """
        topic_list = ['수업 내용', '로드', '교수님 강의스타일 및 강의력', '시험 출제 스타일', '학점']
        return random.choice(topic_list)
    
    def add_data_to_collection(self, data_path: str):
        """
        json 파일의 데이터를 chromadb에 적재
        """
        with open(data_path, 'r') as f:
            data = ijson.items(f, 'item')

            for obj in tqdm(data):
                self.collection.add(
                    ids=[str(uuid.uuid4())],
                    documents=obj["sentence"],
                    embeddings=list(map(float, (obj["embedding"]))),
                    metadatas=[{"code": obj['lectureCode'], 
                                "topic": self.random_topic()}]
                )
    
    # TODO: 쿼리를 embedding vector로
    def get_similar_reviews(self, query: str, top_k: int = 5):
        """
        chromadb를 이용하여 사용자 쿼리와 유사한 강의평 문장 검색
        """
        query_embedding = []

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
            # where={"metadata_field": "is_equal_to_this"},
            # where_document={"$contains":"search_string"}
            )
        return results



