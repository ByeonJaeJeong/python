# 병합정렬

def merge_sort(a):
    n = len(a)

    if n <= 1:
        return a
    mid = n // 2

    g1 = merge_sort(a[:mid])  # 재귀호출로 첫번째 그룹을 정렬
    g2 = merge_sort(a[mid:])  # 재귀호출로 두번째 그룹을 정렬

    # 두그룹을 하나로 병합
    result = []
    while g1 and g2:
        if (g1[0] < g2[0]):
            # g1값이 더 작으면 그값을 빼내어 결과로 추가
            result.append(g1.pop(0))
        else:
            # g2값이 더작으면 그값을 빼내어 결과로 추가
            result.append(g2.pop(0))
    # 아직 남아 있는 자료들을 결과에 추가
    # g1과 g2중 이미 빈것은 while을 바로지나감
    while g1:
        result.append(g1.pop(0))
    while g2:
        result.append(g2.pop(0))
    return result


if __name__ == '__main__':
    d = [6, 2, 4, 5, 9, 8, 1, 3, 7, 10]
    print(merge_sort(d))
