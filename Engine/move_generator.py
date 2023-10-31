from Engine.piece import Piece
from Engine.game_state import GameState
from Engine.move import Move
from Engine.castle import Castle
from Engine.promotion import Promotion
from Engine.precomputed_move_data import PrecomputedMoveData
import copy


class MoveGenerator:

    game_runner: GameState = None
    precomputed: PrecomputedMoveData = None
    direction_offsets: list[int] = [8, -8, 1, -1, 7, -7, 9, -9]  # N, S, E, W, NW, SE, NE, SW

    def __init__(self, game_runner: GameState, precomputed: PrecomputedMoveData) -> None:
        self.game_runner = game_runner
        self.precomputed = precomputed

    def generate_sliding_moves(self, piece: int, start_square: int) -> list[Move]:
        if not Piece.is_sliding_piece(piece):
            raise ValueError("Piece is not a sliding piece")
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
                # Capture enemy piece
                elif Piece.get_colour(piece) != Piece.get_colour(end_square_piece):
                    moves.append(Move(start_square, end_square))
                    break
                else:
                    break

        return moves

    def generate_pawn_moves(self, piece: int, start_square: int) -> list[Move]:
        if not Piece.is_type(piece, Piece.pawn):
            raise ValueError("Piece is not a pawn")
        moves = []
        direction_multiplier = -1 if not Piece.is_white(piece) else 1

        def add_promotion_or_move(end_square):
            if is_promotable(start_square, piece):
                moves.extend(Promotion(promotion_piece, start_square, end_square) for promotion_piece in Piece.get_promotion_pieces())
            else:
                moves.append(Move(start_square, end_square))

        def is_promotable(start_square, piece):
            return (Piece.is_white(piece) and 48 <= start_square <= 55) or (not Piece.is_white(piece) and 8 <= start_square <= 15)

        # Move forward on empty square
        forward_move = start_square + 8 * direction_multiplier
        if self.game_runner.board_representation[forward_move] == 0:
            add_promotion_or_move(forward_move)

            # Two-square move
            two_square_move = start_square + 16 * direction_multiplier
            if ((8 <= start_square <= 15 and Piece.is_white(piece)) or (48 <= start_square <= 55 and not Piece.is_white(piece))) and \
                    self.game_runner.board_representation[two_square_move] == 0:
                moves.append(Move(start_square, two_square_move))

        # Capture moves (both left and right)
        for capture_offset in [7, 9]:
            dist_west = self.precomputed.num_squares_to_edge[start_square][3]
            dist_east = self.precomputed.num_squares_to_edge[start_square][2]
            is_valid_move = (
                (capture_offset == 7 and dist_west > 0 and direction_multiplier == 1) or
                (capture_offset == 9 and dist_east > 0 and direction_multiplier == 1) or
                (capture_offset == 7 and dist_east > 0 and direction_multiplier == -1) or
                (capture_offset == 9 and dist_west > 0 and direction_multiplier == -1)
            )

            if is_valid_move:
                capture_move = start_square + capture_offset * direction_multiplier
                if not (Piece.are_same_colour(self.game_runner.board_representation[capture_move], piece) or
                        self.game_runner.board_representation[capture_move] == 0):
                    add_promotion_or_move(capture_move)

        # En passant
        if self.game_runner.en_passant is not None:
            for en_passant_offset in [7, 9]:
                en_passant_move = start_square + en_passant_offset * direction_multiplier
                if en_passant_move == self.game_runner.en_passant:
                    moves.append(Move(start_square, en_passant_move, is_enpassant=True))

        return moves

    def generate_knight_moves(self, piece: int, start_square: int) -> list[Move]:
        if not Piece.is_type(piece, Piece.knight):
            raise ValueError("Piece is not a knight")
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
            elif not Piece.are_same_colour(self.game_runner.board_representation[end_square], piece):
                moves.append(Move(start_square, end_square))

        return moves

    def generate_castles(self, turn: str) -> list[Move]:
        moves = []
        # White castles
        if turn == "w" and self.game_runner.wk_castle and self.game_runner.board_representation[5] == 0 \
                and self.game_runner.board_representation[6] == 0:
            moves.append(Castle(wk_castle=True))
        if turn == "w" and self.game_runner.wq_castle and self.game_runner.board_representation[1] == 0 \
                and self.game_runner.board_representation[2] == 0 and self.game_runner.board_representation[3] == 0:
            moves.append(Castle(wq_castle=True))
        # Black castles
        if turn == "b" and self.game_runner.bk_castle and self.game_runner.board_representation[61] == 0 \
                and self.game_runner.board_representation[62] == 0:
            moves.append(Castle(bk_castle=True))
        if turn == "b" and self.game_runner.bq_castle and self.game_runner.board_representation[57] == 0 \
                and self.game_runner.board_representation[58] == 0 and self.game_runner.board_representation[59] == 0:
            moves.append(Castle(bq_castle=True))

        return moves

    def generate_king_moves(self, piece: int, start_square: int) -> list[Move]:
        if not Piece.is_type(piece, Piece.king):
            raise ValueError("Piece is not a king")

        moves = []

        for direction_index in range(8):
            for j in range(min(self.precomputed.num_squares_to_edge[start_square][direction_index], 1)):
                end_square = start_square + self.direction_offsets[direction_index] * (j + 1)
                if self.game_runner.board_representation[end_square] == 0:
                    moves.append(Move(start_square, end_square))
                elif not Piece.are_same_colour(self.game_runner.board_representation[end_square], piece):
                    moves.append(Move(start_square, end_square))

        return moves

    def generate_pseudolegal_moves_from_position(self) -> list[Move]:

        moves = []

        for square in range(64):
            piece = self.game_runner.board_representation[square]
            if piece == 0:
                continue
            elif (Piece.is_sliding_piece(piece)) and Piece.get_colour(piece) == self.game_runner.turn_to_move:
                moves += self.generate_sliding_moves(piece, square)
            elif Piece.is_type(piece, Piece.pawn) and Piece.get_colour(piece) == self.game_runner.turn_to_move:
                moves += self.generate_pawn_moves(piece, square)
            elif Piece.is_type(piece, Piece.knight) and Piece.get_colour(piece) == self.game_runner.turn_to_move:
                moves += self.generate_knight_moves(piece, square)
            elif Piece.is_type(piece, Piece.king) and Piece.get_colour(piece) == self.game_runner.turn_to_move:
                moves += self.generate_king_moves(piece, square)
        if self.game_runner.turn_to_move == "w":
            moves += self.generate_castles("w")
        else:
            moves += self.generate_castles("b")

        return moves

    def generate_opponent_pseudolegal_moves_from_position(self) -> list[Move]:
        self.game_runner.switch_turn()
        moves = self.generate_pseudolegal_moves_from_position()
        self.game_runner.switch_turn()
        return moves

    def check_move_internally(self, move: Move) -> None:
        if type(move) == Castle:
            pass
        else:
            self.game_runner.board_representation[move.end_square] = self.game_runner.board_representation[move.start_square]
            self.game_runner.board_representation[move.start_square] = 0
            # Normal move
            if move.is_enpassant:
                pass
                
    # TODO: Finish implementing this      
    def generate_legal_moves_from_position(self) -> list[Move]:
        pseudo_legal_moves = self.generate_pseudolegal_moves_from_position()
        save_gamestate = copy.deepcopy(self.game_runner)
        legal_moves = []
        for move in pseudo_legal_moves:
            move_legal = True
            self.game_runner.play_move_internally(move)
            opponent_moves = self.generate_opponent_pseudolegal_moves_from_position()
            for opponent_move in opponent_moves:
                king_squares = [self.game_runner.white_king_square, self.game_runner.black_king_square]
                if opponent_move.end_square in king_squares:  # This is sufficient because the opponent cannot capture a friendly piece
                    move_legal = False
                    break
            if move_legal:
                legal_moves.append(move)
        self.game_runner = copy.deepcopy(save_gamestate)
        return legal_moves
