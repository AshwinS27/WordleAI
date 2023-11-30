import state
import json
import random

NUM_LETTERS = 5
TOTAL_GUESSES = 13

with open("wordle_list.json", "r") as wordle_list:
    word_list = json.load(wordle_list)

num_success = 0
num_fail = 0
num_error = 0
tot_guesses = 0
player_1_wins = 0
player_2_wins = 0

player_1 = True #Start with player 1, if false = player 2

secret_words = []
states = []
    

def get_best_guess():
    possible_vocabs = []
    for i in range(len(states)):
        vocabs = states[i].get_new_guess()
        possible_vocabs.append(vocabs)
    
    print(possible_vocabs)
    shortest_list = min(possible_vocabs, key=len)
    print(shortest_list)
    return random.choice(shortest_list)


for i in range(1):
    try:
        for i in range(8):
            secret_word = random.choice(word_list)
            secret_words.append(secret_word)
            states.append(state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word, playing_octordle=True))
        
        print("SECRET WORD: ", secret_words)

        for i in range(8):
            states[i].evaluate("graft")
            states[i].evaluate("lines")
            states[i].evaluate("ducky")
            states[i].evaluate("whomp")

        num_guesses = 4

        finished = False

        for i in range(8):
            states[i].display()

        while not finished and num_guesses < TOTAL_GUESSES-1:
            new_guess = get_best_guess()
            print("NEW GUESS: ", new_guess)

            to_remove = []
            finished = True
            for i in range(len(states)):
                print(states)
                print(len(states))
                result = states[i].evaluate(new_guess)
                states[i].display()
                if result:
                    to_remove.append(i)
                finished = finished and result
                print("Finished", finished)
            num_guesses += 1

            for removal in to_remove:
                states.remove(states[removal])

        new_guess = get_best_guess()
        for i in range(len(states)):
            result = states[i].evaluate(new_guess)


        print("Secret word", secret_word)
        print("Guesses Taken", num_guesses+1)

        if not finished:
            num_fail += 1
        else:
            num_success += 1
        tot_guesses += num_guesses

    except(IndexError):
        raise IndexError
        num_error += 1

print("SECRET words:", secret_words)
print("Total successes", num_success)
print("Total failures", num_fail)
print("Total errors", num_error)
print("Total guesses", tot_guesses)
print("Player 1 Wins", player_1_wins)
print("Player 2 wins", player_2_wins)

    