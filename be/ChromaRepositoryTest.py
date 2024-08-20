from ChromaRepository import ChromaRepository
from env import load_chroma_env_vars

env_vars = load_chroma_env_vars()
repo = ChromaRepository(env_vars["host"], env_vars["port"])


data_path = '/Users/jieunpark/Desktop/25th-project-EverytimeAnalyzer/ds/data/embedding_formatted.json'
repo.add_data_to_collection(data_path)
print("데이터 적재 완료!")