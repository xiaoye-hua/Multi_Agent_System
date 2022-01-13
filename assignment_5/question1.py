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
visited_threshold = 0.2
preference_threshold = 0.8

final_preference_lst = []
best_choice = []
method  = 2
c_param =0.1

if method == 1:
    for _ in tqdm(range(similation_number)):
        preference_lst = np.random.random(house_num)
        final_preference = None
        # print(preference_lst[-3:])
        for idx, x in enumerate(preference_lst):
            if x>=preference_threshold:
                final_preference = x
                break
        if final_preference is None:
            final_preference = preference_lst[-1]
        final_preference_lst.append(final_preference)
elif method == 2:
    for _ in tqdm(range(similation_number)):
        preference_lst = np.random.random(house_num)
        final_preference = None
        # print(preference_lst[-3:])
        max_x = 0
        for idx, x in enumerate(preference_lst):
            if x> max_x:
                max_x = x
            if idx >= visited_threshold*house_num and x >=max_x:
                final_preference = x
                break
        if final_preference is None:
            final_preference = preference_lst[-1]
        if final_preference == preference_lst.max():
            best_choice.append(1)
        else:
            best_choice.append(0)
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
print("Probability of choose best house",np.mean(best_choice))
print(f"similation num: {similation_number}; visited house: {visited_threshold*house_num}; pereference threshold: {preference_threshold}")

print(df)




