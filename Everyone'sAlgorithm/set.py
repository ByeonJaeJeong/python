# 빈집합 선언 방법 s=set() , 집합은 순서가 중요하지 않음
# len(s) 집합의 길이를 구함
# add(x) 집합에 자료x를 집어넣음
# discard(x) 집합에 자료 x가 들어있다면 삭제 합니다(없으면 변화 X)
# clear() 집합의 모든자료 삭제
# x in s  어떤 자료 x가 집합 s에 들어있는지 확인합니다.반대로 출력하는 (x not in s)

def find_same_name(a):
    n = len(a)  # 리스트의 자료 개수를 n에 저장
    result = set()  # 결과를 저장할 빈 집합
    for i in range(0, n - 1):  # 0 부터 n-2까지 반복
        for j in range(i + 1, n):  # i+1부터 n-1 까지 반복
            if a[i] == a[j]:  # 이름이 같으면
                result.add(a[i])  # 찾은 이름을 result 에 추가
    return result


if __name__ == '__main__':
    name = ["Tom", "Jerry", "Mike", "Tom"]  # 대소문자 유의 : 파이썬은 대소문자를 구분함0
    print(find_same_name(name))
