from piece import Piece
from game_state import GameState
from move import Move
from precomputed_move_data import PrecomputedMoveData


class MoveGenerator:

    game_runner: GameState = None
    precomputed: PrecomputedMoveData = None
    direction_offsets: list[int] = [8, -8, 1, -1, 7, -7, 9, -9]  # N, S, E, W, NW, SE, NE, SW

    def __init__(self, game_runner: GameState, precomputed: PrecomputedMoveData) -> None:
        self.game_runner = game_runner
        self.precomputed = precomputed

    def generate_sliding_moves(self, piece: int, start_square: int) -> list[Move]:
        # Limit directions for rook and bishop
        start_dir_index = 4 if Piece.is_type(piece, Piece.bishop) else 0
        end_dir_index = 4 if Piece.is_type(piece, Piece.rook) else 8
        moves = []
        # Iterate throug directions and moveable squares
        for direction_index in range(start_dir_index, end_dir_index):
            for j in range(self.precomputed.num_squares_to_edge[start_square][direction_index]):
                end_square = start_square + self.direction_offsets[direction_index] * (j + 1)
                end_square_piece = self.game_runner.board_representation[end_square]
                if end_square_piece == 0:
                    moves.append(Move(start_square, end_square))
                    # Handle one tile king movement
                    if Piece.is_type(piece, Piece.king):
                        break
                # Capture enemy piece
                elif Piece.get_colour(piece) != Piece.get_colour(end_square_piece):
                    moves.append(Move(start_square, end_square))
                    break
                else:
                    break

        return moves

    def generate_pawn_moves(self, piece: int, start_square: int) -> list[Move]:
        moves = []
        direction_multiplier: int = None
        # Change direction of moves for white or black
        if not Piece.is_white(piece):
            direction_multiplier = -1
        # Move forward on empty square
        if start_square + 8 * direction_multiplier == 0:
            moves.append(Move(start_square, start_square + 8 * direction_multiplier))
            # Move forward two squares on empty square if on starting rank
            if 8 <= start_square <= 15 and Piece.is_white(piece) and self.game_runner.board_representation[start_square + 16] == 0:
                moves.append(Move(start_square, start_square + 16))
            elif 48 <= start_square <= 55 and not Piece.is_white(piece) and self.game_runner.board_representation[start_square - 16] == 0:
                moves.append(Move(start_square, start_square - 16))
        # Capture enemy piece
        if not Piece.is_same_colour(self.game_runner.board_representation[start_square + 9 * direction_multiplier], piece):
            moves.append(Move(start_square, start_square + 9 * direction_multiplier))
        if not Piece.is_same_colour(self.game_runner.board_representation[start_square + 7 * direction_multiplier], piece):
            moves.append(Move(start_square, start_square + 7 * direction_multiplier))
        # En passant
        if self.game_runner.en_passant is not None:
            if start_square + 9 * direction_multiplier == self.game_runner.en_passant:
                moves.append(Move(start_square, start_square + 9 * direction_multiplier))
            if start_square + 7 * direction_multiplier == self.game_runner.en_passant:
                moves.append(Move(start_square, start_square + 7 * direction_multiplier))
        return moves

    def generate_knight_moves(self, piece: int, start_square: int) -> list[Move]:
        moves = []
        offset_list = []
        # Find place on board
        dist_west = self.precomputed.num_squares_to_edge[start_square][3]
        dist_east = self.precomputed.num_squares_to_edge[start_square][2]
        dist_north = self.precomputed.num_squares_to_edge[start_square][0]
        dist_south = self.precomputed.num_squares_to_edge[start_square][1]
        # Append viable offsets
        if dist_north > 1 and dist_west > 0:
            offset_list.append(15)
        if dist_north > 1 and dist_east > 0:
            offset_list.append(17)
        if dist_east > 1 and dist_north > 0:
            offset_list.append(10)
        if dist_east > 1 and dist_south > 0:
            offset_list.append(-6)
        if dist_south > 1 and dist_west > 0:
            offset_list.append(-17)
        if dist_south > 1 and dist_east > 0:
            offset_list.append(-15)
        if dist_west > 1 and dist_north > 0:
            offset_list.append(6)
        if dist_west > 1 and dist_south > 0:
            offset_list.append(-10)
        # Generate moves
        for offset in offset_list:
            end_square = start_square + offset
            if self.game_runner.board_representation[end_square] == 0:
                moves.append(Move(start_square, end_square))
            elif not Piece.is_same_colour(self.game_runner.board_representation[end_square], piece):
                moves.append(Move(start_square, end_square))

        return moves

    def generate_castles(self) -> list[Move]:
        pass

    def generate_moves_from_position(self) -> list[Move]:

        moves = []

        for square in range(64):
            piece = self.game_runner.board_representation[square]
            if piece == 0:
                continue
            elif (Piece.is_sliding_piece(piece) or Piece.is_type(piece, Piece.king)) and Piece.get_colour(piece) == self.game_runner.turn_to_move:
                moves += self.generate_sliding_moves(piece, square)
            elif Piece.is_type(piece, Piece.pawn) and Piece.get_colour(piece) == self.game_runner.turn_to_move:
                moves += self.generate_pawn_moves(piece, square)
            elif Piece.is_type(piece, Piece.knight) and Piece.get_colour(piece) == self.game_runner.turn_to_move:
                moves += self.generate_knight_moves(piece, square)

        return moves
