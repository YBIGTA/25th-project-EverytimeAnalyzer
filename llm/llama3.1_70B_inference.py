import os
import json
from dotenv import load_dotenv
from llamaapi import LlamaAPI

# Initialize the llamaapi with api_token
load_dotenv()
api_token = os.getenv('API_TOKEN')
llama = LlamaAPI(api_token)

# TODO: DB 연결. 지금은 임시로 sample_data.json에 저장된 데이터를 사용
with open("sample_data.json", "r") as f:
    data = json.load(f)

course_name = data["course_name"]
course_overview = data["course_overview"]
course_review = data["course_reviews"]

# Define input
# TODO: prompt 받는 부분 따로 모듈화
system_message = "강의 정보를 바탕으로 강의 개요와 강의평을 요약하세요. 답변 형식에 맞추어 답변하세요."
user_message = f"""
[강의 정보]
- 강의명: {course_name}
- 강의 개요: {course_overview}
- 강의평: {course_review}

[답변 형식]
- 강의명: (강의명)
- 강의 개요: (강의 개요 요약)
- 강의평:
    - 학점: (강의평에서 학점과 관련한 내용 요약)
    - 로드: (강의평에서 로드와 관련한 내용 요약)
    - 강의력: (강의평에서 강의력과 관련한 내용 요약)
"""

# Define API request
api_request_json = {
    "model": "llama-70b-chat",
    "messages": [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ],
    "stream": False,
    "max_tokens": 4096
    }

# Make your request and handle the responses
response = llama.run(api_request_json)
result = response.json()['choices'][0]['message']['content']
print(result)