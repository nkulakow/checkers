from enum import Enum
import checkers_exceptions as ch_exc


class Color(Enum):
    WHITE = 0
    BLACK = 1


class MovePart(Enum):
    PIECE = 0
    ROW = 1
    COLUMN = 2


class Piece:
    def __init__(self, color: Color, row: int, column: int):
        self._color = color
        self._row = row
        self._column = column
        self._is_King = False

    @property
    def color(self):
        return self._color

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def is_King(self):
        return self._is_King

    def make_King(self):
        self._is_King = True

    def change_position(self, new_row: int, new_column: int):
        self._row = new_row
        self._column = new_column


class Player:
    def __init__(self, name: str, color: Color):
        self._name = name
        self._color = color
        self._pieces = []

    @property
    def color(self):
        return self._color

    @property
    def pieces(self):
        return self._pieces

    def add_piece(self, piece: Piece):
        self._pieces.append(piece)

    def remove_piece(self, piece: Piece):
        try:
            self._pieces.remove(piece)
        except ValueError:
            if piece is not None:
                for old_piece in self._pieces:
                    if old_piece.row == piece.row and old_piece.column == piece.column:
                        self._pieces.remove(old_piece)
                        break

    @property
    def loser(self):
        return len(self._pieces) == 0


class Game:
    def __init__(self, white_name: str = None, black_name: str = None):
        self._board = {}
        self._create_board()
        self._white_player = Player(white_name, Color.WHITE)
        self._black_player = Player(black_name, Color.BLACK)
        self._assign_pieces()
        self._white_move = True
        self._possible_moves = []
        self._must_capture = False
        self._winner = None

    @property
    def white_player(self):
        return self._white_player

    @property
    def black_player(self):
        return self._black_player

    @property
    def possible_moves(self):
        return self._possible_moves

    @property
    def winner(self):
        return self._winner

    @property
    def white_move(self):
        return self._white_move

    @property
    def must_capture(self):
        return self._must_capture

    def _create_board(self):
        for row in range(1, 9):
            self._board[row] = {}
            for column in range(1, 9):
                self._board[row][column] = None

    def _put_piece(self, color: Color, row: int, column: int):
        new_piece = Piece(color, row, column)
        self._white_player.add_piece(new_piece) if color == Color.WHITE else self._black_player.add_piece(new_piece)
        self._board[row][column] = new_piece

    def get_piece(self, row: int, column: int) -> Piece | None:
        return self._board[row][column]

    def _assign_pieces(self):
        column_list = [2, 4, 6, 8]
        for row in [1, 2, 3, 6, 7, 8]:
            column_list = [2, 4, 6, 8] if column_list[0] == 1 else [1, 3, 5, 7]
            color = Color.WHITE if row <= 3 else Color.BLACK
            for column in column_list:
                self._put_piece(color, row, column)

    def print_board_console(self):
        print("  ", "  ".join("12345678"))
        for row in range(8, 0, -1):
            print(row, end="  ")
            for column in self._board[row].keys():
                if not self._board[row][column]:
                    print("-", end="  ")
                else:
                    if self._board[row][column].is_King:
                        print("W*", end=" ") if self._board[row][column].color == Color.WHITE else print("B*", end=" ")
                    else:
                        print("W", end="  ") if self._board[row][column].color == Color.WHITE else print("B", end="  ")
            print("")

    def move_piece(self, old_row: int, old_column: int, new_row: int, new_column: int):
        piece = self._board[old_row][old_column]
        if piece is None:
            raise ch_exc.NoPieceChosen
        elif (piece.color == Color.WHITE and not self._white_move) or (piece.color == Color.BLACK and self._white_move):
            raise ch_exc.InvalidPieceChosen
        self.check_move_valid(piece, new_row, new_column)
        self._move_piece(piece, new_row, new_column)

    def prepare_before_player_move(self):
        self._get_possible_capture_moves()
        if not self._must_capture:
            self._get_possible_simple_moves()

    def check_game_end(self) -> bool:
        if self._white_player.loser:
            self._winner = self._black_player
            return True
        elif self._black_player.loser:
            self._winner = self._white_player
            return True
        return False

    def _move_piece(self, piece: Piece, new_row: int, new_column: int):
        if not self._must_capture:
            self._change_position_on_board(piece, new_row=new_row, new_column=new_column)
            self._check_if_king(piece)
        else:
            self._capture_piece(piece, new_row=new_row, new_column=new_column)
            self._change_position_on_board(piece, new_row=new_row, new_column=new_column)
            self._check_if_king(piece)
            self._possible_moves = []
            self._check_piece_able_to_capture(piece)
            if len(self._possible_moves) != 0:
                return
        self._white_move = not self._white_move

    def check_move_valid(self, piece: Piece, new_row: int, new_column: int):
        for move in self._possible_moves:
            if move[MovePart.PIECE] == piece and new_row == move[MovePart.ROW] and new_column == move[MovePart.COLUMN]:
                return
        raise ch_exc.InvalidMove

    def _check_simple_move_valid(self, old_row: int, old_column: int, new_row: int, new_column: int):
        move_shift = 1 if self._white_move else -1
        if new_row not in [_ for _ in range(1, 9)] or new_column not in [_ for _ in range(1, 9)]:
            raise ch_exc.NonexistentBoardField
        elif new_row - old_row == move_shift and abs(new_column - old_column) == 1:
            if self._board[new_row][new_column]:
                raise ch_exc.OccupiedField
            else:
                return
        else:
            raise ch_exc.InvalidMove

    def _check_capture_move_valid(self, old_row: int, old_column: int, new_row: int, new_column: int):
        if new_row not in [_ for _ in range(1, 9)] or new_column not in [_ for _ in range(1, 9)]:
            raise ch_exc.NonexistentBoardField
        move_shift = 2 if self._white_move else -2
        if new_row - old_row != move_shift or abs(new_column - old_column) != 2:
            raise ch_exc.InvalidMove
        if self._board[new_row][new_column]:
            raise ch_exc.OccupiedField
        middle_row = max(new_row, old_row) - 1
        middle_column = max(new_column, old_column) - 1
        if not self._board[middle_row][middle_column]:
            raise ch_exc.NoPawnToCapture
        elif self._white_move and self._board[middle_row][middle_column].color == Color.WHITE:
            raise ch_exc.NoPawnToCapture
        elif not self._white_move and self._board[middle_row][middle_column].color == Color.BLACK:
            raise ch_exc.NoPawnToCapture
        else:
            return

    def _change_position_on_board(self, piece: Piece, new_row: int, new_column: int):
        self._board[piece.row][piece.column] = None
        self._board[new_row][new_column] = piece
        piece.change_position(new_row=new_row, new_column=new_column)

    def _capture_piece(self, piece: Piece, new_row: int, new_column: int):
        captured_row = new_row - 1 if new_row > piece.row else new_row + 1
        captured_column = new_column - 1 if new_column > piece.column else new_column + 1
        captured = self._board[captured_row][captured_column]
        self._board[captured_row][captured_column] = None
        if self._white_move:
            self._black_player.remove_piece(captured)
        else:
            self._white_player.remove_piece(captured)

    def _check_piece_able_to_capture(self, piece: Piece):
        shifts = [(2, 2), (2, -2)] if self._white_move else [(-2, -2), (-2, 2)]
        for shift_row, shift_column in shifts:
            try:
                self._check_capture_move_valid(piece.row, piece.column, piece.row + shift_row,
                                               piece.column + shift_column)
                self._possible_moves.append({MovePart.PIECE: piece, MovePart.ROW: piece.row + shift_row, MovePart.COLUMN: piece.column + shift_column})
            except (ch_exc.NoPawnToCapture, ch_exc.NonexistentBoardField, ch_exc.OccupiedField):
                continue

    def _check_piece_able_to_simple_move(self, piece: Piece):
        shifts = [(1, 1), (1, -1)] if self._white_move else [(-1, -1), (-1, 1)]
        for shift_row, shift_column in shifts:
            try:
                self._check_simple_move_valid(piece.row, piece.column, piece.row + shift_row,
                                              piece.column + shift_column)
                self._possible_moves.append({MovePart.PIECE: piece, MovePart.ROW: piece.row + shift_row, MovePart.COLUMN: piece.column + shift_column})
            except (ch_exc.NoPawnToCapture, ch_exc.NonexistentBoardField, ch_exc.OccupiedField):
                continue

    def _check_king_able_to_simple_move(self, piece: Piece):
        for row_up, column_up in [(True, True), (True, False), (False, True), (False, False)]:
            self._check_quarter_for_king_simple_move(piece, row_up, column_up)

    def _check_quarter_for_king_simple_move(self, piece: Piece, row_up: bool, column_up: bool):
        row_range = (piece.row + 1, 9, 1) if row_up else (piece.row - 1, 0, -1)
        column_shift = -1 if column_up == row_up else 1
        for row in range(row_range[0], row_range[1], row_range[2]):
            column = piece.column + (piece.row - row) * column_shift
            try:
                if self._board[row][column] is None:
                    self._possible_moves.append({MovePart.PIECE: piece, MovePart.ROW: row, MovePart.COLUMN: column})
                else:
                    return
            except KeyError:
                return

    def _check_king_able_to_capture(self, piece: Piece):
        for row_up, column_up in [(True, True), (True, False), (False, True), (False, False)]:
            self._check_quarter_for_king_capture(piece, row_up, column_up)

    def _check_quarter_for_king_capture(self, piece: Piece, row_up: bool, column_up: bool):
        row_range = (piece.row + 1, 9, 1) if row_up else (piece.row - 1, 0, -1)
        column_shift = 1 if column_up else -1
        column_factor = -1 if column_up == row_up else 1
        for row in range(row_range[0], row_range[1], row_range[2]):
            column = piece.column + (piece.row - row) * column_factor
            try:
                if self._board[row][column] is not None:
                    if self._board[row + row_range[2]][column + column_shift] is None:
                        self._possible_moves.append({MovePart.PIECE: piece, MovePart.ROW: row + row_range[2], MovePart.COLUMN: column + column_shift})
                    return
            except KeyError:
                return

    def _get_possible_capture_moves(self):
        player = self._white_player if self._white_move else self._black_player
        self._possible_moves = []
        self._must_capture = False
        for piece in player.pieces:
            if piece.is_King:
                self._check_king_able_to_capture(piece)
            else:
                self._check_piece_able_to_capture(piece)
        if len(self._possible_moves) != 0:
            self._must_capture = True

    def _get_possible_simple_moves(self):
        player = self._white_player if self._white_move else self._black_player
        for piece in player.pieces:
            if piece.is_King:
                self._check_king_able_to_simple_move(piece)
            else:
                self._check_piece_able_to_simple_move(piece)

    def _check_if_king(self, piece: Piece):
        if self._white_move and piece.row == 8:
            piece.make_King()
        elif not self._white_move and piece.row == 0:
            piece.make_King()

