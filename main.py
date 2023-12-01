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
            else:
                num_success += 1
            tot_guesses += num_guesses

        except(IndexError):
            raise IndexError
            num_error += 1

    return num_success, num_fail, tot_guesses
    print("Total successes", num_success)
    print("Total failures", num_fail)
    print("Total errors", num_error)
    print("Total guesses", tot_guesses)

start_words = ['crane', 'stare','soare','slate','salet','audio']
successes = []
fails = []
tot_guesses = []
for word in start_words:
    num_succ, num_fail, tot_guess = run_trails(word)
    successes.append(num_succ)
    fails.append(num_fail)
    tot_guesses.append(tot_guess)

plt.bar(start_words, successes)
#plt.bar(start_words, fails)
#plt.bar(start_words, tot_guesses)
plt.show()