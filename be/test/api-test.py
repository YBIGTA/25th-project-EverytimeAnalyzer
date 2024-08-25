from main import *

result = get_sims_by_topic("YCI1705-01-00", "강의가 재미있다. 학점이 후하다. 교수가 강의력이 좋다")
print(result)

result = get_recommend_lecture("YCI1705-01-00")
print(result)
