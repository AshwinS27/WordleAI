import state
import json
import random

NUM_LETTERS = 5
TOTAL_GUESSES = 6

with open("wordle_list.json", "r") as wordle_list:
    word_list = json.load(wordle_list)
secret_word = random.choice(word_list)


my_state = state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word)

my_state.evaluate("crane")
my_state.display()

my_state.evaluate("toils")
my_state.display()

my_state.evaluate("hiker")
my_state.display()

new_guess = my_state.get_new_guess()
my_state.evaluate(new_guess)
my_state.display()