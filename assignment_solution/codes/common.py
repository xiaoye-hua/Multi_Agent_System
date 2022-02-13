# -*- coding: utf-8 -*-
# @File    : common.py
# @Author  : Hua Guo
# @Disc    :
from typing import List

import numpy as np


def calculate_confidence_interval(x_lst: List[float], confidence_level=0.99):
    sample_mean = np.mean(x_lst)
    sample_variance = np.sum([(x-sample_mean)**2 for x in x_lst])/(len(x_lst)-1)
    sample_mean_expectation = sample_mean
    sample_variance_expectation = sample_variance/len(x_lst)
    statistics = {
        0.99: 2.58
        , 0.95: 1.96
        , 0.90: 1.64
    }
    c = statistics[confidence_level]
    inc = c*np.sqrt(sample_variance_expectation)
    # print(inc)
    lower = round(sample_mean_expectation - inc, 3)
    upper = round(sample_mean_expectation + inc, 3)
    print(f"- Simulation num: {len(x_lst)}")
    print(f"- Mean value: {round(sample_mean_expectation, 3)}")
    print(f"- Confidence level: {confidence_level}")
    print(f"- Confidence Interval: [{lower}, {upper}]")