import state
import json
import random
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

NUM_LETTERS = 5
TOTAL_GUESSES = 15
NUM_BOARDS = 8

with open("wordle_list.json", "r") as wordle_list:
    word_list = json.load(wordle_list)


word_sets = [
    ['blimp','ghost','cured','fawny'],
    # ['pudgy','mince','balks','froth'],
    # ['graft','lines','ducky','whomp'],
    # ['fakes','glory','chimp','bundt'],
    # ['arose','cubit','nymph'],
    # ['ratio','mends','lucky']
    ]

def run_one_octordle(tot_guesses, num_error, word_set):
    secret_words = []
    states = []
    last_state = None

    def get_best_guess():
        possible_vocabs = []
        for i in range(len(states)):
            vocabs = states[i].get_new_guess()
            possible_vocabs.append(vocabs)
        possible_vocabs = [lst for lst in possible_vocabs if lst]
        if not possible_vocabs:
            return False
        # print("Possible:",possible_vocabs)
        shortest_list = min(possible_vocabs, key=len)
        # print("Shortist List:",shortest_list)
        return random.choice(shortest_list)


    def check_states(states, last_state, guess):
        finished = True
        to_remove = []
        for i in range(len(states)):
            result = states[i].evaluate(guess)
            # states[i].display()
            if result:
                to_remove.append(i)
            finished = finished and result
        
        to_remove.reverse()
        for removal in to_remove:
            last_state = states[removal]
            states.remove(states[removal])
        
        return states, last_state, finished,

    try:
        for i in range(NUM_BOARDS):
            secret_word = random.choice(word_list)
            secret_words.append(secret_word)
            states.append(state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word, playing_octordle=True))
        
        # print("SECRET WORD: ", secret_words)
        first_words = word_set #['graft','lines','ducky','whomp'] #['arose','cubit','nymph'] #
        ## Four words is better strategy that 3 --> empircally
        
        for word in first_words:
            states, last_state, finished = check_states(states, last_state, word)
        num_guesses = len(first_words)
        finished = False
        # for i in range(len(states)):
        #     states[i].display()
        while not finished and num_guesses < TOTAL_GUESSES-1:
            new_guess = get_best_guess()
            if not new_guess:
                raise IndexError
            num_guesses += 1
            states, last_state, finished = check_states(states, last_state, new_guess)
        new_guess = get_best_guess()
        if new_guess: #Otherwise already guessed
            for i in range(len(states)):
                result = states[i].evaluate(new_guess)
                # states[i].display()
        num_guesses += 1
        if len(states) > 0:
            last_state = states[0]
        correct_in_iter = 0
        for word in secret_words:
            if word in last_state.board:
                correct_in_iter += 1
        tot_guesses += num_guesses
    
    except(IndexError):
        raise IndexError
        num_error += 1
    return correct_in_iter, tot_guesses, num_error, num_guesses

successes = []
fails = []

def run_word_set_trials(word_set):

    num_success = 0
    num_fail = 0
    num_error = 0
    tot_guesses = 0

    correct = 0

    correct_arr = []
    guesses = []
    for i in tqdm(range(1000)):
        correct_iter, tot_guesses, num_error, num_guesses = run_one_octordle(tot_guesses, num_error, word_set)
        correct += correct_iter
        correct_arr.append(correct_iter)
        guesses.append(num_guesses)

    print(f"Correct puzzles: {correct}/800")
    # print(correct_arr)
    for elem in correct_arr:
        if elem == NUM_BOARDS:
            num_success += 1
        else:
            num_fail += 1

    # plt.plot(guesses)
    # plt.show()

    return num_success, num_fail
    # print("Total successes", num_success)
    # print("Total failures", num_fail)
    # print("Total errors", num_error)
    # print("Total guesses", tot_guesses)

for word_set in word_sets:
    success, fail = run_word_set_trials(word_set)
    successes.append(success)
    fails.append(fail)


np_s = np.array(successes)
np_f = np.array(fails)


accuracy = np_s/(np_s + np_f)
print(accuracy)
first_words = [word_set[0] for word_set in word_sets]
plt.bar(first_words,accuracy)

plt.xlabel('Word Set (first word)')
plt.ylabel('Success Rate')
plt.title('Success Rate for ech Word Set')

plt.show()