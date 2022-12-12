# WordleClone
A Flask REST Framework API of Wordle.

This is a Python implementation of [Wordle](https://www.nytimes.com/games/wordle/index.html) that copies the same 
logic and gameplay seen in the popular daily word game.

This project was developed using Python 3.9, but should support versions 3.6 and beyond.

## Getting Started
There are only two non-standard libraries used to build this progam: `Flask` and `Flask-RESTful`. The specific
versions are listed in the `requirements.txt` file, and may be installed with Python's package installer with the
following command:

```bash
pip install -r requirements.txt
```

## Usage
To run this code, the user must first launch the Flask server in `main.py`, as seen below. 
```bash
python main.py
```

There are two commands that can be called with this API:
* http://localhost/new_game/
    * This creates a new Wordle game for the user to play. 
    * This must be called before the user is able to make any guesses, 
    but may be called at any time to create a new game. 
* http://localhost/guess/
    * This allows the user to make a guess for the current game. 
    * A maximum of 6 (valid) guesses are allowed to be made before the 
    game tells you the answer. 
    * Invalid guesses (not a real word, doesn't have 5 letters) will alert 
    the user to the type of error they have made.

Samples of the command being called from the command line are included below along with sample outputs. 

<b>New Game</b>
```bash
curl http://localhost:5000/new_game/ -X POST
```
```json
{
  "game_id": 862137
}
```

<b>Guess Word</b>
```bash
curl http://localhost:5000/guess/ -H "Content-Type: application/json" -d "{\"word\": \"layer\", \"game_id\": 123456}" -X POST
```
** Note: The backslashes for the json data is required on Windows as the command line doesn't recognize single quotes
around JSON data.  
```json
{
  "letter1": "incorrect", 
  "letter2": "incorrect", 
  "letter3": "incorrect", 
  "letter4": "wrong position", 
  "letter5": "wrong position", 
  "guess_result": "incorrect", 
  "incorrectly_guessed_letters": ["A", "Y", "L"], 
  "known_letters_in_word": ["E", "R"], 
  "known_letters": "*****", 
  "guesses_remaining": 5
}
```
The output for guessing a word includes the following:
* Which letters were correct, wrong, or in the wrong position
* The overall result of the guess
* The cumulatively known incorrect and known letters
* A representation of the currently known letters
* An indicator for how many guesses the user has left in the current game