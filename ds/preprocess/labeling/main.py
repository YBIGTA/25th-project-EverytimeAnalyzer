import os
import pandas as pd
from select_dataset import process_flag_sentences, process_review_sentences, calculate_distance_matrix, select_min_distance, select_1000_sentences

def main():
    # flag 문장들 전처리 및 embedding vector 생성
    flag_sentences = process_flag_sentences('flag_sentences.txt', 'flag_sentences_embedding.csv')
    
    # 강의평 문장들 호출
    review_file_path = os.path.join(os.path.dirname(__file__), '../../data/embedding_formatted.json')
    review_sentences = process_review_sentences(review_file_path)
    
    # 강의평 문장들과 flag 문장들 간의 manhattan distance 계산
    distance_matrix = calculate_distance_matrix(review_sentences, flag_sentences)

    # 강의평 문장들의 토픽별 유사도 계산 (토픽별 5개 문장과의 유사도 중 가장 작은 값 선택)
    min_distance_matrix = select_min_distance(distance_matrix)

    # 각 토픽별로 200개씩 총 1000개의 문장 선택
    selected_sentences = select_1000_sentences(min_distance_matrix, 'train_dataset.csv')


if __name__ == '__main__':
    main()