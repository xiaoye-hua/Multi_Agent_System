# -*- coding: utf-8 -*-
# @File    : 4_2_Importance_Sampling.py
# @Author  : Hua Guo
# @Disc    :
import numpy as np
from assignment_solution.codes.common import calculate_confidence_interval


def uniform_x(begin=-5, end=5) -> float:
    # begin = -5
    # end = 5
    interval = end - begin
    res = np.random.random()*interval+begin
    assert res>=begin and res<=end, res
    return res


def uniform_pdf(x, begin=-5, end=5):
    # begin = -5
    # end = 5
    return 1./(end-begin)


def norm_pdf(x):
    return 1/np.sqrt(2*np.pi)*np.exp(-x**2/2)


def question2_pdf(x):
    return (1+np.cos(np.pi*x)/2)


def sample_func(begin=-5, end=5, fx=norm_pdf) -> float:
    x = uniform_x(begin=begin, end=end)
    return x**2*fx(x=x)/uniform_pdf(x=x,begin=begin, end=end)


if __name__ == "__main__":
    # Question1 Config
    simulation_num = 10000
    simulation_res = [sample_func() for _ in range(simulation_num)]
    mean = np.mean(simulation_res)
    print('Question 1')
    # print(mean)
    calculate_confidence_interval(x_lst=simulation_res)

    # Question2 Config
    simulation_num = 10000
    begin = -1
    end = 1
    fx = question2_pdf
    simulation_res = [sample_func(begin=begin, end=end, fx=question2_pdf) for _ in range(simulation_num)]
    mean = np.mean(simulation_res)
    print('Question 2')
    calculate_confidence_interval(x_lst=simulation_res)


