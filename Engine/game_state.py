from Engine.piece import Piece
from typing import List


class GameState:

    board_representation: List[int] = [0] * 64
    en_passant: int = None
    turn_to_move: str = None
    wq_castle: bool = None
    wk_Castle: bool = None
    bk_Castle: bool = None
    bq_Castle: bool = None
    half_move_clock: int = None
    full_move_clock: int = None

    def check_castling_availability(self) -> None:

        if self.board_representation[0] != Piece.white + Piece.rook:
            self.wq_castle = False
        if self.board_representation[7] != Piece.white + Piece.rook:
            self.wk_Castle = False
        if self.board_representation[4] != Piece.white + Piece.king:
            self.wq_castle = False
            self.wk_Castle = False
        if self.board_representation[56] != Piece.black + Piece.rook:
            self.bq_Castle = False
        if self.board_representation[63] != Piece.black + Piece.rook:
            self.bk_Castle = False
        if self.board_representation[60] != Piece.black + Piece.king:
            self.bq_Castle = False
            self.bk_Castle = False

    def set_board_from_fen_string(self, fen: str) -> None:
        # set char representation of numerical pieces
        piece_dict = {'k': Piece.king, 'n': Piece.knight, 'q': Piece.queen, 'p': Piece.pawn, 'b': Piece.bishop, 'r': Piece.rook}
        # Set file and rank before iteration
        file = 0
        rank = 7
        fen_split = fen.split(' ')
        # set squares
        for i in range(len(fen_split[0])):
            if fen_split[0][i] == "/":
                file = 0
                rank = rank - 1
            else:
                if fen_split[0][i].isdigit():
                    file += int(fen_split[0][i])
                else:
                    piece_colour = Piece.white if fen_split[0][i].isupper() else Piece.black
                    piece_type = piece_dict[fen_split[0][i].lower()]
                    self.board_representation[rank*8 + file] = piece_colour + piece_type
                    file = file + 1

        # Determine turn from fen
        if fen_split[1][0] == "w":
            self.turn_to_move = "w"
        else:
            self.turn_to_move = "b"

        # Default castling availability to false
        self.wq_castle = False
        self.wk_Castle = False
        self.bq_Castle = False
        self.bk_Castle = False

        # Determine if castling is set to true in fen string

        for i in range(len(fen_split[2])):

            if fen_split[2][i] == "K":
                self.wk_Castle = True

            if fen_split[2][i] == "k":
                self.bk_Castle = True

            if fen_split[2][i] == "Q":
                self.wq_Castle = True

            if fen_split[2][i] == "q":
                self.bq_Castle = True

        self.check_castling_availability()

        # En passant info

        if not fen_split[3] == "-":
            file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

            self.en_passant = file_map[fen_split[3][0]] + (int(fen_split[3][1]) - 1) * 8
     
        self.half_move_clock = int(fen_split[4])
        self.full_move_clock = int(fen_split[5])

    def switch_turn(self) -> None:

        if self.turn_to_move == "w":
            self.turn_to_move = "b"
        else:
            self.turn_to_move = "w"

    def generate_fen_from_board(self) -> str:

        piece_map = {Piece.king: "k", Piece.queen: "q", Piece.rook: "r", Piece.bishop: "b", Piece.knight: "n", Piece.pawn: "p"}
        fen = ""
        count = 0
        rank = 7
        for i in range(64):
            file = i % 8
            if self.board_representation[rank*8+file] == 0:
                count += 1
            else:
                if count != 0:
                    fen += str(count)
                    count = 0
                piece = self.board_representation[rank*8+file]
                colour = "w" if piece < 7 else "b"
                fen += piece_map[piece].upper() if colour == "w" else piece_map[piece - 8]

            if file == 7:
                rank -= 1
                if count != 0:
                    fen += str(count)
                    count = 0
                if i != 63:
                    fen += "/"

        fen += " " + self.turn_to_move + " "

        castle_dash_flag = True

        if self.wk_Castle:
            fen += "K"
            castle_dash_flag = False
        if self.wq_Castle:
            fen += "Q"
            castle_dash_flag = False
        if self.bk_Castle:
            fen += "k"
            castle_dash_flag = False
        if self.bq_Castle:
            fen += "q"
            castle_dash_flag = False
        if castle_dash_flag:
            fen += "-"

        fen += " "

        if self.en_passant is not None:
            file_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
            fen += file_map[self.en_passant % 8] + str((self.en_passant // 8) + 1)
        else:
            fen += "-"

        fen += " " + str(self.half_move_clock) + " " + str(self.full_move_clock)

        return fen

    def __init__(self, fen: str):

        if not len(fen) == 0:
            self.set_board_from_fen_string(fen)
        self.set_board_from_fen_string("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
