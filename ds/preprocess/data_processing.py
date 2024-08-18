import json
import pandas as pd

def load_json(json_path: str) -> pd.DataFrame:
    """Load JSON file and return as a DataFrame."""
    with open(json_path, 'r', encoding='UTF8') as f:
        js = json.loads(f.read())
    return pd.DataFrame(js)

def save_to_csv(df: pd.DataFrame, csv_path: str) -> None:
    """Save DataFrame to a CSV file."""
    df.to_csv(csv_path, sep=',', na_rep='', header=True, encoding='utf-8-sig')

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare DataFrame with selected columns."""
    return pd.DataFrame({
        'lectureCode': df['lectureCode'],
        'year': df['lectureReview'].apply(lambda x: x['year']),
        'semester': df['lectureReview'].apply(lambda x: x['semester']),
        'content': df['lectureReview'].apply(lambda x: x['content']),
        'rate': df['lectureReview'].apply(lambda x: x['rate'])
    })

def group_lectures(df: pd.DataFrame) -> pd.DataFrame:
    """Group lectures by lectureCode and combine all reviews."""
    return df.groupby('lectureCode')['content'].apply(lambda x: ' '.join(x)).reset_index()