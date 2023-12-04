import state
import json
import random
import matplotlib.pyplot as plt
import numpy as np

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
loses = []

player_1 = True #Start with player 1, if false = player 2

result_arr = []
p1_wins = []
p2_wins = []


for i in range(1000):

    # player_1 = True
    if i % 2 == 0:
        player_1 = True
    else:
        player_1 = False

    try:
        secret_word = random.choice(word_list) #erred
        print("SECRET WORD: " + secret_word)

        my_state = state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word, multiplayer=False)
        state_two = state.State(NUM_LETTERS, TOTAL_GUESSES, secret_word, multiplayer=True)

        print("FIRST PLAYER FIRST?: ", player_1)
        finished = my_state.evaluate("crane")
        state_two.evaluate("crane")
        #my_state.display()

        # my_state.evaluate("toils")
        # my_state.display()

        num_guesses = 1

        

        while not finished and num_guesses < TOTAL_GUESSES:
            if player_1:
                new_guess = my_state.get_new_guess()
            else:
                new_guess = state_two.get_new_guess()

            player1 = not player_1

            finished = my_state.evaluate(new_guess)

            state_two.evaluate(new_guess)
            state_two.display()
            num_guesses += 1

        # print("Secret word", secret_word)
        # print("Guesses Taken", num_guesses)

        # my_state.display()
        # print("Guess Number", num_guesses)
        # print("Player 1: ", player_1)
        if not finished:
            num_fail += 1
            result_arr.append(-1)
            p2_wins.append(0)
            p1_wins.append(0)
            loses.append(1)

        else:
            loses.append(0)
            num_success += 1
            if not player_1: ### Player 1 becomes true when Player 2 guesser is used...
                player_1_wins += 1
                result_arr.append(1)
                p1_wins.append(1)
                p2_wins.append(0)
            else:
                player_2_wins += 1
                result_arr.append(2)
                p2_wins.append(1)
                p1_wins.append(0)
        tot_guesses += num_guesses

    except(IndexError):
        raise IndexError
        num_error += 1

def plot_cumulative_wins(player1_wins, player2_wins, loses):
    cumulative_player1 = np.cumsum(player1_wins)
    cumulative_player2 = np.cumsum(player2_wins)
    cum_loss = np.cumsum(loses)

    plt.plot(cumulative_player1, label='Player 1')
    plt.plot(cumulative_player2, label='Player 2')
    plt.plot(cum_loss, label='Overall Losses')

    plt.xlabel('Game Number')
    plt.ylabel('Cumulative Wins')
    plt.title('Cumulative Wins of Player 1 and Player 2 Over Time')

    plt.legend()
    plt.show()

print("Total successes", num_success)
print("Total failures", num_fail)
print("Total errors", num_error)
print("Total guesses", tot_guesses)
print("Player 1 Wins", player_1_wins)
print("Player 2 wins", player_2_wins)

plot_cumulative_wins(p1_wins, p2_wins, loses)
# plt.plot(p1_wins)
# plt.plot(p2_wins)
# plt.show()