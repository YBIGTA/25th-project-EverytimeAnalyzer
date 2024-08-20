import uuid
from decimal import Decimal

import ijson
from chromadb import HttpClient, ClientAPI, Collection
from tqdm import tqdm

client: ClientAPI = HttpClient(port=48000)
collection: Collection = client.get_collection("foo")


def decimalToFloat(matrix: list[list[Decimal]]) -> list[list[float]]:
    result = []
    for row in matrix:
        tmp = list(map(float, row))
        result.append(tmp)
    return result


with open('/Users/gitp/Downloads/embedding.json', 'r') as f:
    data = ijson.items(f, 'item')

    for obj in tqdm(data):
        tmp = obj
        length = len(obj["content_normalized"])
        collection.add(
            ids=[str(uuid.uuid1()) for i in range(length)],
            documents=obj["content_normalized"],
            embeddings=decimalToFloat(obj["sentence_embeddings"]),
            metadatas=[{"code": obj['lectureCode']} for i in range(length)]
        )

"""
content, 
content_split,
content_normalized,
sentence_embeddings,
"""
