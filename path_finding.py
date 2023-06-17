import pygame
from queue import PriorityQueue

# create grid
WIN_WIDTH = 500
WIN_HEIGHT = 500

SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# colours
BARRIER = (0, 0, 0)        
BACKGROUND = (255, 255, 255) 
LINES = (200, 200, 200)   
START = '#0E2954'           
END = '#2E8A99'         
PATH = '#9BCDD2'      
CLOSED = '#FFDEDE'
OPEN = '#FF8551'


class Spot:
        def __init__(self, row, col, spot_width, total_rows):
            self.row = row
            self.col = col
            self.x = col * spot_width
            self.y = row * spot_width
            self.color = BACKGROUND
            self.neighbours = []
            self.spot_width = spot_width
            self.total_rows = total_rows

        def get_pos(self):
            return self.row, self.col

        def is_closed(self):
            # Closed squares (already visited)
            return self.color == CLOSED

        def is_open(self):
            return self.color == OPEN

        def is_barrier(self):
            return self.color == BARRIER

        def is_start(self):
            return self.color == START

        def is_end(self):
            return self.color == END

        def reset(self):
            return self.color == BACKGROUND


        def make_closed(self):
            # Closed squares (already visited)
            self.color = CLOSED

        def make_open(self):
            self.color = OPEN

        def make_barrier(self):
            self.color = BARRIER

        def make_start(self):
            self.color = START

        def make_end(self):
            self.color = END

        def reset(self):
            self.color = BACKGROUND

        def make_path(self):
            self.color = PATH

        def draw(self, win):
            pygame.draw.rect(win, self.color, (self.x, self.y, self.spot_width, self.spot_width))

        def update_neighbours(self, grid):
            self.neighbours = []
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
                self.neighbours.append(grid[self.row + 1][self.col]) 
            
            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up
                self.neighbours.append(grid[self.row - 1][self.col]) 
            
            if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
                self.neighbours.append(grid[self.row][self.col + 1]) 
            
            if self.row > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
                self.neighbours.append(grid[self.row][self.col - 1]) 

        def __lt__(self, other):
            return False
        
def h(p1,p2):
    #Manhaten distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


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
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

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
        
    return False    


def make_grid(rows,spot_width):
    grid = []
    gap = spot_width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, spot_width):
    gap = spot_width // rows

    for i in range(rows):
        pygame.draw.line(win, LINES, (0, i * gap), (spot_width, i * gap))

    for j in range(rows):
        pygame.draw.line(win, LINES, (j * gap, 0), (j * gap, spot_width))
        
    pygame.draw.line(win, LINES, (j * gap, 0), (j * gap, spot_width))

def draw(win, grid, rows, spot_width):
    win.fill(BACKGROUND)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win,rows,spot_width)
    pygame.display.update()


def get_clicked_pos(pos, rows, spot_width):
    gap = spot_width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return col, row

def main(win, spot_width):
    ROWS = 50
    grid = make_grid (ROWS, spot_width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, spot_width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # left mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, spot_width)
                # click inside the grid
                if row <= ROWS and col <= ROWS:
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != start and spot != end:
                        spot.make_barrier()
                

            elif pygame.mouse.get_pressed()[2]: # right mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, spot_width)

                
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    A_star(lambda: draw(win, grid, ROWS, spot_width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, spot_width)

    pygame.quit()

main(SCREEN, WIN_HEIGHT)
