import time

from flask import Flask, render_template, request, jsonify
from Solver import Solver
from Checkers import Game

game = Game()
solver = Solver()
app = Flask(__name__)


@app.route('/beforecomputermove', methods=["POST", "GET"])
def before_computer_move():
    board = game.get_board_to_html()
    if game.check_game_end():
        return render_template('oneplayer.html', the_title="END", board=board, moves=[],
                               white_move=game.white_move, game_end=True)
    game.prepare_before_player_move()
    if game.white_move:
        moves = game.get_possible_moves_to_html()
        title = "One player"
    else:
        moves = []
        title = "Compute move"
    return render_template('oneplayer.html', the_title=title, board=board, moves=moves,
                           white_move=game.white_move, game_end=False)


@app.route('/movepiece', methods=["POST", "GET"])
def move_piece():
    data = request.get_json()
    row = data['row']
    col = data['col']
    new_row = data['new_row']
    new_col = data['new_col']
    game.move_piece(row, col, new_row, new_col)
    response = {'message': 'Piece moved successfully'}
    return jsonify(response)


def computer_move(depth: int):
    start = time.process_time()
    max_move = False
    game.prepare_before_player_move()
    move = solver.get_move(game, depth, max_move)
    stop = time.process_time()
    if stop - start < 1:
        time.sleep(1 + stop - start)
    game.move_piece(move[0], move[1], move[2], move[3])


@app.route('/playermove', methods=["POST", "GET"])
def player_move():
    if game.check_game_end():
        board = game.get_board_to_html()
        return render_template('oneplayer.html', the_title="END", board=board, moves=[],
                               white_move=game.white_move, game_end=True)
    if not game.white_move:
        computer_move(3)
    board = game.get_board_to_html()
    game.prepare_before_player_move()
    if not game.white_move:
        return render_template('oneplayer.html', the_title="Computer move", board=board, moves=[],
                               white_move=game.white_move, game_end=False)
    moves = game.get_possible_moves_to_html()
    return render_template('oneplayer.html', the_title="One player", board=board, moves=moves,
                           white_move=game.white_move, game_end=False)


@app.route('/oneplayer', methods=["POST", "GET"])
def one_player_game_start():
    game.reset()
    game.prepare_before_player_move()
    board = game.get_board_to_html()
    moves = game.get_possible_moves_to_html()
    return render_template('oneplayer.html', the_title="One player", board=board, moves=moves,
                           white_move=game.white_move, game_end=False)


@app.route('/')
def main():
    return render_template('mainpage.html', the_title="Main page")


if __name__ == '__main__':
    app.run()
