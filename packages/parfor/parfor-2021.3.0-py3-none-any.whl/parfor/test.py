from time import sleep
from parfor import parfor
import numpy as np


def my_fun(*args, **kwargs):
    @parfor(range(10), (3,), length=10)
    def fun(i, a):
        sleep(np.random.randint(1, 60))
        assert False
        return a * i ** 2

    return fun


if __name__ == '__main__':
    print(my_fun())