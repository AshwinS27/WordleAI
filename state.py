import numpy as np
import json
import random

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
        self.last_guess = ""

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
        possible_letters = self.alphabet_dict.keys()

        with open("wordle_list.json", "r") as wordle_list:
            vocabulary = json.load(wordle_list)

        valid_words = []
        #Step 1: Eliminate words which dont have letters in the dictionary
        for word in vocabulary:
            if len(word) == 5 and set(word).issubset(set(possible_letters)):
                valid_words.append(word)

        letters_in_word = [key for key, value in self.alphabet_dict.items() if value > 0]

        #Remove words which don't contain '1' letters
        filtered_vocab = [word for word in valid_words if set(letters_in_word).issubset(set(word))]

        #TODO: HOW TO HANDLE THIS WHEN THERE ARE DUPLICATES??
        #Remove words which don't contain '2' letters
        letters_in_place = [key for key, value in self.alphabet_dict.items() if value > 1]

        if letters_in_place:
            last_guess = self.board[self.current_guess-1]
            letter_indices = [last_guess.index(letter) for letter in letters_in_place]
            
            def filter_words(vocabulary):
                filtered_vocabulary = []

                for word in vocabulary:
                    if all(word[i] == letter for i, letter in zip(letter_indices, letters_in_place)):
                        filtered_vocabulary.append(word)

                return filtered_vocabulary
            
            filtered_vocab = filter_words(filtered_vocab)

        is_new = False

        #TODO: This doesn't work?? --> gets stuck in infinite loop
        #This tries to find a non-repeated work from the filtered vocab
        # while not is_new:
        #     next_guess = random.choice(filtered_vocab)
        #     if not next_guess in self.board:
        #         is_new = True
        #         return random.choice(filtered_vocab)
        
        next_guess = random.choice(filtered_vocab)
        return next_guess

        #Ideally we want some metric that we can then use to potentially gain a "not best" guess
        #Will be useful for the competitive wordle

        return "hello"
    
    def validate_guess(self, guess):
        #TODO: Add check for valid guess
        if len(guess) == self.num_letters: #Add check for valid word in vocabulary
            return True
        

    def evaluate(self, guess):
        #TODO: Right now no check for duplicates
        chars_word = [*self.secret_word]
        feedback = ["-"] * len(self.secret_word)

        # finding letters in right place
        for i in range(len(self.secret_word)):
            if guess[i] == self.secret_word[i]:
                self.update_board(i, 2, guess)
                feedback[i] = "X"
                self.counter[guess[i]] += 1
            elif guess[i] in chars_word:
                self.update_board(i, 1, guess)
                feedback[i] = "O"
                self.counter[guess[i]] += 1
            else:
                self.update_board(i, 0, guess)
        
        # finding letters that are out of place
        for i in range(len(self.secret_word)):
            if feedback[i] == "X":
                continue
            elif guess[i] in chars_word and self.counter[guess[i]] < self.secret_word.count(guess[i]):
                self.update_board(i, 1, guess)
                feedback[i] = "O"
                self.counter[guess[i]] += 1

        #Trim the alphabet
        self.alphabet_dict = {key: value for key, value in self.alphabet_dict.items() if value != 0}
        self.current_guess += 1
        # self.display()

        if guess == self.secret_word:
            print("YOU HAVE SOLVED THE WORDLE!!")
            print("------------------------------------")
            return True