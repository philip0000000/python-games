# Author: philip0000000

import pygame
import random

print("Simple pong game by philip0000000")
print("Instructions:")
print("w and s                - for left paddle")
print("up and down arrow keys - for right paddle")
print("r                      - reset scoreboard")
print("o and p                - for speed adjustments")
print("q                      - for left paddle to follow ball")
print("esc key                - to exit game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PADDLE_THICKNESS = 10
PADDLE_LENGTH = 100
PADDLE_MOVE_SPEED = 5

BALL_CIRCUMFERENCE = 10

GAME_WINDOW_SIZE_HORIZONTAL = 640
GAME_WINDOW_SIZE_VERTICAL = 480

WAIT_TIME = 1

# Initialize Pygame
pygame.init()

window = pygame.display.set_mode((GAME_WINDOW_SIZE_HORIZONTAL, GAME_WINDOW_SIZE_VERTICAL)) # Set the window size
pygame.display.set_caption("Pong") # Set the title of the window

window_w, window_h = pygame.display.get_surface().get_size()

# Represents player paddle
class paddle(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x_pos, y_pos):
        # Call the parent's constructor
        super().__init__()

        # Set the background color and set it to be transparent
        self.box = pygame.Surface((PADDLE_THICKNESS, PADDLE_LENGTH))
        self.box.fill(BLACK)
        self.rect = self.box.get_rect()
        self.rect.center = (x_pos, y_pos)

    def up(self):
        self.rect.y -= PADDLE_MOVE_SPEED
        if self.rect.y < 0:
            self.rect.y = 0

    def down(self):
        self.rect.y += PADDLE_MOVE_SPEED
        if self.rect.y + PADDLE_LENGTH > window_h:
            self.rect.y = window_h - PADDLE_LENGTH

    def draw(self):
        window.blit(self.box, self.rect)

    def set_y_pos(self, y_pos):
        self.rect.y = y_pos - (PADDLE_LENGTH / 2)

class ball():
    def __init__(self, x_pos, y_pos):
        # Create rect coordinates
        self.new_ball(x_pos, y_pos)

    def new_ball(self, x_pos, y_pos):
        self.ball = pygame.draw.circle(window, BLACK, (x_pos, y_pos), BALL_CIRCUMFERENCE)

        self.direction = random.choice(["right", "left"]) # Direction the ball is moving towards
        self.angle = float(0)    # Angle the ball
        self.y_pos_float = float(y_pos)

    def draw(self):
        pygame.draw.circle(window, BLACK, (self.ball.left, self.ball.top), BALL_CIRCUMFERENCE)

    def check_if_ball_touch_paddle(self, paddle):
        # Check if we hit the ball
        if self.ball.y > paddle.rect.y and paddle.rect.y + PADDLE_LENGTH > self.ball.y \
        and self.ball.x > paddle.rect.x - (PADDLE_THICKNESS/2) and self.ball.x < paddle.rect.x + PADDLE_THICKNESS:
            self.direction = "left" if self.direction == "right" else "right"
            
            # Get where the ball hit the paddle
            delta = self.ball.y - paddle.rect.y
            if delta > 0:
                if delta > PADDLE_LENGTH:
                    delta = PADDLE_LENGTH

                # Change angle
                if self.angle > 0:
                    self.angle = -abs(self.angle)
                else:
                    self.angle = abs(self.angle)

                # Calculate angle of the ball
                if delta <= PADDLE_LENGTH / 2:
                    if self.angle > 0:
                        self.angle = -abs(self.angle)
                else:
                    delta -= PADDLE_LENGTH

                self.angle = delta * (1 / (PADDLE_LENGTH / 2))

    def check_if_ball_outside_window_right(self, window_w):
        if self.ball.x > window_w:
            return True
        return False

    def check_if_ball_outside_window_left(self):
        if self.ball.x < 0:
            return True
        return False
        
    def update(self):
        if self.direction == "left":
            self.ball.x -= 1
        else: #elif self.direction == "right"
            self.ball.x += 1
        
        # If ball touches top or bottom change direction
        if self.ball.y <= 0:
            self.angle = abs(self.angle)
            self.y_pos_float += self.angle
        elif self.ball.y >= window_h:
            self.angle = -abs(self.angle)
            self.y_pos_float += self.angle

        self.y_pos_float += self.angle
        self.ball.y = int(self.y_pos_float)

    def get_y_pos(self):
        return self.ball.y

auto_follow  = False # If true, left paddle follows ball
paddle_left  = paddle(PADDLE_THICKNESS/2, 300)
paddle_right = paddle(window_w-(PADDLE_THICKNESS/2), 300)
game_ball    = ball(window_w/2, window_h/2)

left_player_score = 0
right_player_score = 0

def draw_score():
    # Load the font
    font = pygame.font.Font(pygame.font.match_font("arial"), 32)
    # Create a Surface object containing the text
    text_surface = font.render(f"{left_player_score} - {right_player_score}", True, BLACK)
    window.blit(text_surface, ((GAME_WINDOW_SIZE_HORIZONTAL / 2) - 40, 10))

# Main game loop
running = True
while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()  # Get key press

    # Move right paddle
    if keys[pygame.K_UP]:
        paddle_right.up()
    if keys[pygame.K_DOWN]:
        paddle_right.down()

    # Move left paddle
    if auto_follow == False:
        if keys[pygame.K_w]:
            paddle_left.up()
        if keys[pygame.K_s]:
            paddle_left.down()
    else:
        # Set left paddle to ball position
        paddle_left.set_y_pos(game_ball.get_y_pos())

    if keys[pygame.K_b]:
            game_ball.new_ball(window_w/2, window_h/2)
    if keys[pygame.K_r]: # Reset scoreboard
        left_player_score = 0
        right_player_score = 0
    if keys[pygame.K_q]: # Left paddle follow the ball
        auto_follow = True if auto_follow == False else False
    if keys[pygame.K_o]: # Make ball movment slower
        WAIT_TIME += 1
    if keys[pygame.K_p]: # Make ball movment faster
        WAIT_TIME -= 1
        if WAIT_TIME < 0:
            WAIT_TIME = 1
    
    pygame.time.wait(WAIT_TIME) # Wait in milliseconds

    # Update ball position
    game_ball.check_if_ball_touch_paddle(paddle_left)
    game_ball.check_if_ball_touch_paddle(paddle_right)
    game_ball.update()

    # If ball is outside bounds
    if game_ball.check_if_ball_outside_window_right(window_w) == True:
        game_ball.new_ball(window_w/2, window_h/2)
        left_player_score += 1
    elif game_ball.check_if_ball_outside_window_left() == True:
        game_ball.new_ball(window_w/2, window_h/2)
        right_player_score += 1

    # Draw to the screen
    window.fill(WHITE)
    paddle_left.draw()
    paddle_right.draw()
    game_ball.draw()
    draw_score()
    pygame.display.flip()
    
pygame.quit()
