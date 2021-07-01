# 최대 공약수 구하기

def gcd(a, b):
    i = min(a, b)
    while True:
        if a % i == 0 and b % i == 0:
            return i
        i = i - 1


# 유클리드 방식 : a와 b의 최대공약수는 b와 a를 b로 나눈 나머지의 최대공약수와 같음 즉, gcd(a,b) = gcd(b, a% b) 와 같음
# 어떤수와 0 의 최대공약수는 자기 자신 즉, gcd(n, 0) = n
def gcd_2(a, b):
    if b == 0:
        return a
    return gcd_2(b, a % b)


if __name__ == '__main__':
    print(gcd(1, 5))
    print(gcd(60, 24))
    print(gcd_2(1, 5))
    print(gcd_2(60, 24))
