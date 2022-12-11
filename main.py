from flask import Flask
from flask_restful import Resource, Api
from wordle import Wordle


app = Flask("WordleAPI")
api = Api(app)

current_game = Wordle()


class Game(Resource):
    """Resource to be called for generating a new Wordle game."""
    def put(self):
        current_game.create_new_game()
        response = {
            'game_id': current_game.game_id
        }
        return response


class Guess(Resource):
    """Resource to be called for guessing words in Wordle game."""
    def put(self, game_id, word):
        # Check if we can even make a guess with current game state
        if current_game.can_guess():
            # Check if querying the correct game
            if game_id == current_game.game_id:
                if current_game.is_valid_guess(word):
                    result = current_game.make_guess(word)
                    return result
                else:
                    if len(word) != current_game.word_length:
                        return 'Please make sure guesses have 5 letters', 400
                    else:
                        return 'Please make sure guesses are valid words', 400
            else:
                return f"Did you mean to query game_id:{current_game.id}", 400
        # Cannot make guesses currently
        else:
            if current_game.num_guesses == current_game.max_num_guesses:
                return "You've reached the maximum number of guesses - please start a new game", 400
            else:
                return "You need to start a new game before you start guessing", 400


api.add_resource(Game, '/new_game/')
api.add_resource(Guess, '/guess/<int:game_id>/<string:word>')


if __name__ == "__main__":
    app.run()