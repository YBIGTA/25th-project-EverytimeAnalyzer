import random
import uuid
import ijson
import pandas as pd
from tqdm import tqdm
from chromadb import HttpClient, ClientAPI, Collection
from chromadb.utils import embedding_functions

# TODO: 토픽모델링 후 topic 부분 수정 필요
class ChromaSentence:
    def __init__(self, host: str, port: int, collection_name: str):
        self.client: ClientAPI = HttpClient(host=host, port=port)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection: Collection = self.client.get_or_create_collection(collection_name, embedding_function=self.embedding_function, metadata={"hnsw:M": 64})
        # self.collection: Collection = self.client.get_or_create_collection(collection_name)

    def random_topic(self) -> str:
        """
        토픽 모델링 결과 나오기 전 임시 토픽 생성
        """
        topic_list = ['수업 내용', '로드', '교수님 강의스타일 및 강의력', '시험 출제 스타일', '학점']
        return random.choice(topic_list)
    
    def load_data(self, data_path: str):
        """
        json 파일의 데이터를 chromadb에 적재
        """
        with open(data_path, 'r') as f:
            data = ijson.items(f, 'item')

            for obj in tqdm(data):
                self.collection.upsert(
                    ids=[str(uuid.uuid4())],
                    documents=obj["sentence"],
                    metadatas=[{"code": obj['lectureCode'], 
                                "topic": self.random_topic()}]  # 토픽모델링 완료 후 수정 필요
                )
    '''
    def load_data_batch(self, data_path: str, batch_size: int = 1000):
        """
        json 파일의 데이터를 chromadb에 배치 단위로 적재
        """
        with open(data_path, 'r') as f:
            data = ijson.items(f, 'item')

            sentences = []
            lectureCodes = []
            topics = []

            for obj in tqdm(data):
                sentences.append(obj['sentence'])
                lectureCodes.append(obj['lectureCode'])
                topics.append(self.random_topic())  # 토픽모델링 완료 후 수정 필요

                # 배치 크기만큼 모이면 데이터 적재
                if len(sentences) >= batch_size:
                    self._load_data(sentences, lectureCodes, topics)
                    sentences.clear()
                    lectureCodes.clear()
                    topics.clear()

            # 마지막 배치 적재
            if sentences:
                self._load_data(sentences, lectureCodes, topics)

    def _load_data(self, sentences, lectureCodes, topics):
        """
        적재할 데이터를 배치로 처리하는 헬퍼 메서드
        """
        embeddings = [self.embedding_function(sentence) for sentence in sentences]
        self.collection.upsert(
            ids=[str(uuid.uuid4()) for _ in range(len(sentences))],
            embeddings=embeddings,
            documents=sentences,
            metadatas=[{"code": code, "topic": topic} for code, topic in zip(lectureCodes, topics)]
        )
    '''

    # TODO: 쿼리를 embedding vector로
    def get_similar_reviews(self, query: str, top_k: int = 5):
        """
        chromadb를 이용하여 사용자 쿼리와 유사한 강의평 문장 검색
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
            )
        return results


class ChromaGroupbyTopic:
    def __init__(self, host: str, port: int, collection_name: str):
        self.client: ClientAPI = HttpClient(host=host, port=port)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection: Collection = self.client.get_or_create_collection(collection_name, embedding_function=self.embedding_function, metadata={"hnsw:M": 64})
    
    def load_data(self, data: pd.DataFrame):
        """
        json 파일의 데이터를 chromadb에 적재
        """
        for sentence, lectureCode, topic in tqdm(zip(data['sentence'], data['lectureCode'], data['topic'])):
            self.collection.upsert(
                ids=[str(uuid.uuid4())],
                documents=" ".join(sentence),
                metadatas=[{"code": lectureCode, 
                            "topic": topic}]
            )

    '''
    def load_data_batch(self, data: pd.DataFrame, batch_size: int = 100):
        """
        데이터프레임의 데이터를 chromadb에 배치 단위로 적재
        """
        sentences = []
        lectureCodes = []
        topics = []

        for sentence, lectureCode, topic in tqdm(zip(data['sentence'], data['lectureCode'], data['topic'])):
            sentences.append(" ".join(sentence))
            lectureCodes.append(lectureCode)
            topics.append(topic)

            # 배치 크기만큼 모이면 데이터 적재
            if len(sentences) >= batch_size:
                self._load_data(sentences, lectureCodes, topics)
                sentences.clear()
                lectureCodes.clear()
                topics.clear()

        # 마지막 배치 적재
        if sentences:
            self._load_data(sentences, lectureCodes, topics)

    def _load_data(self, sentences, lectureCodes, topics):
        """
        적재할 데이터를 배치로 처리하는 헬퍼 메서드
        """
        self.collection.upsert(
            ids=[str(uuid.uuid4()) for _ in range(len(sentences))],
            documents=sentences,
            metadatas=[{"code": code, "topic": topic} for code, topic in zip(lectureCodes, topics)]
        )
    '''

    # TODO: 쿼리를 embedding vector로
    def get_similar_reviews(self, query: str, top_k: int = 5):
        """
        chromadb를 이용하여 사용자 쿼리와 유사한 강의평 문장 검색
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
            )
        return results