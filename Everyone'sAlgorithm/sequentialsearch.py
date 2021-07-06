def search_list(a, x):
    n = len(a)
    for i in range(0, n):
        if x == a[i]:
            return i

    return -1


v = [17, 92, 18, 33, 58, 7, 33, 42]
print(search_list(v, 18))
print(search_list(v, 33))
print(search_list(v, 500))


# search_list에서 검색 위치 결과를 목록으로 보여주는 알고리즘
def search_list_menus(a, x):
    value = []
    n = len(a)
    for i in range(0, n):
        if x == a[i]:
            value.append(i)
    return value


print(search_list_menus(v, 33))
print(search_list_menus(v, 500))


# 학생 번호와 이름이 리스트로 주어졌을때 학생 번호를 입력하면 학생번호에 해당하는 이름을 순차 탐색으로 찾아 돌려주는 함수
def search_scList(num_List, name_List, input_Number):
    n= len(num_List)
    for i in range(0,n):
        if input_Number== num_List[i]:
            return name_List[i]
    return "?"



stu_no = [39, 14, 67, 105]
stu_name = ["justin", "John", "Mike", "Summer"]
print(search_scList(stu_no, stu_name, 39))
print(search_scList(stu_no, stu_name, 14))
print(search_scList(stu_no, stu_name, 500))
