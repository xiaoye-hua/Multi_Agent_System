# Assignment 4
## TODO

1. [ ] p37


## 4. Monte Carlo Simulation
### 4.1 MC Sampling
#### Question 1

1. sample_num > 30 => we will use t statistic
2. we adopt confidence level of 0.99 =》t statistic=
3. Final result:
    1. Simulation num: 10000
    2. Mean value: 0.565
    3. Confidence level: 0.99
    4. Confidence Interval: [0.556, 0.574]
4. Refer to [4_1_MC_Sampling.py](codes/4_1_MC_Sampling.py) for detailed codes.
    
#### Question 2 ??

1. Hypothesis: 
    1. Null: there is no correlation between A and score
2. p-value & critical area
    1. significant level=95%
3. calculate p-value
4. compare p-value and 0.005

- Simulation num: 10000
- fraction of cofficient bigger than 0.3: 0.193
- 0.193>0.005 -> we can't refuse the null hypethesis.

### 4.2 Importance Sampling

### Question 1

- Simulation num: 10000
- Mean value: 1.0
- Confidence level: 0.99
- Confidence Interval: [0.973, 1.028]

#### Question 2

- Simulation num: 10000
- Mean value: 0.468
- Confidence level: 0.99
- Confidence Interval: [0.46, 0.476]


