# main.py
# INPUT: 학정번호 / 교수명을 입력으로 받으면
# OUTPUT: llm이 해당 강의의 강의개요 및 강의평을 요약하여 반환


import logging
from get_lecture_data import get_syllabus_and_reviews
from llama_inference import summarize_lecture

def main():
    try:
        # 사용자 입력 받기
        lecture_code = input("학정번호를 입력하세요: ")
        professor = input("교수명을 입력하세요: ")

        # DB에서 강의 개요와 강의평 가져오기
        data = get_syllabus_and_reviews(lecture_code, professor)
        if not data:
            logging.error(f"학정번호 {lecture_code}, 교수명 {professor}에 해당하는 강의 데이터를 찾을 수 없습니다.")
            return

        # LLM으로 강의 개요와 강의평 요약하기
        summary = summarize_lecture(data)

        # 결과 출력
        print("\n[요약 결과]")
        print(summary)

    except Exception as e:
        logging.error("프로그램 실행 중 오류 발생: %s", str(e))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()