from MongoRepository import MongoRepository
from env import load_env_vars

# 반환값 확인용으로 작성
# 마지막줄에 breakpoint 걸어놓고 봐보세요.

env_vars = load_env_vars()
repo = MongoRepository(env_vars["host"], env_vars["port"], env_vars["username"], env_vars["pw"])

lecture = repo.find_lecture_info("UCE1105-01-00")
reviews = repo.find_reviews("UCE1105-01-00")
syllabus = repo.find_syllabus("UCE1105-01-00")

print()
