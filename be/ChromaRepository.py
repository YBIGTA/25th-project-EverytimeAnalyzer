import random
import uuid
import ijson
from tqdm import tqdm
from chromadb import HttpClient, ClientAPI, Collection


class ChromaRepository:
    def __init__(self, host: str, port: int, collection_name: str):
        self.client: ClientAPI = HttpClient(host=host, port=port)
        self.collection: Collection = self.client.get_or_create_collection(collection_name)

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
    
    def add_data_to_collection_batch(self, data_path: str, batch_size: int = 100):
        """
        json 파일의 데이터를 chromadb에 배치 단위로 적재
        """
        with open(data_path, 'r') as f:
            data = ijson.items(f, 'item')

            sentences = []
            embeddings = []
            lectureCodes = []

            for obj in tqdm(data):
                sentences.append(obj['sentence'])
                embeddings.append(list(map(float, obj['embedding'])))
                lectureCodes.append(obj['lectureCode'])

                # 배치 크기만큼 모이면 데이터 적재
                if len(sentences) >= batch_size:
                    self._add_batch(sentences, embeddings, lectureCodes)
                    sentences.clear()
                    embeddings.clear()
                    lectureCodes.clear()

            # 마지막 배치 적재
            if sentences:
                self._add_batch(sentences, embeddings, lectureCodes)

    def _add_batch(self, sentences, embeddings, lectureCodes):
        """
        적재할 데이터를 배치로 처리하는 헬퍼 메서드
        """
        self.collection.add(
            ids=[str(uuid.uuid4()) for _ in range(len(sentences))],
            documents=sentences,
            embeddings=embeddings,
            metadatas=[{"code": code, "topic": self.random_topic()} for code in lectureCodes]
        )

    
    # TODO: 쿼리를 embedding vector로
    def get_similar_reviews(self, query: str, top_k: int = 4):
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



