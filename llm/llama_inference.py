import os
import json
import logging
from dotenv import load_dotenv
from llamaapi import LlamaAPI


def load_env_vars() -> dict:
    load_dotenv()
    api_token = os.getenv('API_TOKEN')
    if not api_token:
        raise Exception("Llama API token이 설정되지 않았습니다.")
    return api_token

def create_user_message(config_file: str, data: dict) -> str:
    # template
    config = json.load(open(config_file, "r"))
    user_prompt_template = config["prompt"]["user_prompt_template"]

    # data
    lecture_name = data["lecture_name"]
    syllabus = data["syllabus"]
    reviews = " ".join(data["reviews"])

    return user_prompt_template.format(lecture_name=lecture_name, syllabus=syllabus, reviews=reviews)

def get_hyperparameters(config_file: str) -> dict:
    config = json.load(open(config_file, "r"))
    config_dict: dict = {}
    config_dict["system_prompt"] = config["prompt"]["system_prompt"]
    config_dict["max_tokens"] = config["hyperparameters"]["max_tokens"]
    return config_dict

def get_api_response(api_token: str, system_message: str, user_message: str, max_tokens: int) -> dict:
    llama = LlamaAPI(api_token)
    api_request_json = {
        "model": "llama-70b-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
        "max_tokens": max_tokens
        }
    response = llama.run(api_request_json)
    return response.json()['choices'][0]['message']['content']

def summarize_lecture(data):
    try:
        api_token = load_env_vars()
        system_message = get_hyperparameters("config.json")["system_prompt"]
        user_message = create_user_message("config.json", data)
        max_tokens = get_hyperparameters("config.json")["max_tokens"]
        
        result = get_api_response(api_token, system_message, user_message, max_tokens)
        print(result)

    except Exception as e:
        logging.error("프로그램 실행 중 오류 발생: %s", str(e))