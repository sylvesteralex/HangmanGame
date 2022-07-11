from hangman_game_helpers import hangman_pics
from hangman_game_helpers import words
from time import sleep
import random


# Game Menu
def hangman_game():
    print("="*8)
    print("Game Menu")
    print("=" * 8)
    print(">> (S)tart a new game")
    print(">> (E)xit")
    action = str(input("Choose an option: start the game - write (S), exit the game (E) ")).upper()

    while True:
        if action[0] == "S":
            print("=" * 8)
            new_game()
        elif action[0] == "E":
            print("== Logged out ==")
            break
        break


# Actual game
def new_game(mistakes=0):
    # mistakes - wrong answers, a given letter didn't exist
    # solved - game won or lost
    given_letters = set()  # store player's answers
    solved = False
    print("Try to guess the word. You can make no more than 6 mistakes. ")

    # allow player to guess the word
    def final_guess():
        nonlocal solved, mistakes
        action = input("Do you want to guess the word? You will loose if you guess wrong! (Y/N) ").strip().upper()

        if action[0] == "Y":
            player_final_guess = str(input("What's your guess? "))
            # print(f"final guess '{final_guess}' vs word '{word}'")  # === testing
            if player_final_guess == word:
                # print(f"solved") # === testing
                solved = True
            else:
                # print(f"not solved")  # === testing
                solved = False
                mistakes = 7

        # print(f"final guess is {solved}")  # === testing
        return solved

    # hangman stages after a mistake
    def hangman():

        hangman_drawing = ""
        for x in range(0, 8):
            if mistakes == x:
                hangman_drawing = hangman_pics[x]

        # old loop
        # if mistakes == 0:
        #     hangman_drawing = hangman_pics[0]
        # if mistakes == 1:
        #     hangman_drawing = hangman_pics[1]
        # if mistakes == 2:
        #     hangman_drawing = hangman_pics[2]
        # if mistakes == 3:
        #     hangman_drawing = hangman_pics[3]
        # if mistakes == 4:
        #     hangman_drawing = hangman_pics[4]
        # if mistakes == 5:
        #     hangman_drawing = hangman_pics[5]
        # if mistakes == 6:
        #     hangman_drawing = hangman_pics[6]
        # if mistakes == 7:
        #     hangman_drawing = hangman_pics[7]

        return hangman_drawing

    # = GAME START =
    word = random.choice(words)
    # print(word)  # === testing
    letters_left = None
    word_len = len(word)
    word_mockup = str("_" * word_len)  # print the hashed word
    print(word_mockup, "(", word_len, " letters", ")")
    # print(word_mockup.find("_")) # === testing

    while True:
        # if solved True, end the game
        if solved or word_mockup == word:
            solved = True  # in case of guessed step by step
            print("=" * 8)
            print("Bravo! You guessed the word!")
            hangman_game()

        # if not solved continue guessing
        else:
            # end the game if the hangman is drawn
            if mistakes == 7:
                print("=" * 8)
                print("You've lost!")
                print("=" * 8)
                sleep(1)
                print(hangman())
                hangman_game()
            else:
                # take only first letter of the input and sanitize
                print("\n")
                guess = str(input("Guess a letter: ")[0].strip().lower())

                # find indexes of the guessed letter
                indexes = [i for i, x in enumerate(word) if x == guess]
                indexes_len = len(indexes)
                letters_left = len([i for i, _ in enumerate(word_mockup) if _ == "_"])
                # print("letter indexes: ", indexes) # === testing

                # Got a guess! show letters
                # No guess! draw a hangman

                # there is such a letter in this word but is repeated
                # if indexes_len > 0 and guess in given_letters:
                #     mistakes += 1

                # letter guessed correctly
                if indexes_len > 0 and guess not in given_letters:
                    for i in indexes:
                        word_mockup = word_mockup[:i] + guess + word_mockup[i + 1:]

                    letters_left = len([i for i, l in enumerate(word_mockup) if l == "_"])
                    print(word_mockup, "(", letters_left, " letters left", ")")
                    # print("solved:", solved) # === testing

                # there is no such a letter in this word /or/ there is such a letter in this word but is being repeated
                elif indexes_len == 0 or indexes_len > 0 and guess in given_letters:
                    mistakes += 1
                    print(f"{mistakes}/6 mistake(s)")
                    if mistakes == 5:
                        print("Watch out! You can make only one more mistake!")
                    if mistakes == 6:
                        print("You can't make any more mistakes!")
                    if mistakes < 7:
                        # check if the guess was already given, but not for the first time the letter is used
                        if guess in given_letters:
                            print(f"{guess} - You've already given that answer! Try another letter.")
                        else:
                            print("No luck, try again.")
                        print(word_mockup, "(", letters_left, " letters left", ")")
                        # print("solved:", solved) # === testing
                        print(hangman())

                # add the guess to the stored answers
                given_letters.add(guess)

                # print("mistakes: ", mistakes)  # === testing

            # allow to guess the word if less than half of the letters left
            if letters_left <= (word_len/2) and mistakes < 7:
                final_guess()


if __name__ == '__main__':
    hangman_game()
