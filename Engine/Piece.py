class Piece:
    # Associate each piece with a number
    none = 0
    king = 1
    pawn = 2
    knight = 3

    class Piece:
        # Associate each piece with a number
        none = 0
        king = 1
        pawn = 2
        knight = 3
        bishop = 4
        rook = 5
        queen = 6
        # Associate each colour with a number
        white = 0
        black = 8

        @staticmethod
        def is_white(piece: int):
            return piece < 7

        @staticmethod
        def is_sliding_piece(piece: int):
            if not Piece.is_white(piece):
                piece -= 8

            return piece == Piece.bishop or piece == Piece.rook or piece == Piece.queen

        @staticmethod
        def get_colour(piece: int):
            return "w" if piece < 7 else "b"
