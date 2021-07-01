def fact(n):
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f


# 재귀함수
def fact_2(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)


if __name__ == '__main__':
    print(fact(1))
    print(fact(10))
    print(fact_2(1))
    print(fact_2(10))
