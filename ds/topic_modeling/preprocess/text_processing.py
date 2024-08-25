import re
import kss
from hanspell import spell_checker

def split_sentences(reviews: list[str]) -> list[str]:
    """
    강의평을 문장 단위로 split
    Args:
        - reviews: 강의평 리스트
    """
    result = []
    for review in reviews:
        tmp = kss.split_sentences(review)
        result.extend(tmp)
    return result

def normalize_text(text: str) -> str:
    """
    강의평 전처리: 문장 내 공백 및 특수문자 제거, 맞춤법 교정
    Args:
        - text: 강의평
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s.,!?]', '', text)
    
    try:
        checked_text = spell_checker.check(text).as_dict()['checked']
    except Exception as e:
        print(f"Spell check failed for text: {text}. Error: {e}")
        checked_text = text
    
    return checked_text