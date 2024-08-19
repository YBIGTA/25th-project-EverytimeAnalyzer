import os

def load_env_vars() -> dict:
    '''
    환경 변수 로드 및 확인
    '''
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
