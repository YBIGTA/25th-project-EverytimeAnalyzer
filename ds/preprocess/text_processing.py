import re
import kss
from hanspell import spell_checker

def split_sentences(reviews: list[str]) -> list[str]:
    """Split reviews into sentences."""
    result = []
    for review in reviews:
        tmp = kss.split_sentences(review)
        result.extend(tmp)
    return result

def normalize_text(text: str) -> str:
    """Normalize text by removing unwanted characters and applying spell checking."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s.,!?]', '', text)
    
    try:
        checked_text = spell_checker.check(text).as_dict()['checked']
    except Exception as e:
        print(f"Spell check failed for text: {text}. Error: {e}")
        checked_text = text
    
    return checked_text