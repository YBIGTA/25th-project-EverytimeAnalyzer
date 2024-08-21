from sentence_transformers import SentenceTransformer
from ChromaRepository import ChromaRepository
from env import load_chroma_env_vars
from embedding import load_model, generate_embedding

def get_similar_reviews(query: str, repo: ChromaRepository, model: SentenceTransformer, top_k: int = 4):
    """
    사용자에게 입력에 대하여 chromadb에서 유사한 강의평 문장 검색 후 해당 강의평의 학정번호 반환
    """
    query_embedding = generate_embedding(model, [query])
    results = repo.collection.query(query_embeddings=query_embedding, n_results=top_k)

    metadatas = results['metadatas'][0]
    reviews = results['documents'][0]
    for metadata, review in zip(metadatas, reviews):
        print(f"학정번호: {metadata['code']}")
        print(f"강의평: {review}")
        print("----------")
    
    return [metadata['code'] for metadata in metadatas]

def main():
    query = input("어떤 강의를 수강하고 싶으신가요?: ")
    env_vars = load_chroma_env_vars()
    repo = ChromaRepository(env_vars["host"], env_vars["port"], 'lecture_reviews')
    model = load_model()
    return get_similar_reviews(query, repo, model)

if __name__ == "__main__":
    main()

