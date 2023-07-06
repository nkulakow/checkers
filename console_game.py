from Solver import Solver
from Checkers import Game
from checkers_exceptions import InvalidMove, NoPieceChosen


def computermove(game: Game, depth: int, max_move: bool, solver: Solver) -> bool:
    game.print_board_console()
    game.prepare_before_player_move()
    white_move = game.white_move
    move = solver.get_move(game, depth, max_move)
    if len(move) == 0:
        print("You won!")
        return True
    game.move_piece(move[0], move[1], move[2], move[3])
    if game.check_game_end():
        print("You lost!")
        return False
    if game.white_move == white_move:
        return computermove(game, depth, max_move, solver)
    return True


def gamermove(game: Game) -> bool:
    game.print_board_console()
    game.prepare_before_player_move()
    white_move = game.white_move
    move_not_made = True
    while move_not_made:
        try:
            old_row = int(input("Old row: "))
            old_column = int(input("Old column: "))
            new_row = int(input("New row: "))
            new_column = int(input("New column: "))
            game.move_piece(old_row, old_column, new_row, new_column)
            move_not_made = False
        except InvalidMove:
            print("It is invalid move, try again")
        except NoPieceChosen:
            print("No piece was chosen")
    if game.check_game_end():
        print("You won!")
        return False
    if game.white_move == white_move:
        return gamermove(game)
    return True


def play(game: Game, depth: int, solver: Solver):
    not_finished = True
    while not_finished:
        not_finished = gamermove(game)
        if not_finished:
            not_finished = computermove(game, depth, False, solver)


def main():
    depth = int(input("Computers depth: "))
    game = Game()
    solver = Solver()
    play(game, depth, solver)


if __name__ == "__main__":
    main()
