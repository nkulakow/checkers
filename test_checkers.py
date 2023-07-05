import pytest
from Checkers import Game
from checkers_exceptions import NoPawnToCapture, NonexistentBoardField, InvalidMove, OccupiedField


def test_Game_check_move_valid_throw_InvalidMove():
    game = Game()
    with pytest.raises(InvalidMove):
        game._check_simple_move_valid(1, 1, 4, 4)
    with pytest.raises(InvalidMove):
        game._check_simple_move_valid(4, 4, 3, 4)
    with pytest.raises(InvalidMove):
        game._check_simple_move_valid(5, 5, 7, 4)


def test_Game_check_move_valid_throw_OccupiedField():
    game = Game()
    with pytest.raises(OccupiedField):
        game._check_capture_move_valid(1, 1, 3, 3)


def test_Game_check_move_valid_throw_NonexistentBoardField():
    game = Game()
    with pytest.raises(NonexistentBoardField):
        game._check_simple_move_valid(1, 1, 9, 9)


def test_Game_check_move_valid_throw_NoPawnToCapture():
    game = Game()
    with pytest.raises(NoPawnToCapture):
        game._check_capture_move_valid(3, 1, 5, 3)
    with pytest.raises(NoPawnToCapture):
        game._check_capture_move_valid(2, 2, 4, 4)
    with pytest.raises(NoPawnToCapture):
        game.prepare_before_player_move()
        game.move_piece(3, 1, 4, 2)
        game._check_capture_move_valid(7, 1, 5, 3)


def test_Game_check_move_valid_no_throw():
    game = Game()
    game._check_simple_move_valid(3, 1, 4, 2)


def test_Game_possible_moves_first():
    game = Game()
    game.prepare_before_player_move()
    possible_moves = game.possible_moves
    assert len(possible_moves) == 7


def test_Game_check_king_moves():
    game = Game()
    piece = game.get_piece(3, 3)
    game._check_king_able_to_simple_move(piece)
    assert len(game.possible_moves) == 4


def test_Game_check_king_capture_moves():
    game = Game()
    game.prepare_before_player_move()
    king = game.get_piece(6, 6)
    game.move_piece(3, 3, 4, 4)
    game._possible_moves = []
    game._check_king_able_to_capture(king)
    assert len(game.possible_moves) == 1


def test_Game_make_king():
    game = Game()
    new_king = game.get_piece(3, 3)
    first_deleted = game.get_piece(7, 3)
    second_deleted = game.get_piece(8, 2)
    game._board[7][3] = new_king
    new_king.change_position(7, 3)
    game._board[3][3] = None
    game._board[8][2] = None
    game.black_player.remove_piece(first_deleted)
    game.black_player.remove_piece(second_deleted)
    game.prepare_before_player_move()
    game.move_piece(7, 3, 8, 2)
    assert new_king.is_King


def test_end_game():
    game = Game()
    b_player = game.black_player
    b_player._pieces = []
    game.prepare_before_player_move()
    game.move_piece(3, 3, 4, 4)
    assert game.check_game_end()
