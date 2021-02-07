from collections import deque

#내정답
def solution(phone_book):
    phone_book.sort(key=len) #적은것을 메인으로 하기위해 정렬
    print(phone_book)
    for i, value in enumerate(phone_book):
        for j in range(len(phone_book)):
            if i == j :
                print("패스")
                continue
            if phone_book[j].startswith(value):   #startswith 괄호안의 문자열로 시작하는지 여부 확인
                print("진입")
                return False
    return True
    #프로그래머스 추천 정답
    def best_solution(phoneBook):
        phoneBook = sorted(phoneBook)

        for p1, p2 in zip(phoneBook, phoneBook[1:]):
            if p2.startswith(p1):
                return False
        return True

    return answer
#정석 대로의  해쉬 풀이

def hash_solution(phone_book):
    answer = True   #기본값
    hash_map = {}   #헤쉬맵 선언
    for phone_number in phone_book:
        hash_map[phone_number] = 1
    for phone_number in phone_book:
        temp = ""
        for number in phone_number:
            temp += number
            if temp in hash_map and temp != phone_number:
                answer = False
    return answer
if __name__== "__main__":
    phone_books=	[["123","456","789"],["119", "97674223", "1195524421"],["12","123","1235","567","88"]]
    for phone_book in phone_books:
        #print(phone_book)
        #print(solution(phone_book))
        print(hash_solution(phone_book))