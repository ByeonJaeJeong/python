# 해당 배열에서 수의크기가 몇번째 인지를 나타내는 함수
def find_ins_idx(r, v):
    for i in range(0, len(r)):
        if v < r[i]:
            return i
    return len(r)


# 삽입 정렬
def ins_sort(a):
    result = []
    while a:
        value = a.pop(0)
        ins_idx = find_ins_idx(result, value)
        result.insert(ins_idx, value)
    return result


def ins_sort_2(a):
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


if __name__ == '__main__':
    d = [2, 4, 5, 1, 3]
    print(ins_sort(d))
    # ins_sort 는 d를 비우고 return에 모든것을 삽입
    # 새로데이터를 넣은후
    d = [2, 4, 5, 1, 3]
    # 삽입정렬을 통해 정렬한후
    ins_sort_2(d)
    # 출력
    print(d)
# 삽입정렬의 계산복잡도는 O(n²)
