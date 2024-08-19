from sentence_transformers import SentenceTransformer
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm


def load_model(model_name: str = 'jhgan/ko-sroberta-multitask') -> SentenceTransformer:
    """
    사전학습된 SentenceTransformer 모델 호출
    Args:
        - model_name: 모델 이름 (기본값: 'jhgan/ko-sroberta-multitask')
    """
    return SentenceTransformer(model_name)

def generate_embedding(model: SentenceTransformer, sentences: list[str]) -> list:
    """
    문장별 embedding vector 생성
    Args:
        - model: embedding에 사용할 SentenceTransformer 모델
        - sentences: 문장 리스트
    """
    return model.encode(sentences)

def generate_embeddings_batch(model: SentenceTransformer, sentences: list[str], batch_size: int = 64) -> list:
    """
    배치별 embedding vector 생성
    Args:
        - model: embedding에 사용할 SentenceTransformer 모델
        - sentences: 문장 리스트
        - batch_size: 한 번에 처리할 문장 수
    """
    # 입력 문장을 batch_size 크기로 나누기
    batches = [sentences[i:i + batch_size] for i in range(0, len(sentences), batch_size)]
    
    embeddings = []
    
    # 배치 단위로 처리
    for batch in batches:
        batch_embeddings = model.encode(batch)
        embeddings.extend(batch_embeddings)
    
    return embeddings