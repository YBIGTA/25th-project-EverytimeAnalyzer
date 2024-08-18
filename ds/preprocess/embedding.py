from sentence_transformers import SentenceTransformer

def load_model(model_name: str = 'jhgan/ko-sroberta-multitask') -> SentenceTransformer:
    """Load and return the KR-SBERT model."""
    return SentenceTransformer(model_name)

def generate_embeddings(model: SentenceTransformer, sentences: list[str]) -> list:
    """Generate sentence embeddings using the given model."""
    return model.encode(sentences)