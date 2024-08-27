from collections import defaultdict

from chromadb import ClientAPI, Collection, QueryResult, GetResult
from sentence_transformers import SentenceTransformer
import numpy as np

import utils


class VectorRepository:
    def __init__(self, client: ClientAPI, transformer: SentenceTransformer):
        self.client: ClientAPI = client
        # TODO: excpetion
        self.collection: Collection = client.get_collection("lecture_reviews")
        self.transformer: SentenceTransformer = transformer

    def embed_sentence(self, sentence: str):
        return list(map(float, self.transformer.encode(sentence)))

    # def calculate_similarity(self, lecture_code: str, query: str) -> float:
    #     result = self.collection.query(
    #         query_embeddings= self.embed_sentence(query),
    #         where={'code': lecture_code},
    #     )
    #     return sum(result["distances"][0])

    # def get_reviews(self, lecture_code: str, query: str):
    #     topics = ["학점", "교수님 강의스타일 및 강의력", "수업 내용", "로드", "시험 출제 스타일"]
    #     results = dict()
    #     for topic in topics:
    #         result: QueryResult = self.collection.query(
    #             query_embeddings=self.embed_sentence(query),
    #             # where={"code": lecture_code, "topic": topic},
    #             where={"$and": [{"code": lecture_code}, {"topic": topic}]},
    #             n_results=15
    #         )

    def find_top_similar_lecture(self, query: str, topic: str) -> QueryResult:
        result: QueryResult = self.collection.query(
            query_embeddings=self.embed_sentence(query),
            where={"topic": topic},
            n_results=100,
        )
        return result

        # topic 별로 분리된 embedded reviews vectordb에서 가져오기

    def get_embedded_review(self, lecture_code: str) -> dict:
        reviews_get_result: GetResult = self.collection.get(
            where={"code": lecture_code},
            include=['embeddings', 'metadatas']
        )

        metadatas = reviews_get_result['metadatas']
        embeddings = reviews_get_result['embeddings']

        topic_reviews_dict = defaultdict(list)
        for i in range(len(metadatas)):
            topic_reviews_dict[metadatas[i]['topic']].append(embeddings[i])

        return topic_reviews_dict

    def get_reviews_distance_matrix(self, lecture_code: str, queries: list[str]) -> dict:
        embedded_queries = list(map(lambda x: self.embed_sentence(x), queries))
        results: QueryResult = self.collection.query(
            query_embeddings=embedded_queries,
            where={"code": lecture_code},
            n_results=100
        )
        distance_matrix: list[list[float]] = results["distances"]
        distance_avg_map = {}
        for idx in range(len(queries)):
            if len(distance_matrix[idx]) != 0:
                distance_avg_map[queries[idx]] = sum(distance_matrix[idx]) / len(distance_matrix[idx])
            else:
                distance_avg_map[queries[idx]] = None

        return distance_avg_map
        # distance를 반환 로직 변경될 수 있다.

    def get_reviews_classified(self, lecture_code: str, queries: list[str], topic: str) -> list:
        embedded_queries = list(map(lambda x: self.embed_sentence(x), queries))

        # TODO: query를 topic별로 분류해서 그에 맞는 topic들에 대해서만 쿼리
        results: GetResult = self.collection.get(
            # query_embeddings=embedded_queries,
            where={"$and": [{"code": lecture_code}, {"topic": topic}]},
            limit=5
        )

        return results["documents"]


    def get_reviews_by_query(self, query: str, topic_idx: int, n: int):
        embedded_query = self.transformer.encode(query).reshape(1, -1)
        query_result: QueryResult = self.collection.query(
            query_embeddings=embedded_query,
            where={"topic": utils.topic_map[topic_idx]},
            n_results=n
        )

        metadatas = query_result["metadatas"][0]
        distances = query_result["distances"][0]
        documents = query_result["documents"][0]
        query_result_len = len(metadatas)
        result = list()
        for i in range(query_result_len):
            element = {
                'code': metadatas[i]["code"],
                'topic': metadatas[i]["topic"],
                "distance": distances[i],
                "review": documents[i]
            }
            result.append(element)
        return result