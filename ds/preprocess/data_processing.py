import json
import pandas as pd

def load_json(json_path: str) -> pd.DataFrame:
    """
    json 파일을 읽어 DataFrame 형태로 반환
    Args:
        - json_path: json 파일 경로
    """
    with open(json_path, 'r', encoding='UTF8') as f:
        js = json.loads(f.read())
    return pd.DataFrame(js)

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    json에서 단순 변환한 DataFrame을 lectureCode, year, semester, content, rate로 구성된 DataFrame으로 변환한 후, 강의 단위로 그룹화
    Args:
        - df: DataFrame
    """
    df =  pd.DataFrame({
        'lectureCode': df['lectureCode'],
        'year': df['lectureReview'].apply(lambda x: x['year']),
        'semester': df['lectureReview'].apply(lambda x: x['semester']),
        'content': df['lectureReview'].apply(lambda x: x['content']),
        'rate': df['lectureReview'].apply(lambda x: x['rate'])
    })
    df = df.groupby('lectureCode')['content'].apply(lambda x: ' '.join(x)).reset_index()
    return df

def save_to_csv(df: pd.DataFrame, csv_path: str) -> None:
    """
    DataFrame을 csv 파일로 저장
    Args:
        - df: DataFrame
        - csv_path: 저장할 csv 파일 경로
    """
    df.to_csv(csv_path, sep=',', na_rep='', header=True, encoding='utf-8-sig')
