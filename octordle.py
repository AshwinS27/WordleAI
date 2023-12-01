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


player_1 = True #Start with player 1, if false = player 2

correct = 0
def run_one_octordle(correct, tot_guesses, num_error):
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
        print("Possible:",possible_vocabs)
        shortest_list = min(possible_vocabs, key=len)
        print("Shortist List:",shortest_list)
        return random.choice(shortest_list)


    for i in range(1):
        try:
            for i in range(8):
                secret_word = random.choice(word_list)
                secret_words.append(secret_word)
                states.append(state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word, playing_octordle=True))
            
            print("SECRET WORD: ", secret_words)

            for i in range(8):
                # states[i].evaluate("arose")
                # states[i].evaluate("cubit")
                # states[i].evaluate("nymph")

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
                print("NEW GUESS: ", new_guess[0])
                if not new_guess:
                    for i in range(len(states)):
                        vocabs = states[i].get_new_guess()
                        print(vocabs)
                    print(len(states))
                    raise IndexError
                to_remove = []
                finished = True
                for i in range(len(states)):
                    # print(states)
                    # print(len(states))
                    result = states[i].evaluate(new_guess)
                    states[i].display()
                    if result:
                        to_remove.append(i)
                    finished = finished and result
                    # print("Finished", finished)
                num_guesses += 1

                to_remove.reverse()
                print(to_remove)
                print(len(states))
                for removal in to_remove:
                    last_state = states[removal]
                    states.remove(states[removal])


            new_guess = get_best_guess()
            if new_guess: #Otherwise already guessed
                for i in range(len(states)):
                    result = states[i].evaluate(new_guess)
                    states[i].display()

            #print(states[i].board)
            num_guesses += 1
            print("Guesses Taken", num_guesses)

            if len(states) > 0:
                last_state = states[0]

            for word in secret_words:
                if word in last_state.board:
                    correct += 1
            print("Number Puzzles got correct: ", correct)

            tot_guesses += num_guesses

        except(IndexError):
            raise IndexError
            num_error += 1
    return correct, tot_guesses, num_error

for i in range(100):
    correct, tot_guesses, num_error = run_one_octordle(correct, tot_guesses, num_error)

print(f"Correct puzzles: {correct}/800")
#print("SECRET words:", secret_words)
print("Total successes", num_success)
print("Total failures", num_fail)
print("Total errors", num_error)
print("Total guesses", tot_guesses)