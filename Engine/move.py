from typing import List
from Engine.piece import Piece


class Move:

    starting_square: int = None
    end_square: int = None
    is_enpassant: bool = None

    def __init__(self, starting_square: int, end_square: int, is_enpassant: bool = False) -> None:
        self.starting_square = starting_square
        self.end_square = end_square
        self.is_enpassant = is_enpassant

    def captures_king(self, board: List[int]) -> bool:
        # Implement logic to check if this move captures the king
        if Piece.is_king(board[self.end_square]):
            return True
        else:
            return False
