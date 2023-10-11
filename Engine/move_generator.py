from Engine.piece import Piece
from Engine.game_state import GameState
from Engine.move import Move
from Engine.precomputed_move_data import PrecomputedMoveData


class MoveGenerator:

    game_runner: GameState = None
    precomputed: PrecomputedMoveData = None
    direction_offsets: list[int] = [8, -8, 1, -1, 7, -7, 9, -9] # N, S, E, W, NW, SE, NE, SW

    def __init__(self, game_runner: GameState, precomputed: PrecomputedMoveData) -> None:
        self.game_runner = game_runner
        self.precomputed = precomputed

    # todo: differentiate between queen, bishop, rook
    def generate_sliding_moves(self, piece: int, start_square: int) -> list[Move]:
        moves = []
        for direction_index in range(8):
            for j in range(self.precomputed.num_squares_to_edge[start_square][direction_index]):
                end_square = start_square + self.direction_offsets[direction_index] * (j + 1)
                end_square_piece = self.game_runner.board_representation[end_square]
                if end_square_piece == 0:
                    moves.append(Move(start_square, end_square))
                elif Piece.get_colour(piece) != Piece.get_colour(end_square_piece):
                    moves.append(Move(start_square, end_square))
                    break
                else:
                    break

    def generate_moves_from_position(self) -> list[Move]:

        moves = []

        for i in range(64):
            piece = self.game_runner.board_representation[i]
            if piece == 0:
                continue
            elif Piece.is_sliding_piece(piece):
                moves += self.generate_sliding_moves()
