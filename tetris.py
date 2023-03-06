import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = 'Tetris'
FONT_NAME = pygame.font.match_font('arial')
FPS = 4#7

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#ORANGE
#TEAL
#PURPLE

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
        self.y = 5

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
            if current_block.shape[y][x] == '*':
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

def new_block():
    # Define block shapes and colors
    shapes = [
        [['*', '*', '*', '*']],
        [['*', ' ', ' ', ' '],
         ['*', '*', '*', '*']],
        [[' ', ' ', ' ', '*'],
         ['*', '*', '*', '*']],
        [['*', '*'],
         ['*', '*']],
        [[' ', '*', '*'],
         ['*', '*', ' ']],
        [[' ', '*', ' '],
         ['*', '*', '*']],
        [['*', '*', ' '],
         [' ', '*', '*']],
    ]
    colors = [RED, GREEN, BLUE, YELLOW]

    # Create a new block
    shape = random.choice(shapes)
    color = random.choice(colors)
    return Block(shape, color)

def move_block(direction):
    if direction == 'down':
        pass
    elif direction == 'left':
        current_block.x -= 1
    elif direction == 'right':
        current_block.x += 1
    elif direction == 'rotate':
        pass #current_block.shape = rotate_block(block.shape)
    else:
        current_block.y += 1

def rotate_block(shape):
    # Transpose the shape matrix
    rotated_shape = list(zip(*shape[::-1]))
    return rotated_shape

def check_collision():
    # Check if the block collides with the boundaries of the grid
    if current_block.x < 0:
        current_block.x = 0
    if current_block.x + len(current_block.shape[0]) >= block_grid_w:
        current_block.x = block_grid_w - len(current_block.shape[0])

    # Check if the block collides with bottom of the grid
    if current_block.y + len(current_block.shape) >= block_grid_h:
        return True

    # Check if the block collides with bottom of the grid with other blocks
    last_row = current_block.shape[-1]
    for x, element in enumerate(last_row):
        if block_grid[current_block.y + len(current_block.shape)][current_block.x + x] != BLACK:
            return True

    # Check if the block collides with other blocks in the grid to the side
    # Left side
    for y, row in enumerate(current_block.shape):
        for x, element in enumerate(row):
            if current_block.shape[y][x] == '*':
                if block_grid[current_block.y + y][current_block.x + x] != BLACK:
                    current_block.x -= 1
                continue
    # Right side
    for y, row in enumerate(current_block.shape):
        for x, element in reversed(list(enumerate(row))):
            if current_block.shape[y][x] == '*':
                if block_grid[current_block.y + y][current_block.x + x] != BLACK:
                    current_block.x += 1
                continue

def lock_block():
    for i, row in enumerate(block.shape):
        for j, cell in enumerate(row):
            if cell == '*':
                grid[block.y + i][block.x + j] = block.color

def imprint_block_to_grid(current_block):
    for y, row in enumerate(current_block.shape):
        for x, element in reversed(list(enumerate(row))):
            if current_block.shape[y][x] == '*':
                block_grid[current_block.y + y][current_block.x + x] = current_block.color
    pass

def check_gameover():
    pass

def update_score():
    pass

# Main game loop
clock = pygame.time.Clock()
game_over = False
score = 0

current_block = new_block()
next_block = new_block()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    direction = ''
    keys = pygame.key.get_pressed()  # Get key press
    # Move current block
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
        current_block = next_block
        next_block = new_block()
        #update_score()
        #check_gameover()

    # Draw graphics
    screen.fill(BLACK)
    draw_grid(screen)
    #draw_text(screen, f'Score: {score}', 18, WINDOW_WIDTH - 80, 10)

    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
