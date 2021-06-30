import math

def sum_n(n):   # 시간복잡도 O(n)
    s=0
    for i in range(1,n+1):
        s= s+i
    return s
def sum_n_2(n):   #시간복잡도 O(1)
    return n * (n+1) //2
if __name__== "__main__":
    print(sum_n(100))
    print(sum_n_2(100))

