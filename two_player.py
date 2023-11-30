import state
import json
import random

NUM_LETTERS = 5
TOTAL_GUESSES = 6

with open("wordle_list.json", "r") as wordle_list:
    word_list = json.load(wordle_list)

num_success = 0
num_fail = 0
num_error = 0
tot_guesses = 0
player_1_wins = 0
player_2_wins = 0

player_1 = True #Start with player 1, if false = player 2

for i in range(100):
    try:
        secret_word = random.choice(word_list) #erred
        print("SECRET WORD: " + secret_word)

        my_state = state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word)

        my_state.evaluate("crane")
        #my_state.display()

        # my_state.evaluate("toils")
        # my_state.display()

        num_guesses = 0

        finished = False

        while not finished and num_guesses < TOTAL_GUESSES-1:
            if num_guesses % 2 == 0:
                player_1 = True
            else:
                player_1 = False

            new_guess = my_state.get_new_guess()
            finished = my_state.evaluate(new_guess)
            num_guesses += 1

        new_guess = my_state.get_new_guess()

        print("Secret word", secret_word)
        print("Guesses Taken", num_guesses+1)

        if not finished:
            num_fail += 1
        else:
            num_success += 1
            if player_1:
                player_1_wins += 1
            else:
                player_2_wins += 1
        tot_guesses += num_guesses

    except(IndexError):
        num_error += 1

print("Total successes", num_success)
print("Total failures", num_fail)
print("Total errors", num_error)
print("Total guesses", tot_guesses)
print("Player 1 Wins", player_1_wins)
print("Player 2 wins", player_2_wins)

    