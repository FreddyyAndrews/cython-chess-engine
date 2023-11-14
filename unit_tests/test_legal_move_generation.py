import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../Engine"))
from game_state import GameState
from move_generator import MoveGenerator
from precomputed_move_data import PrecomputedMoveData
import pytest


# TODO: Add more tests
@pytest.mark.parametrize(
    "fen_string,expected_move_count",
    [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            20,
        ),  # Starting position
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1",
            20,
        ),  # Starting position (black)
        (
            "2b1kbn1/3r1r2/8/q7/4K3/8/8/8 w - - 0 1",
            1,
        ),  # One legal move (white)
        (
            "1nb1kbn1/6r1/8/8/8/8/1r6/RNB1K2R w KQ - 0 1",
            27,
        ),  # Arbitrary position (white)
        ("8/8/8/8/8/8/1k6/3K4 b - - 0 1", 6),  # Black king in open field, few moves
        ("4k3/8/8/8/8/8/8/4K3 w - - 0 1", 5),  # Endgame, only kings
        (
            "2bq1b2/8/7R/k6Q/7R/8/8/1NB1KBN1 b - - 0 1",
            4,
        ),  # Black king in check, forced moves
    ],
)
def test_generate_legal_moves(fen_string, expected_move_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    legal_moves = move_generator.generate_legal_moves_from_position()
    assert len(legal_moves) == expected_move_count
    assert board.generate_fen_from_board() == fen_string
