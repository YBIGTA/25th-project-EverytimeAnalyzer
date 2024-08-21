from chromadb import HttpClient, ClientAPI
from VectorRepository import VectorRepository

client: ClientAPI = HttpClient("43.201.1.128", 48000)

# collections = client.list_collections()
# print()

repo = VectorRepository(client)
result = repo.calculate_similarity("IIE4115-01-00", "강의력 좋은")
print(result)

# result = client.get_collection("lecture_reviews").get(where={"code": "IIE4115-01-00"})
# print()
