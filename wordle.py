# Comments are terminal commands that must be run for the program to work. 
# Make sure to restart your IDE after.
import numpy as np # pip install numpy
import random
from termcolor import colored # pip install termcolor in cmd prompt
import os
import requests # pip install requests in cmd prompt
github_answers_url = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/1792f853e1cd0249f7588c724e00d46dbc4894eb/wordle-answers-alphabetical.txt"
github_guesses_url = "https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/b8375870720504ecf89c1970ea4532454f12de94/wordle-allowed-guesses.txt"
response = requests.get(github_answers_url)
if response.status_code == 200:
    allowed_answers = response.text.splitlines()
else:
    print("Failed to fetch the file from GitHub.")
response = requests.get(github_guesses_url)
if response.status_code == 200:
    allowed_guesses = allowed_answers + response.text.splitlines()
else:
    print("Failed to fetch the file from GitHub.")
class Wordle_Game:
    def __init__(self, allowed_guesses, allowed_answers):
        self.board = np.empty((6, 5), dtype=object)
        self.correct_word = random.choice(allowed_answers)
        self.grayed_letters = set([])
        self.guess_count = 0
        self.current_word_index = 0
        self.words_list = allowed_guesses

    def update_board(self, colored_word):
        self.board[self.current_word_index] = colored_word
        self.current_word_index += 1
        self.print_board()

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n")
        for row in self.board:
            if any(letter is not None for letter in row):
                for letter in row:
                    letter = str(f"{letter}")
                    if letter != "None":
                        print(letter, end=" ")
                    else:
                        print(" ", end=" ")
                print("\n")
    def color_words(self, guess):
        correct_word = list(self.correct_word)
        guess = list(guess)
        colored_letters = []
        correct_letter_count = {letter: correct_word.count(letter) for letter in set(correct_word)}
        guess_letter_count = {letter: 0 for letter in set(correct_word)}
        
        for index, letter in enumerate(guess):
            if letter == correct_word[index]:
                letter_color = "green"
            elif letter in correct_word:
                guess_letter_count[letter] += 1
                if guess_letter_count[letter] <= correct_letter_count[letter]:
                    letter_color = "yellow"
                else:
                    letter_color = "grey"
            else:
                letter_color = "grey"
                self.grayed_letters.add(letter)
            colored_letters.append(colored(letter, letter_color))
            
        self.update_board(colored_letters)
        return colored_letters

    def guess(self):
        words_list = self.words_list
        while True:
            guess = input("Enter a 5 letter word: ").lower()
            if guess in words_list:
                break
            else:
                print("Invalid word. Please guess again: ")
        self.color_words(guess)
        return guess
    def start_game(self):
        remaining_letters = list("abcdefghijklmnopqrstuvwxyz")
        while True:
            guess = self.guess()
            self.guess_count += 1
            guessed_letters = set(guess)
            remaining_letters = [letter for letter in remaining_letters if letter not in guessed_letters or (letter in guessed_letters and letter in self.correct_word)]
            
            print(f"Available Letters for Guessing: \n")
            for letter in remaining_letters:
                print(letter, end=" ")
            print("\n")
            
            if guess == self.correct_word:
                print(f"Congrats! You guessed the word on guess {self.guess_count}.")
                break
            elif self.guess_count == 6:
                print(f"You ran out of guesses! The word was {self.correct_word}.")
                break
wordle = Wordle_Game(allowed_guesses, allowed_answers)
wordle.start_game()