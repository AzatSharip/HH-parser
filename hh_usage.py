# -*- coding: utf-8 -*-
import pickle
import pandas as pd

# from collections import Counter
#
# with open(f'data.data', 'rb') as file:
#     data = pickle.load(file)
#     print(len(data))
#
# with open(f'links.data', 'rb') as file:
#     links = pickle.load(file)
#     print(f'Вакансий всего {len(links)}')

with open(f'df.data', 'rb') as file:
    df = pickle.load(file)
    print(df)




# counter = Counter(data)
# top = counter.most_common(1000)
# for t in top:
#     print(t)
