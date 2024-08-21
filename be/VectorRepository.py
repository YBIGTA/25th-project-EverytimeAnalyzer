from chromadb import ClientAPI, Collection, QueryResult
from sentence_transformers import SentenceTransformer
from decimal import Decimal


def decimalToFloat(matrix: list[list[Decimal]]) -> list[list[float]]:
    result = []
    for row in matrix:
        tmp = list(map(float, row))
        result.append(tmp)
    return result


class VectorRepository:
    def __init__(self, client: ClientAPI):
        collection_name = "lecture_reviews"
        self.client: ClientAPI = client
        print("loading transformer")
        self.transformer: SentenceTransformer = SentenceTransformer('jhgan/ko-sroberta-multitask')
        print("loading transformer complete")

        # TODO: excpetion
        self.collection: Collection = client.get_collection(collection_name)

    def calculate_similarity(self, lecture_code: str, query: str) -> float:
        result = self.collection.query(
            query_embeddings=list(map(float, self.transformer.encode(query))),
            where={'code': lecture_code},
            n_results=100
        )
        return sum(result["distances"][0])


    def find_top_similar_lecture(self, query: str, n: int) -> list[str]:
        result: QueryResult =  self.collection.query(
            query_embeddings= list(map(float, self.transformer.encode(query)))
        )

        return  result
