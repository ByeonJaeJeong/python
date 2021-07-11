# 선택정렬 알고리즘

# 배열중에 제일 작은수의 인덱스를 구하는 알고리즘
def find_min_idx(a):
    n = len(a)
    min_idx = 0
    for i in range(1, n):
        if a[i] < a[min_idx]:
            min_idx = i
    return min_idx


def sel_sort(a):
    result = []
    while a:
        min_idx = find_min_idx(a)
        value = a.pop(min_idx)
        result.append(value)
    return result


def sel_sort2(a):
    n = len(a)
    for i in range(0, n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
            # 찾은 최소값을 i위치로
        a[i], a[min_idx] = a[min_idx], a[i]


if __name__ == '__main__':
    d = [2, 4, 5, 1, 3]
    print(sel_sort(d))
    d = [2, 4, 5, 1, 3]
    sel_sort2(d)
    print(d)
