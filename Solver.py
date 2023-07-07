from Checkers import Game, MovePart, Color
import math
from GameState import GameState
import random


class Solver:
    def __init__(self):
        self.max_player = None

    def get_move(self, game: Game, depth: int, move_max: bool) -> list[int]:
        self.max_player = Color.WHITE
        best_moves = []
        minimum = math.inf
        maximum = -math.inf
        state = GameState(game)
        for move in state.get_possible_moves():
            piece = move[MovePart.PIECE]
            new_row = move[MovePart.ROW]
            new_column = move[MovePart.COLUMN]
            new_state = state.make_move(piece.row, piece.column, new_row, new_column)
            result = self.alfa_beta(
                new_state, depth - 1, not move_max, -math.inf, math.inf
            )
            if result > maximum and move_max:
                best_moves = [(piece.row, piece.column, new_row, new_column)]
                maximum = result
            elif result < minimum and not move_max:
                best_moves = [(piece.row, piece.column, new_row, new_column)]
                minimum = result
            elif result == minimum or result == maximum:
                best_moves.append((piece.row, piece.column, new_row, new_column))
        return random.choice(best_moves)

    def alfa_beta(
            self, state: GameState, depth: int, move_max: bool, alfa: float, beta: float
    ) -> float:
        if state.is_finished() or depth == 0:
            return state.get_heuristic_value(self.max_player)
        if move_max:
            for child in state.get_children():
                alfa = max(
                    alfa, self.alfa_beta(child, depth - 1, not move_max, alfa, beta)
                )
                if alfa >= beta:
                    return alfa
            return alfa
        else:
            for child in state.get_children():
                beta = min(
                    beta, self.alfa_beta(child, depth - 1, not move_max, alfa, beta)
                )
                if alfa >= beta:
                    return beta
            return beta
