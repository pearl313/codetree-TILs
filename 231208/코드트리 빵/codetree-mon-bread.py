import sys
input = sys.stdin.readline
from collections import deque

# 인접한 4방향 (우선순위 : 상 좌 우 하)
dxy = [(-1, 0), (0, -1), (0, 1), (1, 0)]

# 범위 안에 드는 지 확인하는 함수
def possible(x, y):
    return 0 <= x < n and 0 <= y < n

# 편의점으로 이동하는 함수
def move_to_store():
    # 격자 위에 사람이 존재한다면, 그 위치에서 본인이 가고 싶어하는 편의점까지의 최단 거리 구하기
    for i in range(len(people)):
        # 편의점에서 해당 베이스캠프까지의 거리를 구하고, 가장 최단 거리인 방향으로 1칸 움직이기
        x = where_store[i][0] - 1
        y = where_store[i][1] - 1
        # 이미 도착했으면 이동하지 않기
        if visited[x][y]:
            continue
        dist_to_base = [[-1] * n for _ in range(n)]
        dist_to_base[x][y] = 0
        q = deque()
        q.append((x, y))
        while q:
            cur_x, cur_y = q.popleft()
            for dx, dy in dxy:
                nx, ny = cur_x + dx, cur_y + dy
                if not possible(nx, ny):
                    continue
                if visited[nx][ny]:
                    continue
                if dist_to_base[nx][ny] != - 1:
                    continue
                dist_to_base[nx][ny] = dist_to_base[cur_x][cur_y] + 1
                q.append((nx, ny))

        min_v = 1e10
        can_go = []
        for dx, dy in dxy:
            nx, ny = people[i][0] + dx, people[i][1] + dy
            if not possible(nx, ny):
                continue
            if visited[nx][ny]:
                continue
            if dist_to_base[nx][ny] == -1:
                continue
            if min_v > dist_to_base[nx][ny]:
                min_v = dist_to_base[nx][ny]
                can_go.append((dist_to_base[nx][ny], nx, ny))

        can_go = sorted(can_go, key=lambda x:x[0])
        # 1칸 이동
        people[i][0] = can_go[0][1]
        people[i][1] = can_go[0][2]

    check_visited()

# 해당 칸을 지날 수 없도록 체크해두는 함수
def check_visited():
    # 각자 원하는 편의점에 도착했다면, 이동하지 못하도록 체크 처리하기
    for i in range(len(people)):
        x = where_store[i][0] - 1
        y = where_store[i][1] - 1
        if people[i][0] == x and people[i][1] == y:
            visited[x][y] = True


# 베이스캠프로 이동하는 함수
def move_to_base():
    # 자신이 가고 싶어하는 편의점과 가장 가까운 베이스캠프 찾기
    start_x, start_y = where_store[time - 1][0] - 1, where_store[time - 1][1] - 1
    dist_to_base = [[-1] * n for _ in range(n)]
    dist_to_base[start_x][start_y] = 0
    q = deque()
    q.append((start_x, start_y))
    base_ls = []
    while q:
        cur_x, cur_y = q.popleft()
        for dx, dy in dxy:
            nx, ny = cur_x + dx, cur_y + dy
            if not possible(nx, ny):
                continue
            if visited[nx][ny]:
                continue
            if dist_to_base[nx][ny] != - 1:
                continue
            dist_to_base[nx][ny] = dist_to_base[cur_x][cur_y] + 1
            q.append((nx, ny))
            if board[nx][ny] == 1:
                base_ls.append((dist_to_base[nx][ny], nx, ny))
    # 최단거리이면서, 행이 작고, 열이 작은 베이스캠프로 이동
    base_ls = sorted(base_ls, key=lambda x:(x[0], x[1], x[2]))
    people.append([base_ls[0][1], base_ls[0][2]])
    # 다른 사람이 지나갈 수 없도록 체크해두기
    visited[base_ls[0][1]][base_ls[0][2]] = True


# 모두 도착했는지 확인하는 함수
def check_arrive():
    for i in range(m):
        x = where_store[i][0] - 1
        y = where_store[i][1] - 1
        if people[i][0] != x or people[i][1] != y:
            return False
    return True

n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
where_store = [list(map(int, input().split())) for _ in range(m)]
time = 0
people = []
visited = [[False] * n for _ in range(n)]

while True:
    time += 1

    # 격자 내에 사람이 있다면, 각자 가고 싶은 편의점으로 1칸 씩 이동
    if people:
        move_to_store()

    # 현재 시간 time이 m 이하인 경우, time 번 사람이 가고싶은 편의점과 가장 가까운 베이스 캠프로 이동
    if time <= m:
        move_to_base()

    # 모두 편의점에 도착했는지 확인
    if len(people) == m:
        if check_arrive():
            break
print(time)