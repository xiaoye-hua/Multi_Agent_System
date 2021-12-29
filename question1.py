# -*- coding: utf-8 -*-
# @File    : question1.py
# @Author  : Hua Guo
# @Disc    :
from tqdm import tqdm
import numpy as np
import pandas as pd

# config

house_num = 1000
similation_number = 10000
visited_threshold = 5000
preference_threshold = 0.8

final_preference_lst = []
for _ in tqdm(range(similation_number)):
    preference_lst = np.random.random(house_num)
    final_preference = None
    # print(preference_lst[-3:])
    for idx, x in enumerate(preference_lst):
        if idx >= visited_threshold and x>=preference_threshold:
            final_preference = x
            break
    if final_preference is None:
        final_preference = preference_lst[-1]
    final_preference_lst.append(final_preference)
def get_stats(lst):
    res = {}
    res['mean'] = np.mean(lst)
    res['min'] = np.min(lst)
    res['max'] = np.max(lst)
    return res

df = {}
lst_lst = [final_preference_lst]
lst_name = ['final_preference']

for name, lst in zip(lst_name, lst_lst):
    stats = get_stats(lst)
    df[name] = stats
df = pd.DataFrame(df).T
print(f"similation num: {similation_number}; visited house: {visited_threshold}; pereference threshold: {preference_threshold}")
print(df)




