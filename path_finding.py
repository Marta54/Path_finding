import pygame
from queue import PriorityQueue
import time

pygame.font.init()
# create grid
WIN_WIDTH = 800
WIN_HEIGHT = 500

SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Path finding visualization")

# selection buttons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_X = 550
BUTTON_Y = 130

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
            self.colour = BACKGROUND
            self.neighbours = []
            self.spot_width = spot_width
            self.total_rows = total_rows

        def get_pos(self):
            return self.row, self.col

        def is_closed(self):
            # Closed squares (already visited)
            return self.colour == CLOSED

        def is_open(self):
            return self.colour == OPEN

        def is_barrier(self):
            return self.colour == BARRIER

        def is_start(self):
            return self.colour == START

        def is_end(self):
            return self.colour == END

        def reset(self):
            return self.colour == BACKGROUND


        def make_closed(self):
            # Closed squares (already visited)
            self.colour = CLOSED

        def make_open(self):
            self.colour = OPEN

        def make_barrier(self):
            self.colour = BARRIER

        def make_start(self):
            self.colour = START

        def make_end(self):
            self.colour = END

        def reset(self):
            self.colour = BACKGROUND

        def make_path(self):
            self.colour = PATH

        def draw(self, win):
            pygame.draw.rect(win, self.colour, (self.x, self.y, self.spot_width, self.spot_width))

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
        
class Button:
    def __init__(self, BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, text, border_colour):
        self.BUTTON_X = BUTTON_X
        self.BUTTON_Y = BUTTON_Y
        self.BUTTON_WIDTH = BUTTON_WIDTH
        self.BUTTON_HEIGHT = BUTTON_HEIGHT
        self.border_colour = border_colour
        self.colour = BACKGROUND
        self.text = text
        self.font = pygame.font.SysFont('Arial', 20)
        
        self.button = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

    def get_pos(self):
        return self.button.x, self.button.width, self.button.y, self.button.height
    
    def make_clicked(self):
        self.colour = OPEN

    def reset(self):
        self.colour = BACKGROUND

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.button) 
        pygame.draw.rect(win, self.border_colour, self.button, 1) 
        self.button_text = self.font.render(self.text, True, BARRIER)
        SCREEN.blit(self.button_text, (self.button.x + self.button.width // 2 - self.button_text.get_width() // 2,
                               self.button.y + self.button.height // 2 - self.button_text.get_height() // 2))

def h(p1,p2):
    #Manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


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

def reconstruct_path(came_from, current, draw):
    size = 0
    while current in came_from:
        current = came_from[current]
        size += 1
        current.make_path()
        draw()

    return size


def make_grid(rows, spot_width):
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
        
def draw_buttons(win, buttons):
    for button in buttons:
        button.draw(win)
    
    
    
    # instructions
    instructions_font = pygame.font.SysFont('Arial', 15)
    SCREEN.blit(instructions_font.render('1. Select an Algorithm', True, BARRIER), (530, 10))
    SCREEN.blit(instructions_font.render('2. Choose Start and End points in the grid', True, BARRIER), (530, 30))
    SCREEN.blit(instructions_font.render('3. Draw Barriers in the Grid', True, BARRIER), (530, 50))
    SCREEN.blit(instructions_font.render('4. Click Space to Start', True, BARRIER), (530, 70))
    SCREEN.blit(instructions_font.render('5. Click c to clear', True, BARRIER), (530, 90))

    pygame.display.update()

def draw(win, grid, rows, spot_width, buttons, text_info):
    win.fill(BACKGROUND)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win,rows,spot_width)
    draw_buttons(win, buttons)

    # text info
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
    text = ['Time Spent: ', 'Distance: ']
    
    buttons = [Button(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 'A*', BARRIER),
               Button(BUTTON_X, BUTTON_Y + (BUTTON_HEIGHT + 10), BUTTON_WIDTH, BUTTON_HEIGHT, 'Dijkstra - not yet', BARRIER),
               Button(BUTTON_X, BUTTON_Y + 2 * (BUTTON_HEIGHT + 10), BUTTON_WIDTH, BUTTON_HEIGHT, 'Wavefront - not yet', BARRIER),
               Button(BUTTON_X, BUTTON_Y + 3 * (BUTTON_HEIGHT + 10), BUTTON_WIDTH, BUTTON_HEIGHT, 'BFS - not yet', BARRIER),
               Button(530, 380,  BUTTON_WIDTH, 40, text[0], BACKGROUND),
               Button(530, 420,  BUTTON_WIDTH, 40, text[1], BACKGROUND)
               ]

    start = None
    end = None

    run = True
    algorithm = None
    while run:
        draw(win, grid, ROWS, spot_width, buttons, text)
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False             

            if pygame.mouse.get_pressed()[0]: # left mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, spot_width)

                # Select Algorithm
                font = pygame.font.SysFont('Arial', 20)
                # A*
                if (pos[1] < BUTTON_Y + BUTTON_HEIGHT and pos[1] > BUTTON_Y) and (pos[0] > BUTTON_X and pos[0] < BUTTON_X + BUTTON_WIDTH):
                    algorithm = 'A*'
                    buttons[0].make_clicked()
                    
                # click inside the grid
                if row <= ROWS and col <= ROWS and algorithm: 
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

                    if algorithm == 'A*':
                        t0 = time.time()
                        size = A_star(lambda: draw(win, grid, ROWS, spot_width, buttons,text), grid, start, end)
                        elapsed = time.time() - t0
                        text = [f'Time Spent: {time.strftime("%M:%S.{}".format(str(elapsed % 1)[2:])[:9], time.gmtime(elapsed))}', f'Distance: {size[1]} blocks']
                        buttons[-2] = Button(530, 380,  BUTTON_WIDTH, 40, text[0], BACKGROUND)
                        buttons[-1] = Button(530, 420,  BUTTON_WIDTH, 40, text[1], BACKGROUND)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    algorithm = None
                    for button in buttons:
                        button.reset()

                    text = ['Time Spent: ', 'Distance: ']
                    buttons[-2] = Button(530, 380,  BUTTON_WIDTH, 40, text[0], BACKGROUND)
                    buttons[-1] = Button(530, 420,  BUTTON_WIDTH, 40, text[1], BACKGROUND)                    
                        
                    grid = make_grid(ROWS, spot_width)

    pygame.quit()

main(SCREEN, WIN_HEIGHT)
