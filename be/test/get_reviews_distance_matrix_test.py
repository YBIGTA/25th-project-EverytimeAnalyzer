from env import load_env_vars
from MongoRepository import MongoRepository
from chromadb import HttpClient, Collection
from VectorRepository import VectorRepository
from sentence_transformers import SentenceTransformer

env_vars = load_env_vars()
sentence_transformer = SentenceTransformer('jhgan/ko-sroberta-multitask')
vector_repo = VectorRepository(HttpClient(env_vars["host"], 48000), sentence_transformer)

print(vector_repo.get_reviews_distance_matrix("YCI1705-01-00", ["학점을 잘주는 강의", "재미있는 강의", "빡센 강의"]))
