import os
import json
import logging
from dotenv import load_dotenv
from llamaapi import LlamaAPI


def load_env_vars() -> dict:
    '''
    환경 변수 로드 및 확인
    '''
    load_dotenv()
    api_token = os.getenv('API_TOKEN')
    if not api_token:
        raise Exception("Llama API token이 설정되지 않았습니다.")
    return api_token

def create_user_prompt(config_file: str, data: dict) -> str:
    '''
    user prompt 생성
    '''
    # template
    config = json.load(open(config_file, "r"))
    user_prompt_template = config["prompt"]["user_prompt_template"]

    # data
    lecture_name = data["lecture_name"]
    syllabus = data["syllabus"]
    reviews = " ".join(data["reviews"])

    return user_prompt_template.format(lecture_name=lecture_name, syllabus=syllabus, reviews=reviews)

def get_params(config_file: str) -> dict:
    '''
    config 파일에서 hyperparameters 로드
    hyperparameters 목록: https://github.com/llamaapi/llamaapi-python 참고
    '''
    config = json.load(open(config_file, "r"))
    params = config["hyperparameters"]
    params["system_prompt"] = config["prompt"]["system_prompt"]

    return params

def get_api_response(api_token: str, system_message: str, user_prompt: str, hyperparameters: dict) -> dict:
    '''
    llama api에 request 보내기
    '''
    llama = LlamaAPI(api_token)

    api_request_json = {
        "model": "llama-70b-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        }
    api_request_json.update(hyperparameters)

    response = llama.run(api_request_json)
    return response.json()['choices'][0]['message']['content']

def summarize_lecture(data):
    '''
    강의 개요 및 강의평 요약
    '''
    api_token = load_env_vars()
    params = get_params("config.json")

    system_message = params.pop("system_prompt")
    user_prompt = create_user_prompt("config.json", data)

    try:
        result = get_api_response(api_token, system_message, user_prompt, params)
        return result

    except Exception as e:
        logging.error("api 호출 중 오류 발생: %s", str(e))