from collections import deque

def solution(babbling):
    o = ["aya", "ye", "woo", "ma"] # 1 2 3 4
    A = deque(babbling)
    A_pop = A.popleft()
    result = 0
    
    for a in range(0,4):
        for b in range(0,4):
            if A_pop == o[a]:
                result += 1
                A_pop = A.popleft()
                a, b = 0, 0
                break
            elif o[a] != o[b]:
                words = o[a] + o[b]
                if words == A_pop:
                    result += 1
                    A_pop = A.popleft()
                    a, b = 0, 0



babbling = ["ayaye", "uuuma", "ye", "yemawoo", "ayaa"]
print(solution(babbling))