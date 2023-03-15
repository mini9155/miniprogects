from collections import deque

def solution(babbling):
    b = ["aya", "ye", "woo", "ma"] # 3,2,3,2 = 2,3,4,5,8,10
    #
    a = deque(babbling)

    for i in babbling:
        if b[0] in i:
            pass
        elif b[1] in i:
            pass
        elif b[2] in i:
            pass
        elif b



babbling = ["ayaye", "uuuma", "ye", "yemawoo", "ayaa"] # 5,5,2,7,3
print(solution(babbling))