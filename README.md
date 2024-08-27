# 📚 Everytime Analyzer: 에브리타임 강의평 기반 강의 추천 시스템
Everytime Analyzer는 강의에 대한 학생들의 솔직한 평가가 담긴 에브리타임의 '강의평' 데이터와 연세포탈의 강의 개요 데이터를 기반으로, 사용자의 니즈에 부합하는 강의를 추천해주는 서비스입니다.

### Table of contents
1. [🛠️ Architecture](##-🛠️-Architecture)
2. [📂 Repository Structure](##-📂-Repository-Structure)
3. [👯 Team](##-👯-Team)

## 🛠️ Architecture
![image](https://github.com/YBIGTA/25th-project-EverytimeAnalyzer/blob/main/docs/flowchart.png)
### 1. Data Crawling
#### 1.1 에브리타임 강의평 데이터
에브리타임 강의평 데이터에는 로그인을 해야만 접근이 가능하다는 점을 고려하여, EC2에 selenium을 사용할 수 있는 환경을 구축하여 하루 500건 미만의 request를 통해 자동으로 데이터가 수집되도록 하였습니다.
#### 1.2 연세포탈 강의 개요 데이터
(내용)
### 2. Topic Modeling
강의평 데이터에 내재되어있을 것으로 기대되는 학생들이 강의를 평가하는 기준을 추출하고자 Latent Dirichlet Allocation (LDA) 알고리즘을 이용하여 강의를 분류하는 5개의 기준 (수업 내용, 로드, 교수님 강의스타일 및 강의력, 시험 출제 스타일, 학점) 을 추출하였습니다. 
### 3. Topic Classification
BERT 아키텍쳐를 한국어로 사전학습한 KoBERT 모델을 사용하여 강의평의 각 문장을 LDA로 추출한 5개의 토픽으로 분류하였습니다.
#### 3.1 Data Labeling
KoBERT를 fine-tuning하는데 사용할 학습 데이터를 만들기 위해, 각 토픽별로 5개의 flag sentence를 만들고, 총 25개의 flag sentence와의 코사인 유사도를 바탕으로 5000개의 강의평 문장을 추출하였습니다. 마지막으로 추출된 5000개의 문장에 대해 gpt 3.5 turbo api를 사용하여 라벨을 부여한 후, 중복 제거 및 맞춤법 교정 등의 전처리를 거쳐 약 4000여 개의 데이터를 학습 데이터셋으로 사용하였습니다. 
#### 3.2 Fine-tuning
Training loss와 Validation loss의 추이에 따라, 3 epoch의 fine-tuning을 진행했습니다. 
#### 3.3 Inference
fine-tuning을 마친 KoBERT 모델로, 전체 7만여 개의 강의평 문장의 토픽을 분류했습니다. 
### 4. Loading Data into VectorDB
각각의 강의평 문장을 강의와 토픽으로 그룹화하여 chroma에 적재하였습니다. 강의평 문장 단위로 적재하지 않고 강의와 토픽으로 강의평 문장들을 그룹화하여 적재함으로써, 추후 사용자 input과의 similarity search에 있어 보다 안정적인 결과값이 도출되도록 하였습니다. 
### 5. Summarization using LLM
Llama 3.1 70B API를 이용하여, 사용자의 input을 기반으로 추출된 5개의 추천 강의에 대한 강의 개요 및 강의평을 요약합니다.
### 6. User Interaction
backend는 FastAPI, frontend는 Vue를 이용하여, 사용자로부터 수강하고자 하는 강의에 대한 설명을 input으로 받아, 5개의 추천 강의와 각 강의의 강의 개요 및 강의평 요약 정보를 output으로 제공하는 파이프라인을 구축하였습니다. 

## 📂 Repository Structure
```bash
25th-project-EverytimeAnalyzer
├── be                                \\ backend, chroma, Llama API
│   └── load_data                     \\ load data to chroma collections
├── docs                              \\ presentation, flowchart image
├── ds                                \\ modeling
│   ├── data
│   ├── topic_modeling                \\ topic modeling: LDA
│   └── topic_classification          \\ topic classification: KoBERT
├── fe                                \\ frontend
└── scraping                          \\ crawling data from Yonsei portal and Everytime
```

## 👯 Team
|박준형|박지은|최서영|홍규원|
|:---:|:---:|:---:|:---:|
|<img src="https://avatars.githubusercontent.com/u/147307286?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/97666193?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/175555303?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/155924433?v=4" width="150" height="150">|
|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/jsybf)](https://github.com/jsybf)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/iamzieun)](https://github.com/iamzieun)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/choi613504)](https://github.com/choi613504)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/kkyu0215)](https://github.com/kkyu0215)|