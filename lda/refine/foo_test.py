import pandas as pd
from konlpy.tag import Okt
from _collections import defaultdict
from refine_func import *

data = pd.read_csv("../data/temp.csv")
data.reset_index(inplace=True)

reviewList = data['review'].tolist()
extract_pos(reviewList, 'Noun')
