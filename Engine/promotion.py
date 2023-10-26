from Engine.move import Move


class Promotion(Move):

    piece_to_promote_to: int = None

    def __init__(self, piece_to_promote_to: int, starting_square: int, end_square: int) -> None:
        super().__init__(starting_square, end_square)
        self.piece_to_promote_to = piece_to_promote_to
