# Question 2

1. Refer to [assignment_main.py](assignment_5/question2.py) for main code
2. Refer to [log](assignment_5/log) for raw result


# Question 1


Strategy

1. Once x is bigger than n, then rent the place
    1. n=0.5
    2. n=0.8
    2. n=0.9
2. After visited n1 houses, once x is bigger than n2, then rent the place
    1. n1=1/3 of total house num, n2=0.5
    2. n1=1/2 of total house num, n2=0.8
    
 *******
 ### Result
 # Question 1

similation num: 10000; visited house: 0; pereference threshold: 0.5
                       max      mean       min
final_preference  0.999997  0.748692  0.500046

similation num: 10000; visited house: 0; pereference threshold: 0.8
                      max      mean      min
final_preference  0.99999  0.900533  0.80006

similation num: 10000; visited house: 0; pereference threshold: 0.9
                       max      mean       min
final_preference  0.999992  0.950007  0.900023




Probability of choose best house 0.335
similation num: 10000; visited house: 200.0; pereference threshold: 0.8
                  max      mean       min
final_preference  1.0  0.899398  0.000803

Probability of choose best house 0.3623
similation num: 10000; visited house: 300.0; pereference threshold: 0.8
                  max      mean     min
final_preference  1.0  0.848718  0.0003
Probability of choose best house 0.3708

similation num: 10000; visited house: 350.0; pereference threshold: 0.8
                  max      mean       min
final_preference  1.0  0.826265  0.000076

Probability of choose best house 0.3725
similation num: 10000; visited house: 370.0; pereference threshold: 0.8
                  max      mean       min
final_preference  1.0  0.813979  0.000428

Probability of choose best house 0.3632
similation num: 10000; visited house: 400.0; pereference threshold: 0.8
                  max      mean       min
final_preference  1.0  0.796998  0.000244
    
# Question 3


1. [mc result](assignment_5/result/mc_multi_threads/)
2. [Q learning result](assignment_5/result/q_learning)
3. [sarsa result](assignment_5/result/sarsa)
