import os
from dotenv import load_dotenv

def load_env_vars() -> dict:
    '''
    환경 변수 로드 및 확인
    '''
    load_dotenv()

    env_vars = {
        'host': os.getenv('MONGO_HOST'),
        'port': int(os.getenv('MONGO_PORT')),
        'username': os.getenv('MONGO_USERNAME'),
        'pw': os.getenv('MONGO_PW')
    }

    for key, value in env_vars.items():
        if value is None:
            raise Exception(f"please set env {key.upper()}")

    return env_vars

def load_chroma_env_vars() -> dict:
    '''
    ChromaDB 환경 변수 로드 및 확인
    '''
    load_dotenv()

    env_vars = {
        'host': os.getenv('CHROMA_HOST'),
        'port': int(os.getenv('CHROMA_PORT')),
    }

    for key, value in env_vars.items():
        if value is None:
            raise Exception(f"please set env {key.upper()}")

    return env_vars