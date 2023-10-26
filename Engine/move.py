class Move:

    starting_square: int = None
    end_square: int = None
    is_enpassant: bool = None

    def __init__(self, starting_square: int, end_square: int, is_enpassant: bool = False) -> None:
        self.starting_square = starting_square
        self.end_square = end_square
        self.is_enpassant = is_enpassant
