import state
import json
import random

NUM_LETTERS = 5
TOTAL_GUESSES = 8

with open("wordle_list.json", "r") as wordle_list:
    word_list = json.load(wordle_list)

num_success = 0
num_fail = 0
num_error = 0
tot_guesses = 0

for i in range(1000):
    try:
        #secret_word = random.choice(word_list)
        print("SECRET WORD: " + secret_word)secret_word = "idles"


        my_state = state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word)

val = my_state.validate_guess("label")
if my_state.good_word == True:
            my_state.evaluate("label")
            my_state.display()
else:
    print("Please guess a valid word.")
#my_state.evaluate("aniti")
#my_state.display()

        # my_state.evaluate("idles")
        # my_state.display()

my_state.evaluate("hiker")
my_state.display()

        finished = False
        while not finished and num_guesses < TOTAL_GUESSES-1:
            new_guess = my_state.get_new_guess()
            finished = my_state.evaluate(new_guess)
            num_guesses += 1

        print("Secret word", secret_word)
        print("Guesses Taken", num_guesses+1)

        if not finished:
            num_fail += 1
        else:
            num_success += 1
        tot_guesses += num_guesses

    except(IndexError):
        num_error += 1

print("Total successes", num_success)
print("Total failures", num_fail)
print("Total errors", num_error)
print("Total guesses", tot_guesses)

    