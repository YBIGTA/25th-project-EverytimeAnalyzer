import json
import logging
from typing import Dict, Optional

from llamaapi import LlamaAPI


class LlamaClient:
    def __init__(self, api_tokens: str, config_file_path: str):
        config = json.load(open(config_file_path, "r"))

        # get hyper-parameters
        self.hyperparameters = config["hyperparameters"]
        self.system_prompt = config["system_prompt"]
        self.user_prompt_template = config["user_prompt_template"]

        self.llama = LlamaAPI(api_tokens)

    def build_user_prompt(self, reviews: list[str], syllabus: str, lecture_info: dict) -> str:
        """
        user prompt 생성
        """
        lecture_name = lecture_info['name'],
        syllabus = syllabus
        reviews = " ".join(reviews)
        reviews_len = min(len(reviews), 4000)
        reviews = reviews[:reviews_len]
        return self.user_prompt_template.format(
            lecture_name=lecture_name,
            syllabus=syllabus,
            reviews=reviews
        )

    #TODO: reviews가 너무 많을 경우 일부만 request에 포함하기
    def request(self, lecture_info: dict, reviews: list[str], syllabus: str) -> str:

        user_prompt = self.build_user_prompt(reviews, syllabus, lecture_info)

        api_request_json = {
            "model": "llama-70b-chat",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }
        api_request_json.update(self.hyperparameters)

        try:
            response = self.llama.run(api_request_json)
            return response.json()['choices'][0]['message']['content']

        except Exception as e:
            logging.error("api 호출 중 오류 발생: %s", str(e))
