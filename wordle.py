from collections import Counter
import hashlib
import random
import re


class Wordle:
    """An implementation of the NY Times Wordle game [https://www.nytimes.com/games/wordle/index.html].
    Users must guess an unknown 5 letter word within 6 attempts. Words that are guessed are evaluated
    against the hidden word, and the user is informed of whether guessed letters are in the correct
    spot, are in the wrong position, or aren't in the word at all."""
    def __init__(self):
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
        """Creates a new Wordle game.

        Randomly selects a word from the provided word list, creates a game_id based off of
        a hashing of the selected word, and resets relevant information for the game state
        (e.g. number of guesses, letters that have been guessed, etc.)"""
        # Select random word to guess
        self.current_word = random.choice(self.word_list)
        self.current_word = 'marry'
        # Generate a unique-ish id for the game derived from the word
        # Note: 'unique-ish' is due to trimming hash to last 6 digits
        m = hashlib.md5()
        m.update(self.current_word.encode("utf-8"))
        self.game_id = int(m.hexdigest(), 16) % (10**6)
        # Reset relevant game state information
        self.num_guesses = 0
        self.incorrectly_guessed_letters = []
        self.known_letters_in_word = []
        self.known_letters = ['*'] * self.word_length
        self.is_word_guessed = False

    def can_guess(self):
        """Determines whether Wordle can currently guess a word.

        :return: Boolean for whether the current game state can make guesses.

        Wordle can only make a guess if the game has started (i.e. already has a `current_word`),
        there are less than 6 guesses, and the user has not already guessed the word."""
        return self.current_word and (self.num_guesses < self.max_num_guesses) and (not self.is_word_guessed)

    def is_valid_guess(self, word: str):
        """Determines if the user-provided word is a valid guess.

        :param word: The user-provided word.
        :return: Boolean for whether the user's word is valid.

        A valid guess must be in our list of words and be exactly 5 characters."""
        return word.lower() in self.word_list and len(word) == self.word_length

    def make_guess(self, word: str):
        """Evaluate the user-provided word against the current game. The results are stored in `guess_result`
        which are then passed back to inform the user about how their guess matched up against the actual
        word.

        :param word: The user-provided word.
        :return guess_result: A dictionary containing all the relevant information for the current game
            state to allow the user to make informed decisions for future guesses.
        """
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
            # If guess is incorrect, store result, wrong letter, and indicate word is not a match
            elif letter_guess not in self.current_word:
                incorrectly_guessed_letters.append(letter_guess.upper())
                guess_result[f"letter{i + 1}"] = "incorrect"
                is_match = "incorrect"
            # If guess is in word, but different spot
            elif letter_guess in self.current_word:
                # Need to consider edge cases of a letter occurring multiple times in guess v. once in actual
                # I.E. We don't want the user to assume a letter occurs more often than it actually does
                # If the number of positive matches of a specific letter and the current letter's cardinality
                #   in the guessed word are less than the total frequency, that letter will be tagged in the
                #   wrong position, otherwise, it will be marked as a wrong letter

                # Frequency of specified letter in actual word
                cnt = Counter(self.current_word)
                letter_frequency = cnt[letter_guess]
                # Number of positive matches made in current guess with specific letter
                positive_matches = sum([1 for l1, l2 in zip(word, self.current_word) if l1 == l2 and letter_guess == l1])
                # Determine the cardinality of the specified letter's occurrence in the guessed word
                letter_indices = [i.start() for i in re.finditer(letter_guess, word)]
                letter_cardinality = letter_indices.index(i)

                if positive_matches + letter_cardinality < letter_frequency:
                    guess_result[f"letter{i + 1}"] = "wrong position"
                else:
                    guess_result[f"letter{i + 1}"] = "incorrect"

                known_letters_in_word.append(letter_guess.upper())
                is_match = "incorrect"

        # Store our results to return the server
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
