from flask import Flask, render_template, request, redirect, url_for, jsonify
from Checkers import Game

game = Game()
app = Flask(__name__)


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


@app.route('/oneplayer', methods=["POST", "GET"])
def one_player_game():
    not_finished = True
    game.prepare_before_player_move()
    board = game.get_board_to_html()
    moves = game.get_possible_moves_to_html()
    return render_template('oneplayer.html', the_title="One player", board=board, moves=moves)


@app.route('/')
def main():
    return render_template('mainpage.html', the_title="Main page")


if __name__ == '__main__':
    app.run()
