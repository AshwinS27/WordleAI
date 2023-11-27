import numpy as np
import json
import random
from collections import Counter

class State:

    def __init__(self, num_letters, tot_guesses, secret_word):
        self.max_guesses = tot_guesses
        self.num_letters = num_letters
        self.board = [[]] * tot_guesses # Contains each guess
        self.result = np.full((tot_guesses, num_letters), -1)
        self.alphabet_dict = {chr(i): -1 for i in range(ord('a'), ord('z') + 1)}
        self.secret_word = secret_word
        self.current_guess = 0
        self.curr_score = 0
        self.last_guess = ""
        self.good_word = True
        self.counter = Counter()

    def display(self):
        print("GUESS NUMBER ", self.current_guess)
        print("Board: ", self.board)
        print("Result: ")
        print(self.result)
        print("Alphabet: ", self.alphabet_dict)
        print("--------------------------------------------------------")

    def get_alphabet_index(self, char):
        return ord(char.lower()) - ord('a')

    def update_board(self, i, value, guess):
        self.board[self.current_guess] = guess
        self.result[self.current_guess][i] = value
        if guess[i] in self.alphabet_dict:
            self.alphabet_dict[guess[i]] = max(value, self.alphabet_dict[guess[i]])
        self.curr_score += 1

    def get_words_consistent_with_2(self, vocab_in):
        #Remove words which don't contain '2' letters
        letters_in_place = [key for key, value in self.alphabet_dict.items() if value > 1]

        if letters_in_place:
            last_guess = self.board[self.current_guess-1]

            def get_all_indices(word, letter):
                return [i for i in range(len(word)) if word[i] == letter]

            letter_indices = [get_all_indices(last_guess, letter) for letter in letters_in_place]
            filter_letter_indices = []
            repeated_letters_in_place = []
            for index_set, letter in zip(letter_indices, letters_in_place):
                for index in index_set:
                    if self.result[self.current_guess-1][index] == 2: #Only keep it if correct place
                        filter_letter_indices.append(index)
                        repeated_letters_in_place.append(letter)

            #Remove words which don't have letters with score 2 in correct place
            def filter_words(vocabulary):
                filtered_vocabulary = []

                for word in vocabulary:
                    if all(word[i] == letter for i, letter in zip(filter_letter_indices, repeated_letters_in_place)):
                        filtered_vocabulary.append(word)

                return filtered_vocabulary
            
            return filter_words(vocab_in)
        else:
            return vocab_in
        
    def get_new_guess(self):
        possible_letters = self.alphabet_dict.keys()

        with open("wordle_list.json", "r") as wordle_list:
            vocabulary = json.load(wordle_list)

        valid_words = []
        #Step 1: Eliminate words which dont have letters in the dictionary
        for word in vocabulary:
            if len(word) == 5 and set(word).issubset(set(possible_letters)):
                valid_words.append(word)

        filtered_vocab = [key for key, value in self.alphabet_dict.items() if value > 0]

        #Remove words which don't contain '1' letters
        filtered_vocab = [word for word in valid_words if set(filtered_vocab).issubset(set(word))]

        #Remove words not consistent with '2' letters
        filtered_vocab = self.get_words_consistent_with_2(filtered_vocab)

        ##TODO: Remove words which have letters with score 1 == definitely in the wrong place
        ## If word is crane == [0 0 1 0 0] --> we include all words which have 'a' but dont have crne --> ALREADY DONE
        ## WHAT WE DONT HAVE RN --> We are not removing words which have __a__ in the second index

        #Get respective index of each '1' letter
        #Remove words which have '1' letter in last guess spot

        is_new = False

        #TODO: This doesn't work?? --> gets stuck in infinite loop
        #This tries to find a non-repeated work from the filtered vocab
        # while not is_new:
        #     next_guess = random.choice(filtered_vocab)
        #     if not next_guess in self.board:
        #         is_new = True
        #         return random.choice(filtered_vocab)

        if len(filtered_vocab) == 1 and self.current_guess < self.max_guesses - 1:
            print(self.board[self.current_guess-1])
            print(filtered_vocab)
            next_guess = self.board[self.current_guess-1]
        else:
            next_guess = random.choice(filtered_vocab)
        
        return next_guess

        #Ideally we want some metric that we can then use to potentially gain a "not best" guess
        #Will be useful for the competitive wordle

    
    def validate_guess(self, guess):
        with open('wordle_list.json', 'r') as wordle_list:
            valid = json.load(wordle_list)
        if guess in valid:
            self.good_word = True
        else:
            self.good_word = False
        return self.good_word

    def evaluate(self, guess):
        chars_word = [*self.secret_word]
        feedback = ["-"] * len(self.secret_word)
        self.counter = Counter()

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
            elif guess[i] in chars_word and self.counter[guess[i]] > self.secret_word.count(guess[i]):
                self.update_board(i, 0, guess)
                feedback[i] = "-"

        #Trim the alphabet
        self.alphabet_dict = {key: value for key, value in self.alphabet_dict.items() if value != 0}
        self.current_guess += 1
        self.display()

        if guess == self.secret_word:
            print("YOU HAVE SOLVED THE WORDLE!!")
            print("------------------------------------")
            return True