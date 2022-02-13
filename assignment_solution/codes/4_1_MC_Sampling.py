# -*- coding: utf-8 -*-
# @File    : 4_1_MC_Sampling.py
# @Author  : Hua Guo
# @Disc    :
import numpy as np
from tqdm import tqdm

from assignment_solution.codes.common import calculate_confidence_interval


def mc_simulation():
    x = np.random.normal(loc=0.0, scale=1.0)
    return (np.cos(x))**2


if __name__ == "__main__":
    simulation_num = 10000
    confidence_level = 0.99
    simu_res = [mc_simulation() for _ in tqdm(range(simulation_num))]
    # print(np.mean(simu_res))
    print("Quesiton 1:")
    calculate_confidence_interval(x_lst=simu_res, confidence_level=confidence_level)

    # question 2
    from scipy import stats
    import numpy as np
    simulation_num = 10000
    n = 10
    threshold = 0.3
    slope_lst = []
    num = 0
    for _ in range(simulation_num):
        A = np.random.random(n)
        S = np.random.random(n)
        slope_0, intercept, r_value, p_value, std_err = stats.linregress(A, S)
        # print(slope_0)
        if slope_0 >= threshold:
            num += 1
    print("Question 2")
    print(f"- Simulation num: {simulation_num}")
    print(f'- fraction of cofficient bigger than 0.3: {round(float(num)/simulation_num, 3)}')