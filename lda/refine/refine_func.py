from konlpy.tag import Okt
from _collections import defaultdict

okt = Okt()

def deto(tokenList: list[list[str]]) -> list[str]:
    result = []
    for tokens in tokenList:
        result.append(" ".join(tokens))
    return result

def ppos(reviews: list[str]) -> list[list[tuple[str]]]:
    result: list[list[tuple[str]]] = []
    for review in reviews:
        tmp = okt.pos(review)
        result.append(tmp)
    return result


def extract_pos(reviews: list[str], pos: str) -> list[list[str]]:
    ppos_extracted = ppos(reviews)
    result = []
    for row in ppos_extracted:
        tmp = list(filter(lambda t: t[1] == pos, row))
        tmp = list(map(lambda t: t[0], tmp))
        result.append(tmp)
    return result


def count_frequency(posList: list[list[str]]) -> dict:
    frequency = defaultdict(int)
    flatten = sum(posList, [])
    for token in flatten:
        frequency[token] += 1
    return frequency


def filter_stopword(tokensList: list[list[str]], stopwords: list[str]) -> list[list[str]]:
    result: list[list[str]] = []
    for tokens in tokensList:
        sentence: list[str] = list(filter(lambda s: s not in stopwords, tokens))
        result.append(sentence)
    return result




def pos_tagging(tokens: list[tuple[str]], exclude_list: list[str]) -> list[tuple[str]]:
    result: list[tuple[str]] = []
    for token in tokens:
        if token[1] not in exclude_list:
            result.append(token)
    return result
# def token_dict(reviews: str) -> dict:
