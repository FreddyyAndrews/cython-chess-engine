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
        ("rnbqkbnr/pppppppp/8/8/3Pp3/8/5PPP/4K3 w kq e5 0 1", 12),  # En passant for white
        ("4k3/3ppp2/8/8/3Pp3/8/5PPP/4K3 b - d3 0 1", 10),  # En passant for black
        ("rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1", 51),  # Starting white with no pawns
        ("rnbqkbnr/8/8/8/8/8/8/RNBQKBNR b KQkq - 0 1", 51)  # Starting black with no pawns
    ],
)
def test_generate_pseudo_legal_moves(fen_string, expected_move_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_pseudolegal_moves_from_position()
    assert len(moves) == expected_move_count


@pytest.mark.parametrize(
    "fen_string, starting_square, expected_move_count",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 2, 0),  # Starting position bishop
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1", 58, 0),  # Starting position (black) bishop
        ("2bqkbnr/2pppppp/8/3B4/8/8/1PPPPPPP/3QKBNR w Kk - 0 1", 35, 10),  # White Bishop in middle
        ("2bqk1nr/2pppppp/8/3Bb3/8/8/1PPPPPPP/3QKBNR w Kk - 0 1", 36, 8),  # Black Bishop in middle
        ("2bqk1nr/2pppppp/8/8/4R3/8/1PPPPPPP/3QKBN1 w k - 0 1", 28, 11),  # White Rook in middle
        ("2bqk1n1/2pppppp/8/8/4r3/8/1PPPPPPP/3QKBN1 w - - 0 1", 28, 11),  # White Rook in middle
        ("2bqk1n1/2pppppp/8/8/4r3/4Q3/1PPPPPPP/4KBN1 w - - 0 1", 20, 15),  # White Queen on Board
        ("2b1k1n1/2pppppp/8/8/4r3/4Q3/qPPPPPPP/4KBN1 w - - 0 1", 8, 13),  # White Queen on Board
    ],
)
def test_generate_sliding_moves(fen_string, starting_square, expected_move_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_sliding_moves(board.board_representation[starting_square], starting_square)
    assert len(moves) == expected_move_count


@pytest.mark.parametrize(
    "fen_string, starting_square, expected_move_count",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 8, 2),  # Starting position white pawn
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1", 48, 2),  # Starting position black pawn
        ("rnbqkbnr/ppp1p1pp/8/3p1p2/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1", 28, 3),  # White Pawn with captures
        ("rnbqkbnr/pppp1ppp/8/4p3/3P1P2/8/PPP1P1PP/RNBQKBNR w KQkq - 0 1", 36, 3),  # Black Pawn with captures
        ("7k/P7/8/8/8/8/8/7K w - - 0 1", 48, 4),  # White pawn promotion
        ("7k/P7/8/8/8/8/p7/7K w - - 0 1", 8, 4),  # Black pawn promotion
        ("rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1", 36, 2),  # Enpassant white
        ("rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR w KQkq e3 0 1", 27, 2),  # Enpassant black
    ],
)
def test_generate_pawn_moves(fen_string, starting_square, expected_move_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_pawn_moves(board.board_representation[starting_square], starting_square)
    assert len(moves) == expected_move_count


@pytest.mark.parametrize(
    "fen_string, starting_square, expected_move_count",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 4, 0),  # Starting position white king
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1", 60, 0),  # Starting position black king
        ("8/8/8/8/4K3/8/8/8 w - - 0 1", 28, 8),  # White king alone
        ("8/8/8/8/4k3/8/8/8 b - - 0 1", 28, 8),  # Black king alone
    ],
)
def test_generate_king_moves(fen_string, starting_square, expected_move_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_king_moves(board.board_representation[starting_square], starting_square)
    assert len(moves) == expected_move_count


@pytest.mark.parametrize(
    "fen_string, expected_castle_count",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0),  # Starting position white
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1", 0),  # Starting position black
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1", 2),  # White can castle both ways
        ("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b KQkq - 0 1", 2),  # Black can castle both ways
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 1", 0),  # Castling available but not allowed white
        ("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b - - 0 1", 0),  # Castling available but not allowed black
    ],
)
def test_generate_castles(fen_string, expected_castle_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_castles(board.turn_to_move)
    assert len(moves) == expected_castle_count


@pytest.mark.parametrize(
    "fen_string, starting_square, expected_move_count",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 1, 2),  # Starting position white knight
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1", 57, 2),  # Starting position black knight
        ("rnbqkbnr/pppppppp/8/8/3N4/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1", 27, 6),  # White knight in middle
        ("rnbqkbnr/pppppppp/3n4/8/3N4/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1", 43, 4),  # Black Knight in middle
        ("rnbqkbnr/pppp1ppp/3n4/8/3N4/8/PPPPpPPP/R1BQKBNR w KQkq - 0 1", 27, 7),  # White knight captures
        ("rnbqkbnr/pNpp1ppp/3n4/8/3N4/8/PPPPpPPP/R1BQKBNR w KQkq - 0 1", 43, 5),  # Black Knight captures
    ],
)
def test_generate_knight_moves(fen_string, starting_square, expected_move_count):
    board = GameState(fen_string)
    assert board.generate_fen_from_board() == fen_string
    precomputed = PrecomputedMoveData()
    move_generator = MoveGenerator(board, precomputed)
    moves = move_generator.generate_knight_moves(board.board_representation[starting_square], starting_square)
    assert len(moves) == expected_move_count


@pytest.mark.parametrize(
    "fen_string, starting_square, move_type",
    [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0, "knight"),  # Invalid knight call
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 5, "king"),  # Invalid King call
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0, "pawn"),  # Invalid Pawn Call
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 24, "sliding"),  # Invalid sliding piece call
    ],
)
def test_value_errors(fen_string, starting_square, move_type):

    with pytest.raises(ValueError):
        board = GameState(fen_string)
        assert board.generate_fen_from_board() == fen_string
        precomputed = PrecomputedMoveData()
        move_generator = MoveGenerator(board, precomputed)

        # Dynamically construct the method name
        method_name = f"generate_{move_type}_moves"

        # Use getattr to call the appropriate method
        method_to_call = getattr(move_generator, method_name)
        piece = board.board_representation[starting_square]
        method_to_call(piece, starting_square)
