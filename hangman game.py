# Author philip0000000
import random

# List of words to choose from
words = [ "yogurt", "giraffe", "Piano", "Violin", "Moon",
          "Sofa", "Boat", "Flute", "Orange", "Strawberry",
          "football", "piano", "Banana", "gamma", "Science",
          "Pencil", "Phone", "Flower", "Guitar", "Drum",
          "Cat", "Cloud", "horse", "spider", "umbrella",
          "jaguar", "lemon", "Sky", "train", "alpha",
          "Radio", "xylophone", "Computer", "cat", "Fridge",
          "Tree", "Apple", "newspaper", "Microwave", "Table",
          "book", "Bed", "Speaker", "mango", "Camera",
          "Music", "delta", "Book", "Desk", "whale",
          "octopus", "Dryer", "kangaroo", "Television", "Chair",
          "beta", "queen", "Theater", "Dog", "Headphones",
          "Paper", "Dance", "Mountain", "Star", "desk",
          "Clock", "Sun", "elephant", "violin", "apple",
          "Pen", "Trumpet", "raccoon", "Blueberry", "Car",
          "igloo", "Saxophone", "Stove", "zebra", "Ocean",
          "Art", "Dishwasher", "Oven", "Lamp" ]

word = random.choice(words) # Choose a random word from the list
word = word.lower()
correct_letters = []        # Correct letters
incorrect_letters = []      # Incorrect letters
tries = 6                   # Number of tries
run_loop = True             # If the game should continue

# Main game loop
while run_loop:
    # Print the current state of the game
    print()
    print("Word: " + "".join([letter if letter in correct_letters else "_" for letter in word]))
    print("Incorrect letters: " + " ".join(incorrect_letters))
    print("Tries remaining: " + str(tries))

    letter = input("Guess a letter: ")   # Prompt the player for a letter
    letter = letter.lower()

    # if letter has been used, do nothing
    if letter in correct_letters or letter in incorrect_letters:
        print(f"Letter has already been used: {letter}")
    elif letter in word:                 # Check if the letter is in the word
        correct_letters.append(letter)   # Add the letter to the correct letters list
    else:                                # It is a wrong letter
        incorrect_letters.append(letter) # Add the letter to the incorrect letters list
        tries -= 1                       # Decrement the number of tries

    # Check if the player has won the game
    if all(letter in correct_letters for letter in word):
        print(f"Congratulations! You won! The word was: {word}") # Print win message
        run_loop = False                   # End main game loop
    # Check if the player has lost the game
    elif tries == 0:
        print(f"Sorry, you lost. The word was {word}.") # Print lose message
        run_loop = False                                # End main game loop
