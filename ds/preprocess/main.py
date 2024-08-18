import os
import json
import pandas as pd
from data_processing import load_json, save_to_csv, prepare_dataframe, group_lectures
from text_processing import split_sentences, normalize_text
from embedding import load_model, generate_embeddings

def process_reviews(input_json: str, output_json: str) -> None:
    # json 파일로부터 데이터를 불러와서 강의별로 그룹화
    df = load_json(input_json)
    df = prepare_dataframe(df)
    df = group_lectures(df)
    
    # 문장 단위로 분리 및 전처리
    df['content_split'] = df['content'].apply(lambda x: split_sentences([x]))
    df['content_normalized'] = df['content_split'].apply(
        lambda sentences: [normalize_text(sentence) for sentence in sentences]
    )
    
    # 문장별 embedding vector 생성
    model = load_model()
    df['sentence_embeddings'] = df['content_normalized'].apply(
        lambda sentences: generate_embeddings(model, sentences)
    )
    
    # 저장
    result = df.to_dict(orient='records')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_json_path = os.path.join(os.path.dirname(__file__), '../data/sample.json')
    output_json_path = os.path.join(os.path.dirname(__file__), '../data/output.json')

    process_reviews(input_json_path, output_json_path)