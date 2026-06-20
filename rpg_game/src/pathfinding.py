import heapq
from src.constants import DIRECTIONS

#A*寻路：g=已走步数 h=曼哈顿距离 f=g+h
def astar(start, goal, game_map, blocked_positions):
    goal_x, goal_y = goal
    if not game_map.is_walkable(goal_x, goal_y):
        return []
    open_set=[]
    heapq.heappush(open_set, (0,0,start,None))
    visited={}
    while open_set:
        f,g,current,parent = heapq.heappop(open_set)
        if current in visited:
            continue
        visited[current]=(g,parent)
        if current == goal:
            path=[]
            node = current
            while node != start:
                path.append(node)
                node = visited[node][1]
            path.reverse()
            return path
        cx,cy=current
        for (dx,dy) in DIRECTIONS:
            nx,ny=cx+dx,cy+dy
            neighbor=(nx,ny)
            if neighbor in visited or not game_map.is_walkable(nx, ny) or (neighbor in blocked_positions and neighbor != goal):
                continue
            new_g = g+1
            h = abs(nx - goal_x) + abs(ny - goal_y)
            new_f = new_g+h
            heapq.heappush(open_set, (new_f,new_g, neighbor, current))
    return []
