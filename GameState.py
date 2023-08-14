from Checkers import Game, Color, MovePart
import copy

from checkers_exceptions import NoPieceChosen


class GameState:
    def __init__(self, game: Game):
        self._game = game
        self._game.prepare_before_player_move()

    def make_move(self, old_row: int, old_column: int, new_row: int, new_column: int):
        game = copy.deepcopy(self._game)
        game.move_piece(old_row, old_column, new_row, new_column)
        return GameState(game)

    def get_possible_moves(self):
        return self._game.possible_moves

    def is_finished(self):
        return self._game.check_game_end()

    def get_children(self):
        if self.is_finished():
            return None
        children = []
        self._game.prepare_before_player_move()
        for move in self.get_possible_moves():
            piece = move[MovePart.PIECE]
            try:
                new_child = self.make_move(piece.row, piece.column, move[MovePart.ROW], move[MovePart.COLUMN])
                children.append(new_child)
            except NoPieceChosen:
                print("Raised error No piece chosen")
            except KeyError:
                print("key error was raised")
        return children

    def get_winner(self):
        return self._game.winner

    def payoff(self, max_player: Color) -> int:
        if self.get_winner() == max_player:
            return 1
        elif self.get_winner():
            return -1
        else:
            return 0

    def get_heuristic_value(self, max_player: Color) -> float:
        if self.is_finished():
            return self.payoff(max_player)
        if self._game.white_move:
            current_player = Color.WHITE
            other_player = Color.BLACK
        else:
            current_player = Color.BLACK
            other_player = Color.WHITE
        factor = 1 if max_player == current_player else - 1
        if any(piece.is_King for piece in self._game.get_player_pieces(current_player)):
            kings = [piece for piece in self._game.get_player_pieces(current_player) if piece.is_King]
            other_kings = [piece for piece in self._game.get_player_pieces(other_player) if piece.is_King]
            return factor * len(kings) / (12 + len(other_kings))
        return factor * len(self._game.get_player_pieces(current_player)) / (
                12 + len(self._game.get_player_pieces(other_player)))
