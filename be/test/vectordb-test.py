from chromadb import HttpClient, ClientAPI
from VectorRepository import VectorRepository
from sentence_transformers import SentenceTransformer

client: ClientAPI = HttpClient("43.201.1.128", 48000)

sentence_transformer =  SentenceTransformer('jhgan/ko-sroberta-multitask')
repo = VectorRepository(client, sentence_transformer)

print(result)

# result = client.get_collection("lecture_reviews").get(where={"code": "IIE4115-01-00"})
# print()
