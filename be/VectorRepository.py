from decimal import Decimal

from chromadb import ClientAPI, Collection, QueryResult
from sentence_transformers import SentenceTransformer


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

    def find_top_similar_lecture(self, query: str, topic: str) -> QueryResult:
        result: QueryResult = self.collection.query(
            query_embeddings=self.calculate_similarity(query),
            where={"topic": topic},
            n_results=50
        )
        return result
