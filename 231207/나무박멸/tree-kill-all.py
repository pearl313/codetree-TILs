from collections import deque

# 인접한 4방향 (상하좌우)
dxy_1 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# 대각선 4방향
dxy_2 = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

# 범위 안에 드는 지 확인하는 함수
def possible(x, y):
    return 0 <= x < n and 0 <= y < n

def where_tree():
    global q, done_board
    # 나무가 있는 위치 찾아서 저장하기
    for i in range(n):
        for j in range(n):
            if done_board[i][j] >= 1:
                q.append((i, j))

# 나무 성장 함수
def growth():
    global q, can_breed
    # 나무 위치 찾기
    where_tree()
    # 인접한 4방향 확인 후 나무 성장
    while q:
        cur_x, cur_y = q.popleft()
        cnt = 0
        for dx, dy in dxy_1:
            nx, ny = cur_x + dx, cur_y + dy
            if not possible(nx, ny):
                continue
            if done_board[nx][ny] < 0:
                continue
            if done_board[nx][ny] == 0:
                can_breed[cur_x][cur_y] += 1
                continue
            cnt += 1
        ing_board[cur_x][cur_y] += cnt

# 나무 번식 함수
def breeding():
    global q, ing_board
    # 나무 위치 찾기
    where_tree()
    while q:
        cur_x, cur_y = q.popleft()
        for dx, dy in dxy_1:
            nx, ny = cur_x + dx, cur_y + dy
            if not possible(nx, ny):
                continue
            if done_board[nx][ny] < 0:
                continue
            if done_board[nx][ny] > 0:
                continue
            ing_board[nx][ny] += ing_board[cur_x][cur_y] // can_breed[cur_x][cur_y]


# 제초제 뿌릴 위치 선정하는 함수
def find_point():
    global can_dead, where, dead_trees
    for i in range(n):
        for j in range(n):
            if ing_board[i][j] > 0:
                cur_x, cur_y = i, j
                for dx, dy in dxy_2:
                    no = []
                    for f in range(1, k + 1):
                        nx = cur_x + dx * f
                        ny = cur_y + dy * f
                        if no and (dx, dy) in no:
                            continue
                        if not possible(nx, ny):
                            continue
                        if ing_board[nx][ny] <= 0:
                            no.append((dx, dy))
                            continue
                        can_dead[cur_x][cur_y] += ing_board[nx][ny]
    
    max_val = 0
    x, y = 0, 0
    for i in range(n):
        for j in range(n):
            if max_val == can_dead[i][j]:
                continue
            elif max_val < can_dead[i][j]:
                max_val = can_dead[i][j]
                x, y = i, j
    dead_trees += max_val
    spread_dead(x, y)


# 제초제 뿌린 후에 박멸하는 함수
def spread_dead(x, y):
    global drug, done_board
    # 1년 지난 거 체크하기
    for i in range(n):
        for j in range(n):
            if drug[i][j] > 0:
                drug[i][j] -= 1
                if drug[i][j] == 0:
                    ing_board[i][j] = 0
    # 제초제 뿌려주기
    drug[x][y] = c
    ing_board[x][y] = -2
    for dx, dy in dxy_2:
            no = []
            for f in range(1, k + 1):
                nx = x + dx * f
                ny = y + dy * f
                if no and (dx, dy) in no:
                    continue
                if not possible(nx, ny):
                    continue
                if ing_board[nx][ny] <= 0:
                    no.append((dx, dy))
                    if ing_board[nx][ny] == -1:
                        continue
                ing_board[nx][ny] = -2
                drug[nx][ny] = c

n, m, k, c = map(int, input().split())
done_board = [list(map(int, input().split())) for _ in range(n)]
ing_board = [i[:] for i in done_board]
q = deque()
where = []
drug = [[0] * n for _ in range(n)]
dead_trees = 0
for _ in range(m):
    can_breed = [[0] * n for _ in range(n)]
    # 성장
    growth()
    # 번식
    breeding()
    can_dead = [i[:] for i in ing_board]
    # 제초제 위치 선정
    x, y = 0, 0
    find_point()
    done_board = [i[:] for i in ing_board]
print(dead_trees)