import math


def squared_n(n):
    s = 0
    for i in range(1, n + 1):
        s += (i * i)
    return s


def squared_n_2(n):
    return (n * (n + 1) * (2 * n + 1)) // 6


if __name__ == '__main__':
    print(squared_n(10))
    print(squared_n_2(10))
