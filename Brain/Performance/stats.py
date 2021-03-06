import numpy as np

from Brain.Performance.random_matrix import RandomMatrix

def expectation(a):
    return np.sum(a)/a.size


def cov(a, b):
    return expectation(a*b) - expectation(a)*expectation(b)

if __name__ == '__main__':
    a = RandomMatrix(500, 500, 0.4)
    print(cov(a[0:200], a[200:400]))
    #print(RandomMatrix(100, 100, 0.5).values)
