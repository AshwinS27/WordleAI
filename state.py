import numpy as np

class State:

    def __init__(self, num_letters, tot_guesses, secret_word):
        self.num_letters = num_letters
        self.board = [[]] * tot_guesses # Contains each guess
        self.result = np.full((tot_guesses, num_letters), -1)
        self.alphabet = [-1] * 26
        self.alphabet_dict = {chr(i): -1 for i in range(ord('a'), ord('z') + 1)}
        self.secret_word = secret_word
        self.current_guess = 0
        self.curr_score = 0

    def display(self):
        print("GUESS NUMBER ", self.current_guess)
        print("Board: ", self.board)
        print("Result: ")
        print(self.result)
        # print("Alphabet: ", self.alphabet)
        print("Alphabet: ", self.alphabet_dict)
        print("--------------------------------------------------------")

    def get_alphabet_index(self, char):
        return ord(char.lower()) - ord('a')

    def update_board(self, i, value, guess):
        self.board[self.current_guess] = guess
        self.result[self.current_guess][i] = value
        self.alphabet[self.get_alphabet_index(guess[i])] = value
        self.alphabet_dict[guess[i]] = value
        self.curr_score += 1

    def get_new_guess(self):
        #TODO: Figure out an optimal guess
        #Use the board + result + alphabet to figur out the best guess
        return "hello"
    
    def validate_guess(self, guess):
        #TODO: Add check for valid guess
        if len(guess) == self.num_letters: #Add check for valid word in vocabulary
            return True
        

    def evaluate(self, guess):
        #TODO: Right now no check for duplicates
        chars_word = [*self.secret_word]

        for i in range(len(self.secret_word)):
            if guess[i] == self.secret_word[i]:
                self.update_board(i, 2, guess)
            elif guess[i] in chars_word:
                self.update_board(i, 1, guess)
            else:
                self.update_board(i, 0, guess)

        #Trim the alphabet
        self.alphabet_dict = {key: value for key, value in self.alphabet_dict.items() if value != 0}
        self.current_guess += 1