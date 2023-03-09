import pygame
import random

# TODO:
# refactor code and make more responsive controllers

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = 'Tetris'
FONT_NAME = pygame.font.match_font('arial')
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
TEAL = (0, 128, 128)
PURPLE = (128, 0, 128)

# Define game variables
TILE_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // TILE_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // TILE_SIZE
GRID_TOP = 0
GRID_LEFT = WINDOW_WIDTH // 2 - GRID_WIDTH * TILE_SIZE // 2
GRID_BOTTOM = GRID_HEIGHT * TILE_SIZE
GRID_RIGHT = GRID_LEFT + GRID_WIDTH * TILE_SIZE

block_grid_w, block_grid_h = 10, 20
block_grid = [[BLACK for _ in range(block_grid_w)] for _ in range(block_grid_h)]

class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = (block_grid_w // 2) - (len(self.shape[0]) // 2)
        self.y = -2

# Define functions
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_grid(surface):
    # Get cordinates
    size = pygame.display.get_window_size()
    size = (size[0] // 2, size[1] // 2)
    x0 = size[0] - TILE_SIZE * (block_grid_w // 2)
    x1 = x0 + TILE_SIZE * block_grid_w
    y0 = size[1] - TILE_SIZE * (block_grid_h // 2)
    y1 = y0 + TILE_SIZE * block_grid_h

    # Draw current blocks
    for y, row in enumerate(current_block.shape):
        for x, element in enumerate(row):
            if element == '*':
                if y0 + (current_block.y+y) * TILE_SIZE >= y0:
                    pygame.draw.rect(surface, current_block.color,
                                    (x0 + (current_block.x+x) * TILE_SIZE,
                                    y0 + (current_block.y+y) * TILE_SIZE,
                                    TILE_SIZE, TILE_SIZE))
 
    # Draw blocks
    for y in range(block_grid_h):
        for x in range(block_grid_w):
            if block_grid[y][x] != BLACK:
                pygame.draw.rect(surface, block_grid[y][x],
                                (x0 + x * TILE_SIZE, y0 + y * TILE_SIZE,
                                TILE_SIZE, TILE_SIZE))

    # Draw grid
    for x in range(x0, x1 + 1, TILE_SIZE):                  # Add +1 for last line
        pygame.draw.line(surface, WHITE, (x, y0), (x, y1))
    for y in range(y0, y1 + 1, TILE_SIZE):                  # Add +1 for last line
        pygame.draw.line(surface, WHITE, (x0, y), (x1, y))

    # Draw next block
    for y, row in enumerate(next_block.shape):
        for x, element in enumerate(row):
            if element == '*':
                pygame.draw.rect(surface, next_block.color,
                                    ((WINDOW_WIDTH - 6 * TILE_SIZE) + (x * TILE_SIZE),
                                    (WINDOW_HEIGHT - 6 * TILE_SIZE) + (y * TILE_SIZE),
                                    TILE_SIZE, TILE_SIZE))

def new_block():
    # Define block shapes and colors
    shapes = [
        [[' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        ['*', '*', '*', '*'],
        [' ', ' ', ' ', ' ']],
        [['*', ' ', ' '],
         ['*', '*', '*'],
         [' ', ' ', ' ']],
        [[' ', ' ', '*'],
         ['*', '*', '*'],
         [' ', ' ', ' ']],
        [['*', '*'],
         ['*', '*']],
        [[' ', '*', '*'],
         ['*', '*', ' '],
         [' ', ' ', ' ']],
        [[' ', '*', ' '],
         ['*', '*', '*'],
         [' ', ' ', ' ']],
        [['*', '*', ' '],
         [' ', '*', '*'],
         [' ', ' ', ' ']]
    ]
    colors = [RED, GREEN, BLUE, YELLOW, ORANGE, TEAL, PURPLE]

    # Create a new block
    shape = random.choice(shapes)
    color = random.choice(colors)
    return Block(shape, color)

def move_block(direction):
    global speed, velocity

    # Add to speed
    speed += velocity
    if speed > 1:
        speed = 0.0

    if direction == 'down':
        while does_block_fit(1, 0, current_block.shape):
            current_block.y += 1
    elif direction == 'left':
        if does_block_fit(0, -1, current_block.shape):
            current_block.x -= int(speed)
    elif direction == 'right':
        if does_block_fit(0, 1, current_block.shape):
            current_block.x += int(speed)
    elif direction == 'rotate':
        rotate_block()
    else:
        current_block.y += int(speed)

def rotate_array(arr):
    n = len(arr)
    m = len(arr[0])
    result = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            result[j][n-i-1] = arr[i][j]
    return result

def does_block_fit(y_pos, x_pos, arr2D):
    for y, row in enumerate(arr2D):
        for x, element in enumerate(row):
            if element == '*':
                if current_block.x + x + x_pos < 0 or current_block.x + x + x_pos >= len(block_grid[0]) or \
                   current_block.y + y + y_pos >= len(block_grid) or \
                   block_grid[current_block.y + y + y_pos][current_block.x + x + x_pos] != BLACK:
                    return False
    return True

def rotate_block():
    # Transpose the shape matrix
    rotated_array = rotate_array(current_block.shape)
    
    # Test if rotated block fits in the current position
    if does_block_fit(0, 0, rotated_array):
        # Change the current block position
        current_block.shape = rotated_array

def collides_with_bottom():
    # Check if the block collides with bottom of the grid
    for y, row in enumerate(current_block.shape):
        for x, element in enumerate(row):
            if current_block.shape[y][x] == '*' and current_block.y + y + 1 >= len(block_grid):
                return True
    return False

def check_collision():
    # Check if the block collides with bottom of the grid
    if collides_with_bottom() == True:
        return True

    # Check if the block collides with other blocks, one step down
    if does_block_fit(1, 0, current_block.shape) == False:
        return True
    return False

def imprint_block_to_grid(current_block):
    for y, row in enumerate(current_block.shape):
        for x, element in reversed(list(enumerate(row))):
            if current_block.shape[y][x] == '*':
                block_grid[current_block.y + y][current_block.x + x] = current_block.color

def check_gameover():
    for y, row in enumerate(current_block.shape):
        for x, element in enumerate(row):
            if element == '*' and current_block.y + y + 1 > 0 and \
                block_grid[current_block.y + y + 1][current_block.x + x] != BLACK:
                    global game_over
                    game_over = True
                    return

def update_score():
    for y, item in reversed(list(enumerate(current_block.shape))):
        for elem in item:
            if elem == '*':
                row_filled = True
                for element in block_grid[current_block.y + y]:
                    if element == BLACK:
                        row_filled = False
                        break
                if row_filled:
                    # Remove full row
                    block_grid.pop(current_block.y + y)
                    # Add to score
                    global score
                    score += 1
                    # Jump to next row
                    break
    # Add new rows
    while len(block_grid) < block_grid_h:
        block_grid.insert(0, [BLACK for _ in range(block_grid_w)])

# Main game loop
clock = pygame.time.Clock()
game_over = False
exit = False
score = 0
speed = 0.0
velocity = 0.2

current_block = new_block()
next_block = new_block()

while not game_over:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            Exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
                exit = True

    # Get key press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_PLUS]:
        velocity += 0.1
    if keys[pygame.K_MINUS]:
        velocity -= 0.1
    
    # Move current block
    direction = ''
    if keys[pygame.K_LEFT]:
        direction = 'left'
    if keys[pygame.K_RIGHT]:
        direction = 'right'
    if keys[pygame.K_DOWN]:
        direction = 'down'
    if keys[pygame.K_UP]:
        direction = 'rotate'

    # Update game logic
    move_block(direction)
    if (check_collision()):
        imprint_block_to_grid(current_block)
        update_score()
        current_block = next_block
        next_block = new_block()
        check_gameover()

    # Draw graphics
    screen.fill(BLACK)
    draw_grid(screen)
    draw_text(screen, f'Score: {score}', 18, WINDOW_WIDTH - 80, 10)

    pygame.display.update()
    clock.tick(FPS)

if exit == False:
    while not exit:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                Exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    exit = True

        # Draw graphics
        screen.fill(BLACK)
        size = pygame.display.get_window_size()
        size = (size[0] // 2, size[1] // 2)
        draw_text(screen, 'Game Over', 25, size[0], size[1] - 25)
        draw_text(screen, f'Score: {score}', 25, size[0], size[1] + 25)
        pygame.display.update()
        clock.tick(FPS)

# Quit Pygame
pygame.quit()
