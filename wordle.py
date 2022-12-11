import hashlib
import random


class Wordle:
    def __init__(self):
        # Read in our list of valid words
        with open('words.txt') as f:
            self.word_list = f.read().splitlines()
        self.num_guesses = 0
        self.max_num_guesses = 6
        self.word_length = 5
        self.game_id = None
        self.current_word = None
        self.incorrectly_guessed_letters = []
        self.known_letters_in_word = []
        self.known_letters = []
        self.is_word_guessed = False

    def create_new_game(self):
        # Select random word to guess
        self.current_word = random.choice(self.word_list)
        # Generate a unique-ish id for the game derived from the word
        # Note: 'unique-ish' is due to trimming hash to last 6 digits
        m = hashlib.md5()
        m.update(self.current_word.encode("utf-8"))
        self.game_id = int(m.hexdigest(), 16) % (10**6)
        # Reset number of guesses and wrongly guessed letters
        self.num_guesses = 0
        self.incorrectly_guessed_letters = []
        self.known_letters_in_word = []
        self.known_letters = ['*'] * self.word_length
        self.is_word_guessed = False

    def can_guess(self):
        # There is a current word, less than 6 guesses, and word not already guessed
        return self.current_word and (self.num_guesses < self.max_num_guesses) and (not self.is_word_guessed)

    def is_valid_guess(self, word):
        # User's guess is in list of words and has 5 characters
        return word.lower() in self.word_list and len(word) == self.word_length

    def make_guess(self, word):
        # Increment our number of guesses
        self.num_guesses += 1

        word = word.lower()

        guess_result = {}
        is_match = "correct"
        incorrectly_guessed_letters = []
        known_letters_in_word = []
        # Iterate over each index of guessed word and actual
        for i, (letter_guess, letter_actual) in enumerate(zip(word, self.current_word)):
            # If guess is correct, store result
            if letter_guess == letter_actual:
                self.known_letters[i] = letter_guess.upper()
                known_letters_in_word.append(letter_guess.upper())
                guess_result[f"letter{i+1}"] = "correct"
            # If guess is in word, but different spot
            elif letter_guess in self.current_word:
                known_letters_in_word.append(letter_guess.upper())
                guess_result[f"letter{i+1}"] = "wrong position"
                is_match = "incorrect"
            # If guess is incorrect, store result, wrong letter, and indicate word is not a match
            else:
                incorrectly_guessed_letters.append(letter_guess.upper())
                guess_result[f"letter{i + 1}"] = "incorrect"
                is_match = "incorrect"

        # Add overall guess result and incorrect letters
        guess_result["guess_result"] = is_match
        if is_match == "correct":
            self.is_word_guessed = True
        # Update wrong letters
        self.incorrectly_guessed_letters.extend(incorrectly_guessed_letters)
        self.incorrectly_guessed_letters = list(set(self.incorrectly_guessed_letters))
        guess_result["incorrectly_guessed_letters"] = self.incorrectly_guessed_letters
        # Update known letters
        self.known_letters_in_word.extend(known_letters_in_word)
        self.known_letters_in_word = list(set(self.known_letters_in_word))
        guess_result["known_letters_in_word"] = self.known_letters_in_word
        # Add what we know so far
        guess_result["known_letters"] = ''.join(self.known_letters)
        # Add general info that's useful to know
        guess_result["guesses_remaining"] = self.max_num_guesses - self.num_guesses

        # If we've reached max number of guesses, include answer
        if self.num_guesses >= self.max_num_guesses:
            guess_result["correct_answer"] = self.current_word.upper()

        return guess_result
