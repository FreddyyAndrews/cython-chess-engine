from Engine.GameRunner import GameRunner
import pytest

def test_set_board_from_fen_string():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    br = GameRunner(fen)
    assert br.board_representation == [
    5, 3, 4, 6, 1, 4, 3, 5,
    2, 2, 2, 2, 2, 2, 2, 2,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    10, 10, 10, 10, 10, 10, 10, 10,
    13, 11, 12, 14, 9, 12, 11, 13]

def test_fen_string_from_board_same_as_board_from_fen():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    br = GameRunner(fen)
    assert br.board_representation == [
    5, 3, 4, 6, 1, 4, 3, 5,
    2, 2, 2, 2, 2, 2, 2, 2,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    10, 10, 10, 10, 10, 10, 10, 10,
    13, 11, 12, 14, 9, 12, 11, 13]

    assert br.generate_fen_from_board() == fen
