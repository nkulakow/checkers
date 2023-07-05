class NonexistentBoardField(BaseException):
    def __init__(self):
        super().__init__("That's not existing position on board")


class OccupiedField(BaseException):
    def __init__(self):
        super().__init__("Occupied field chosen")


class NoPawnToCapture(BaseException):
    def __init__(self):
        super().__init__("No pawn to capture in this move")


class InvalidMove(BaseException):
    def __init__(self):
        super().__init__("This is invalid move")


class NoPieceChosen(BaseException):
    def __init__(self):
        super().__init__("No piece was chosen")


class InvalidPieceChosen(BaseException):
    def __init__(self):
        super().__init__("Chosen piece that does not belong to the player")
