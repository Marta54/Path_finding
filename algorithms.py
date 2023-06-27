from queue import PriorityQueue
import heapq
from collections import deque
import pygame

def h(p1,p2):
    # Manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    # came_from: dictionary where key are the neogbours and the values the node from which we came
    size = 0
    while current in came_from:
        current = came_from[current]
        size += 1
        current.make_path()
        draw()

    return size


def A_star(draw, grid, start, end):
    count = 0 
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # node
        open_set_hash.remove(current)

        if current == end:
            # make path
            size = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True, size

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()

        if current != start:
            current.make_closed()
        
    return False, None


def Dijkstra(draw, grid, start, end):
    n = len(grid)
    distances = [[float("inf")] * n for _ in range(n)]
    distances[start.get_pos()[0]][start.get_pos()[1]] = 0
    visited = set()
    queue = [(0, start)]
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_distance, current = heapq.heappop(queue)
        
        if current == end:
            # come back here in the end
            size = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()

            return True, size
        
        visited.add(current)

        for neighbour in current.neighbours:
            loc = neighbour.get_pos()
            
            neighbour.make_closed()
            end.make_end()
            start.make_start()

            if neighbour not in visited:
                neighbour.make_open()
                distance = current_distance + 1 
                if distance < distances[loc[0]][loc[1]]:
                    came_from[neighbour] = current
                    distances[loc[0]][loc[1]] = distance
                    heapq.heappush(queue,(distance, neighbour))
        draw()
    return False, None

def bfs(draw, grid, start, end):
    visited = set([start])    
    queue = deque([start])
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = queue.popleft()

        if current_node == end:
            size = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True, size

        # visited.add(current_node)

        nodes = current_node.neighbours
        for neighbour in nodes:
            neighbour.make_closed()
            end.make_end()
            start.make_start()

            if neighbour not in visited:
                neighbour.make_open()
                queue.append(neighbour)
                visited.add(neighbour)
                came_from[neighbour] = current_node

        draw()

    return False, None

def dfs(draw, grid, start, end):
    stack = [start]
    visited = set([start])
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = stack.pop()
    
        if current == end:
            size = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()

            return True, size

        for neighbour in current.neighbours:
            current.reset()
            neighbour.make_closed()
            end.make_end()
            start.make_start()

            if neighbour not in visited:
                neighbour.make_open()
                stack.append(neighbour)
                visited.add(neighbour)
                came_from[neighbour] = current
        draw()

    return False, None
