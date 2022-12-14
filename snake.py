# AUthor philip0000000
# simple snake game, works on windows only

import os
import msvcrt
from random import randrange
import time

class snake_game:
    def __init__(self):
        # The dimensions of the game board
        self.BOARD_WIDTH  = 20
        self.BOARD_HEIGHT = 20

        self.board = [] # The board, which is a grid of squares
        self.snake = [] # The snake, a list of coordinates (x, y)
        self.food  = () # The food, a single coordinate (x, y)
        self.score = 0  # The score, is the length of the snake

        # The direction in which the snake is moving, represented as a string
        self.direction = "" # ("up", "down", "left", or "right")

        self.main_loop_run = True # Run the main loop
        self.WAIT          = 0.3  # How long to wait in second

    def start(self):
        # Initialize the game
        self.board = [[0 for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.snake.append((self.BOARD_WIDTH / 2, self.BOARD_HEIGHT / 2)) # Begin in the middle
        self.generate_food()
        self.direction = "right"
        self.main_loop_run = True

        # Run game loop
        while self.main_loop_run == True:
            self.update()
            self.render()
            self.handle_input()

    def update(self):
        if self.main_loop_run == False:
            return

        # Get the current position of the snake's head
        x, y = self.snake[0]

        # Update the position of the snake's head based on the current direction
        if self.direction == "up":
            y -= 1
        elif self.direction == "down":
            y += 1
        elif self.direction == "left":
            x -= 1
        elif self.direction == "right":
            x += 1

        # Check if the snake has collided with the wall or itself
        if (x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT or
            (x, y) in self.snake):
            self.game_over()
            return

        # Check if the snake has eaten the food
        if (x, y) == self.food:
            # Increase the score and generate new food
            self.score += 1
            self.generate_food()
        else:
            # Remove the tail of the snake if it hasn't eaten the food
            self.snake.pop()

        # Add the new position of the snake's head to the front of the snake
        self.snake.insert(0, (x, y))

    def render(self):
        if self.main_loop_run == False:
            return

        # Clear the screen
        os.system("cls" if os.name == "nt" else "clear")

        # Print the game board
        print("+--------------------+")       # Print top border
        for y in range(self.BOARD_HEIGHT):
            print("|", end="")                # Print left border
            for x in range(self.BOARD_WIDTH):
                if (x, y) in self.snake:
                    print("S" if (x, y) == self.snake[0] # Print the snake head
                          else "s", end="")   # Print the snake body
                elif (x, y) == self.food:
                    print("F", end="")        # Print the food
                else:
                    print(" ", end="")        # Print an empty space
            print("|", end="")                # Print right border
            print()

        print("+--------------------+")       # Print bottom border
        print("Score: {}".format(self.score)) # Print the score

    def handle_input(self):
        if self.main_loop_run == False:
            return

        time.sleep(self.WAIT) # Sleep in seconds

        key = self.get_key()

        # Update the direction of the snake based on the user input
        if key == b"w" and self.direction   != "down":
            self.direction = "up"
        elif key == b"s" and self.direction != "up":
            self.direction = "down"
        elif key == b"a" and self.direction != "right":
            self.direction = "left"
        elif key == b"d" and self.direction != "left":
            self.direction = "right"
        elif key == b"\x1b": # Esc key, end game
            self.game_over()
            return

    def game_over(self):
        print("Game over!")                         # Print the game over message
        print("Final score: {}".format(self.score)) # Print the final score
        self.main_loop_run = False                  # End the main game loop

    def generate_food(self):
        not_done = True
        while not_done:
            x = randrange(self.BOARD_WIDTH)
            y = randrange(self.BOARD_HEIGHT)
            if (x, y) not in self.snake:            # If food is generated on snake body, redo
                not_done = False
        self.food = (x, y)

    def get_key(self):
        key = ""
        # Get key pressed if any
        # Works on windows, for linux see:
        # https://stackoverflow.com/questions/2408560/non-blocking-console-input
        if msvcrt.kbhit():
            key = msvcrt.getch()
        return key

game = snake_game()
game.start()
