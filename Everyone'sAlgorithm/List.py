# List  a=[5,7,9] 대괄호 안에 쉼표로 구분하여 적어주면 사용가능
# len(List) 리스트 길이(자료 개수) 를 구함 len(a) =>return 3
# append(x) 자료 x를 리스트이 맨 뒤에 추가함 a.append(4) => a=[5,7,9,4]
# insert(i,x) 리스트의 i 번 위치에 x를 추가함
# pop(i) i번 위치에 있는 자료를 리스트에서 빼내면서 그값을 함수의 결괏값으로 돌려줌 i를 지정하지 않을시 마지막값을 빼서 돌려줌
# clear() 리스트의 모든 자료를 지움
# x in a 어떤 자료 x가 리스트 a안에 있는지 확인(반대값인 x not in a)도 있음

def find_max(a):  # O(n)
    n = len(a)  # 입력크기 n
    max_v = a[0]  # 리스트의 첫번째 값을 최댓값으로 기억
    for i in range(1, n):  # 1투터 n-1까지 반복
        if a[i] > max_v:  # 이번 값이 현재까지 기억된 최댓값보다 크면
            max_v = a[i]  # 최댓값 변경
    return max_v


def find_max_idx(a):
    n = len(a)  # 입력크기
    max_idx = 0  # 최대값이 있는 위치
    for i in range(n):
        if a[i] > a[max_idx]:  # 이번값이 최댓값보다크면
            max_idx = i  # 최댓값 위치변경
    return max_idx


def find_min(a):
    n = len(a)
    min_v = a[0]
    for data in a:
        if data < min_v:
            min_v = data
    return min_v


if __name__ == '__main__':
    v = [17, 92, 18, 33, 58, 7, 33, 42]
    print(find_max(v))
    print(find_max_idx(v))
    print(find_min(v))

