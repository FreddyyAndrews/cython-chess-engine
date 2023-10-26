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
        ("8/8/8/8/4p3/8/8/4K3 w - - 0 1", 8),  # King surrounded by empty squares
    ],
)
def test_generate_pseudo_legal_moves(fen_string, expected_move_count):
    board = GameState(fen_string)
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_pseudolegal_moves_from_position()
    assert len(moves) == expected_move_count
