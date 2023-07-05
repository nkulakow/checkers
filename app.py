from flask import Flask
from Checkers import Game

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    game = Game()
    moves = [
        (3, 1, 4, 2),
        (6, 2, 5, 1),
        (4, 2, 5, 3),
        (6, 4, 4, 2),
        (3, 3, 4, 4),
        (6, 8, 5, 7),
        (4, 4, 5, 3),
        (7, 7, 6, 8),
        (3, 5, 4, 4),
        (8, 8, 7, 7),
        (5, 3, 6, 2),
        (7, 1, 5, 3),
        (5, 3, 3, 5)
    ]
    game.print_board_console()
    game.prepare_before_player_move()
    print(game.possible_moves)
    for old_row, old_column, new_row, new_column in moves:
        game.move_piece(old_row, old_column, new_row, new_column)
        if game.check_game_end():
            print("END")
        game.print_board_console()
        game.prepare_before_player_move()
        print(game.possible_moves)

    #app.run()
