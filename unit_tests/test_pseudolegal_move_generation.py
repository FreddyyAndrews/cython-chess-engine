import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../Engine'))

from game_state import GameState
from move_generator import MoveGenerator
from precomputed_move_data import PrecomputedMoveData
import pytest


@pytest.mark.parametrize(
    "fen_string,expected_move_count",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 20),  # Starting position
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1", 20),  # Starting position (black)
        ("8/8/8/8/4p3/8/8/4K3 w - - 0 1", 5),  # King surrounded by empty squares
        ("rnbqk2r/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQK2R w KQkq - 0 1", 25),  # White to castle kingside
        ("r3kbnr/pppq1ppp/2n1p3/3pP3/3P4/2N5/PPP2PPP/R1BQK1NR b KQkq - 0 1", 35),  # Black to castle queenside
        ("8/P7/8/8/8/8/8/k6K w - - 0 1", 7),  # Promotion for white
        ("k6K/8/8/8/8/8/p7/8 b - - 0 1", 7),  # Promotion for black
        ("rnbqkbnr/pppppppp/8/8/3Pp3/8/PPP2PPP/RNBQKBNR w KQkq e3 0 1", 29),  # En passant for white
    ],
)
def test_generate_pseudo_legal_moves(fen_string, expected_move_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_pseudolegal_moves_from_position()
    assert len(moves) == expected_move_count
