from LlamaClient import LlamaClient
from MongoRepository import MongoRepository
from env import load_env_vars

if __name__ == "__main__":
    env_vars = load_env_vars()
    repo = MongoRepository(env_vars["host"], env_vars["port"], env_vars["username"], env_vars["pw"])

    # api 토큰 넣어주십쇼~
    client = LlamaClient(None, "./config/config.json")

    lecture = repo.find_lecture_info("UCE1105-01-00")
    reviews = repo.find_reviews("ATM4105-01-00")
    syllabus = repo.find_syllabus("UCE1105-01-00")

    result = client.request(lecture, reviews, syllabus)
    print()
