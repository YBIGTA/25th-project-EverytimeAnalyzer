## Everytime Analyzer: 에브리타임 강의평 기반 강의 추천 시스템
(프로젝트 개요)

### Architecture
(플로우차트 사진이랑 각 단계별 설명)

### Repository Structure
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

### Team
|박준형|박지은|최서영|홍규원|
|:---:|:---:|:---:|:---:|
|<img src="https://avatars.githubusercontent.com/u/147307286?v=4" width="120" height="120">|<img src="https://avatars.githubusercontent.com/u/97666193?v=4" width="120" height="120">|<img src="https://avatars.githubusercontent.com/u/175555303?v=4" width="120" height="120">|<img src="https://avatars.githubusercontent.com/u/155924433?v=4" width="120" height="120">|
|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/jsybf)](https://github.com/jsybf)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/iamzieun)](https://github.com/iamzieun)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/choi613504)](https://github.com/choi613504)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/kkyu0215)](https://github.com/kkyu0215)|