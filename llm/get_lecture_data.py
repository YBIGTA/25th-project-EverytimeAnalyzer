import os
import logging
from dotenv import load_dotenv
from typing import List, Dict, Optional
from MongoRepository import MongoRepository

def load_env_vars() -> dict:
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

def get_syllabus_and_reviews(lecture_code: str, professor: str) -> Optional[Dict]:
    env_vars = load_env_vars()

    repo: MongoRepository = MongoRepository(
        env_vars['host'],
        env_vars['port'],
        env_vars['username'],
        env_vars['pw']
    )

    for lecture_data in repo.find_all_lecture_data():
        # 강의 코드와 교수님 이름으로 강의 선택
        if lecture_data['code'][:7] == lecture_code and professor in lecture_data['professorList']:
            syllabus = repo.find_syllabus_by_code(lecture_data['code'])
            reviews = repo.find_reviews_by_code(lecture_data["code"])

            if not syllabus or not reviews:
                logging.warning(f"Can't find syllabus or reviews with code: {lecture_data['code']}")
                continue

            return {
                'code': lecture_data['code'],
                'lecture_name': lecture_data['name'],
                'professor': lecture_data['professorList'],
                'syllabus': syllabus['syllabus'],
                'reviews': reviews
            }
    
    return None