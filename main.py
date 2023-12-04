import state
import json
import random
import matplotlib.pyplot as plt

NUM_LETTERS = 5
TOTAL_GUESSES = 6

with open("wordle_list.json", "r") as wordle_list:
    word_list = json.load(wordle_list)


def run_trails(start_word):
    num_success = 0
    num_fail = 0
    num_error = 0
    tot_guesses = 0
    guess_solved_at = []

    for i in range(1000):
        try:
            secret_word = random.choice(word_list) #erase 
            # print("SECRET WORD: " + secret_word)

            my_state = state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word)

            finished = my_state.evaluate(start_word) #geese

            num_guesses = 1

            while not finished and num_guesses < TOTAL_GUESSES:
                new_guess = my_state.get_new_guess()
                finished = my_state.evaluate(new_guess)
                my_state.display()
                num_guesses += 1

            if not finished:
                num_fail += 1
                guess_solved_at.append(0)
            else:
                guess_solved_at.append(num_guesses)
                num_success += 1
            tot_guesses += num_guesses

        except(IndexError):
            raise IndexError
            num_error += 1

    return num_success, num_fail, tot_guesses, guess_solved_at
    print("Total successes", num_success)
    print("Total failures", num_fail)
    print("Total errors", num_error)
    print("Total guesses", tot_guesses)

start_words = ['crane']#, 'stare','soare','slate','salet','audio']
successes = []
fails = []
tot_guesses = []
from collections import Counter

for word in start_words:
    num_succ, num_fail, tot_guess, guess_solved_at = run_trails(word)
    successes.append(num_succ)
    fails.append(num_fail)
    tot_guesses.append(tot_guess)

    counts = Counter(guess_solved_at)

    counts_dict = dict(counts)
    counts_dict[1] = 0
    sorted_dict = sorted(counts_dict.items())
    print("sorted_dict", sorted_dict)

    guess_solved = [elem[1] for elem in sorted_dict]
    plt.bar(range(0,TOTAL_GUESSES+1), guess_solved)
    plt.xlabel('Guess Number Wordle Solved')
    plt.ylabel('Games')
    plt.title('Guess Number Wordle was Solved')

#plt.bar(start_words, successes)
#plt.bar(start_words, fails)
#plt.bar(start_words, tot_guesses)
plt.show()