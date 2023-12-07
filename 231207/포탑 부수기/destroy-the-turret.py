from collections import deque

def set_attacker():
    min_attack = 5001
    set_i, set_j = 0, 0
    for i in range(n):
        for j in range(m):
            if board[i][j] == 0:
                continue

            if board[i][j] < min_attack:
                min_attack = board[i][j]
                set_i, set_j = i, j
            elif board[i][j] == min_attack:
                if attack_time[i][j] > attack_time[set_i][set_j]:
                    set_i, set_j = i, j
                elif attack_time[i][j] == attack_time[set_i][set_j]:
                    if i + j > set_i + set_j:
                        set_i, set_j = i, j
                    elif i + j == set_i + set_j:
                        if j > set_j:
                            set_i, set_j = i, j

    board[set_i][set_j] += n + m
    return board[set_i][set_j], set_i, set_j


def set_target():
    max_attack = -1
    set_i, set_j = 0, 0
    for i in range(n):
        for j in range(m):
            if board[i][j] == 0:
                continue
            if i == attacker_i and j == attacker_j:
                continue

            if board[i][j] > max_attack:
                max_attack = board[i][j]
                set_i, set_j = i, j
            elif board[i][j] == max_attack:
                if attack_time[i][j] < attack_time[set_i][set_j]:
                    set_i, set_j = i, j
                elif attack_time[i][j] == attack_time[set_i][set_j]:
                    if i + j < set_i + set_j:
                        set_i, set_j = i, j
                    elif i + j == set_i + set_j:
                        if j < set_j:
                            set_i, set_j = i, j
    return set_i, set_j

def laser_attack(i, j):
    di = [0, 1, 0, -1]
    dj = [1, 0, -1, 0]
    visited = [[False] * m for _ in range(n)]
    visited[i][j] = True
    queue = deque()
    queue.append((i, j, []))
    while queue:
        i, j, route = queue.popleft()

        for direction in range(4):
            ni, nj = (i + di[direction]) % n, (j + dj[direction]) % m
            if ni == target_i and nj == target_j:
                board[target_i][target_j] -= attack_point
                for att_i, att_j in route:
                    board[att_i][att_j] -= attack_point // 2
                    attack_status[att_i][att_j] = True
                return True

            if not visited[ni][nj] and board[ni][nj] != 0:
                visited[ni][nj] = True
                temp = route[:]
                temp.append((ni, nj))
                queue.append((ni, nj, temp))

    return False

def cannon_attack(i, j):
    ci = [1, 1, -1, -1, 0, 1, 0, -1]
    cj = [1, -1, 1, -1, 1, 0, -1, 0]
    board[i][j] -= attack_point
    for direction in range(8):
        cannon_i, cannon_j = (i + ci[direction]) % n, (j + cj[direction]) % m
        if cannon_i == attacker_i and cannon_j == attacker_j:
            continue
        attack_status[cannon_i][cannon_j] = True
        board[cannon_i][cannon_j] -= attack_point // 2

def check_under_zero():
    for i in range(n):
        for j in range(m):
            if board[i][j] < 0:
                board[i][j] = 0

def recover():
    check = []
    count = 0
    for i in range(n):
        for j in range(m):
            if board[i][j] != 0 and not attack_status[i][j]:
                board[i][j] += 1
            
def can_attack_anyone():
    count = 0
    for i in range(n):
        for j in range(m):
            if board[i][j] != 0:
                count += 1
    
    if count == 1:
        return False
    return True


n, m, k = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
attack_time = [[0] * m for _ in range(n)]

for turn in range(1, k + 1):
    attack_status = [[False] * m for _ in range(n)]
    attack_point, attacker_i, attacker_j = set_attacker()
    target_i, target_j = set_target()
    attack_time[attacker_i][attacker_j] = turn
    attack_status[attacker_i][attacker_j] = True
    attack_status[target_i][target_j] = True
    if not laser_attack(attacker_i, attacker_j):
        cannon_attack(target_i, target_j)
    check_under_zero()
    recover()
    if not can_attack_anyone():
        break
print(max([max(_) for _ in board]))

'''
4 4 3
6 8 0 1
0 0 0 0
0 0 0 0
0 0 8 0

5 10 704
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2186
0 0 0 0 4346 0 0 0 0 0
0 0 0 0 3889 3148 1500 0 0 0
0 3440 0 0 17 0 0 0 0 0
'''