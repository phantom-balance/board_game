# represents the board as 2x2 list with 2 character for a piece with 1st character as it's color and 2nd character as its type
# if "--" no piece is present
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = () # coordinates for the square where en passant capture is possible
        self.king_side_castle = False
        self.queen_side_castle = False

    def make_move(self, move):
        if (self.white_to_move and move.piece_moved[0]=='w') or (not self.white_to_move and move.piece_moved[0]=='b'):
            self.board[move.start_row][move.start_col] = "--"
            self.board[move.end_row][move.end_col] = move.piece_moved
            self.move_log.append(move)
            self.white_to_move = not self.white_to_move
            if (move.is_queen_side_castling_move!=True) or (move.is_king_side_castling_move!=True):
                if move.piece_moved == "wK":
                    self.white_king_location = (move.end_row, move.end_col)
                elif move.piece_moved == "bK":
                    self.black_king_location = (move.end_row, move.end_col)

            # pawn promotion
            if move.pawn_promotion:
                self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'

            if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ((move.start_row + move.end_row)//2, move.start_col)
                self.board[(move.end_row+move.start_row)//2][move.end_col] = '--'

            else:
                self.enpassant_possible = ()

            if move.is_enpassant_move:
                self.board[move.start_row][move.start_col] = '--'
                self.board[move.start_row][move.end_col] = '--'

            if move.is_queen_side_castling_move:
                if move.piece_moved[0]=='w':
                    self.board[move.start_row][move.start_col] = '--'
                    self.board[move.end_row][move.end_col] = '--'
                    self.board[7][3] = "wR"
                    self.board[7][2] = "wK"
                    self.white_king_location = (7, 2)
                if move.piece_moved[0]=="b":
                    self.board[move.start_row][move.start_col] = '--'
                    self.board[move.end_row][move.end_col] = '--'
                    self.board[0][3] = "bR"
                    self.board[0][2] = "bK"
                    self.white_king_location = (0, 2)
            if move.is_king_side_castling_move:
                if move.piece_moved[0]=='w':
                    self.board[move.start_row][move.start_col] = '--'
                    self.board[move.end_row][move.end_col] = '--'
                    self.board[7][5] = "wR"
                    self.board[7][6] = "wK"
                    self.white_king_location = (7, 6)
                if move.piece_moved[0]=="b":
                    self.board[move.start_row][move.start_col] = '--'
                    self.board[move.end_row][move.end_col] = '--'
                    self.board[0][5] = "bR"
                    self.board[0][6] = "bK"
                    self.white_king_location = (0, 6)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            # undo en_passant
            if move.is_enpassant_move:
                self.board[move.start_row][move.end_col] = 'bp' if move.piece_moved =='wp' else 'wp'
                self.enpassant_possible = (move.end_row, move.end_col)

            # undo a 2 square pawn advance
            if move.piece_moved[1] == 'p' and abs(move.start_row-move.end_row) == 2:
                self.board[(move.end_row+move.start_row)//2][move.end_col] = '--'
                self.enpassant_possible=()

            if move.piece_moved[0] == "w" and move.is_king_side_castling_move:
                self.board[7][5] = "--"
                self.board[7][6] = "--"
                self.board[7][7] = "wR"
                self.board[7][4] = "wK"

            if move.piece_moved[0] == "w" and move.is_queen_side_castling_move:
                self.board[7][2] = "--"
                self.board[7][3] = "--"
                self.board[7][0] = "wR"
                self.board[7][4] = "wK"

            if move.piece_moved[0] == "b" and move.is_king_side_castling_move:
                self.board[0][5] = "--"
                self.board[0][6] = "--"
                self.board[0][7] = "bR"
                self.board[0][4] = "bK"

            if move.piece_moved[0] == "b" and move.is_queen_side_castling_move:
                self.board[0][2] = "--"
                self.board[0][3] = "--"
                self.board[0][0] = "bR"
                self.board[0][4] = "bK"

    def get_valid_moves(self):
        # temp_enpassant_possible = self.enpassant_possible

        moves = self.get_all_possible_moves()

        for i in range(len(moves)-1, 0, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.undo_move()
            self.white_to_move = not self.white_to_move

        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False

        # self.enpassant_possible = temp_enpassant_possible
        return moves

    def in_check(self):
        # decoupling from get_valid_moves
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def get_all_possible_moves(self):
        moves = []
        self.castling_check(moves)
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.get_pawn_moves(r, c, moves)
                    elif piece == 'R':
                        self.get_rook_moves(r, c, moves)
                    elif piece == 'K':
                        self.get_king_moves(r, c, moves)
                    elif piece == "N":
                        self.get_knight_moves(r, c, moves)
                    elif piece == 'B':
                        self.get_bishop_moves(r, c, moves)
                    elif piece == 'Q':
                        self.get_queen_moves(r, c, moves)

        return moves

    def castling_check(self, moves):
        if self.white_to_move:
            if self.board[7][1]==self.board[7][2]==self.board[7][3]=="--":
                moves.append(Move((7, 4), (7, 0), self.board, is_queen_side_castling_move=True))
            if self.board[7][5]==self.board[7][6]=="--":
                moves.append(Move((7,4), (7,7), self.board, is_king_side_castling_move=True))
        else:
            if self.board[0][1]==self.board[0][2]==self.board[0][3]=="--":
                moves.append(Move((0, 4), (0, 0), self.board, is_queen_side_castling_move=True))
            if self.board[0][5]==self.board[0][6]=="--":
                moves.append(Move((0,4), (0,7), self.board, is_king_side_castling_move=True))

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if (r == 6) and (self.board[r-2][c] == "--"):
                    moves.append(Move((r, c), (r-2, c), self.board))
            # moving left
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, is_enpassant_move=True))
            # moving right
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, is_enpassant_move=True))
        else:
            if r<=6:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if (r == 1) and (self.board[r+2][c] == "--"):
                        moves.append(Move((r, c), (r+2, c), self.board))
                # moving right
                if c-1 >= 0:
                    if self.board[r+1][c-1][0] == "w":
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                    elif (r+1, c-1) == self.enpassant_possible:
                        moves.append(Move((r, c), (r+1, c-1), self.board, is_enpassant_move=True))
                # moving left
                if c+1 <= 7:
                    if self.board[r+1][c+1][0] == "w":
                        moves.append(Move((r, c), (r+1, c+1), self.board))
                    elif (r+1, c+1) == self.enpassant_possible:
                        moves.append(Move((r, c), (r+1, c+1), self.board, is_enpassant_move=True))

    def get_knight_moves(self, r, c, moves):
        plays = [(r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2), (r+1, c-2), (r+1, c+2), (r+2, c-1), (r+2, c+1)]
        self_type = self.board[r][c][0]
        for (R, C) in plays:
            if 0<=R<=7 and 0<=C<=7:
                if self_type != self.board[R][C][0]:
                    moves.append(Move((r, c), (R, C), self.board))

    def get_rook_moves(self, r, c, moves):
        if self.white_to_move:
            running_up = True
            running_down = True
            running_left = True
            running_right = True
            i = 0
            while running_up and r-i>0:
                i += 1
                if self.board[r-i][c][0] == "-":
                    moves.append(Move((r, c), (r-i, c), self.board))
                elif self.board[r-i][c][0] == "b":
                    moves.append(Move((r, c), (r-i, c), self.board))
                    running_up = False
                else:
                    running_up = False

            i = 0
            while running_down and r+i<7:
                i += 1
                if self.board[r+i][c][0] == "-":
                    moves.append(Move((r, c), (r+i, c), self.board))
                elif self.board[r+i][c][0] == "b":
                    moves.append(Move((r, c), (r+i, c), self.board))
                    running_down = False
                else:
                    running_down = False

            i = 0
            while running_left and c-i>0:
                i += 1
                if self.board[r][c-i][0] == "-":
                    moves.append(Move((r, c), (r, c-i), self.board))
                elif self.board[r][c-i][0] == "b":
                    moves.append(Move((r, c), (r, c-i), self.board))
                    running_left = False
                else:
                    running_left = False

            i = 0
            while running_right and c+i<7:
                i += 1
                if self.board[r][c+i][0] == "-":
                    moves.append(Move((r, c), (r, c+i), self.board))
                elif self.board[r][c+i][0] == "b":
                    moves.append(Move((r, c), (r, c+i), self.board))
                    running_right = False
                else:
                    running_right = False

        if not self.white_to_move:
            running_up = True
            running_down = True
            running_left = True
            running_right = True
            i = 0
            while running_down and r-i>0:
                i += 1
                if self.board[r-i][c][0] == "-":
                    moves.append(Move((r, c), (r-i, c), self.board))
                elif self.board[r-i][c][0] == "w":
                    moves.append(Move((r, c), (r-i, c), self.board))
                    running_down = False
                else:
                    running_down = False

            i = 0
            while running_up and r+i<7:
                i += 1
                if self.board[r+i][c][0] == "-":
                    moves.append(Move((r, c), (r+i, c), self.board))
                elif self.board[r+i][c][0] == "w":
                    moves.append(Move((r, c), (r+i, c), self.board))
                    running_up = False
                else:
                    running_up = False

            i = 0
            while running_right and c-i>0:
                i += 1
                if self.board[r][c-i][0] == "-":
                    moves.append(Move((r, c), (r, c-i), self.board))
                elif self.board[r][c-i][0] == "w":
                    moves.append(Move((r, c), (r, c-i), self.board))
                    running_right = False
                else:
                    running_right = False

            i = 0
            while running_left and c+i<7:
                i += 1
                if self.board[r][c+i][0] == "-":
                    moves.append(Move((r, c), (r, c+i), self.board))
                elif self.board[r][c+i][0] == "w":
                    moves.append(Move((r, c), (r, c+i), self.board))
                    running_left = False
                else:
                    running_left = False

    def get_king_moves(self, r, c, moves):
        if self.white_to_move:
            running_up = True
            running_down = True
            running_left = True
            running_right = True
            running_up_right = True
            running_up_left = True
            running_down_right = True
            running_down_left = True
            i = 0
            while running_up and r-i>0 and i==0:
                i += 1
                if self.board[r-i][c][0] == "-":
                    moves.append(Move((r, c), (r-i, c), self.board))
                elif self.board[r-i][c][0] == "b":
                    moves.append(Move((r, c), (r-i, c), self.board))
                    running_up = False
                else:
                    running_up = False

            i = 0
            while running_down and r+i<7 and i==0:
                i += 1
                if self.board[r+i][c][0] == "-":
                    moves.append(Move((r, c), (r+i, c), self.board))
                elif self.board[r+i][c][0] == "b":
                    moves.append(Move((r, c), (r+i, c), self.board))
                    running_down = False
                else:
                    running_down = False

            i = 0
            while running_left and c-i>0 and i==0:
                i += 1
                if self.board[r][c-i][0] == "-":
                    moves.append(Move((r, c), (r, c-i), self.board))
                elif self.board[r][c-i][0] == "b":
                    moves.append(Move((r, c), (r, c-i), self.board))
                    running_left = False
                else:
                    running_left = False

            i = 0
            while running_right and c+i<7 and i==0:
                i += 1
                if self.board[r][c+i][0] == "-":
                    moves.append(Move((r, c), (r, c+i), self.board))
                elif self.board[r][c+i][0] == "b":
                    moves.append(Move((r, c), (r, c+i), self.board))
                    running_right = False
                else:
                    running_right = False

            i = 0
            while running_up_right and c+i<7 and r-i>0 and i==0:
                i += 1
                if self.board[r-i][c+i][0] == "-":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                elif self.board[r-i][c+i][0] == "b":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                    running_up_right = False
                else:
                    running_up_right = False

            i = 0
            while running_up_left and c-i>0 and r-i>0 and i==0:
                i += 1
                if self.board[r-i][c-i][0] == "-":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                elif self.board[r-i][c-i][0] == "b":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                    running_up_left = False
                else:
                    running_up_left = False

            i = 0
            while running_down_right and c+i<7 and r+i<7 and i==0:
                i += 1
                if self.board[r+i][c+i][0] == "-":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                elif self.board[r+i][c+i][0] == "b":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                    running_down_right = False
                else:
                    running_down_right = False

            i = 0
            while running_down_left and c-i>0 and r+i<7 and i==0:
                i += 1
                if self.board[r+i][c-i][0] == "-":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                elif self.board[r+i][c-i][0] == "b":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                    running_down_left = False
                else:
                    running_down_left = False

        if not self.white_to_move:
            running_up = True
            running_down = True
            running_left = True
            running_right = True
            running_up_right = True
            running_up_left = True
            running_down_right = True
            running_down_left = True
            i = 0
            while running_down and r-i>0 and i==0:
                i += 1
                if self.board[r-i][c][0] == "-":
                    moves.append(Move((r, c), (r-i, c), self.board))
                elif self.board[r-i][c][0] == "w":
                    moves.append(Move((r, c), (r-i, c), self.board))
                    running_down = False
                else:
                    running_down = False

            i = 0
            while running_up and r+i<7 and i==0:
                i += 1
                if self.board[r+i][c][0] == "-":
                    moves.append(Move((r, c), (r+i, c), self.board))
                elif self.board[r+i][c][0] == "w":
                    moves.append(Move((r, c), (r+i, c), self.board))
                    running_up = False
                else:
                    running_up = False

            i = 0
            while running_right and c-i>0 and i==0:
                i += 1
                if self.board[r][c-i][0] == "-":
                    moves.append(Move((r, c), (r, c-i), self.board))
                elif self.board[r][c-i][0] == "w":
                    moves.append(Move((r, c), (r, c-i), self.board))
                    running_right = False
                else:
                    running_right = False

            i = 0
            while running_left and c+i<7 and i==0:
                i += 1
                if self.board[r][c+i][0] == "-":
                    moves.append(Move((r, c), (r, c+i), self.board))
                elif self.board[r][c+i][0] == "w":
                    moves.append(Move((r, c), (r, c+i), self.board))
                    running_left = False
                else:
                    running_left = False

            i = 0
            while running_up_right and c-i>0 and r+i<7 and i==0:
                i += 1
                if self.board[r+i][c-i][0] == "-":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                elif self.board[r+i][c-i][0] == "w":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                    running_up_right = False
                else:
                    running_up_right = False

            i = 0
            while running_up_left and c+i<7 and r+i<7 and i==0:
                i += 1
                if self.board[r+i][c+i][0] == "-":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                elif self.board[r+i][c+i][0] == "w":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                    running_up_left = False
                else:
                    running_up_left = False

            i = 0
            while running_down_right and c-i>0 and r-i>0 and i==0:
                i += 1
                if self.board[r-i][c-i][0] == "-":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                elif self.board[r-i][c-i][0] == "w":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                    running_down_right = False
                else:
                    running_down_right = False

            i = 0
            while running_down_left and c+i<7 and r-i>0 and i==0:
                i += 1
                if self.board[r-i][c+i][0] == "-":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                elif self.board[r-i][c+i][0] == "w":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                    running_down_left = False
                else:
                    running_down_left = False

    def get_bishop_moves(self, r, c, moves):
        if self.white_to_move:
            running_up_right = True
            running_up_left = True
            running_down_right = True
            running_down_left = True

            i = 0
            while running_up_right and c+i<7 and r-i>0:
                i += 1
                if self.board[r-i][c+i][0] == "-":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                elif self.board[r-i][c+i][0] == "b":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                    running_up_right = False
                else:
                    running_up_right = False

            i = 0
            while running_up_left and c-i>0 and r-i>0:
                i += 1
                if self.board[r-i][c-i][0] == "-":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                elif self.board[r-i][c-i][0] == "b":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                    running_up_left = False
                else:
                    running_up_left = False

            i = 0
            while running_down_right and c+i<7 and r+i<7:
                i += 1
                if self.board[r+i][c+i][0] == "-":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                elif self.board[r+i][c+i][0] == "b":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                    running_down_right = False
                else:
                    running_down_right = False

            i = 0
            while running_down_left and c-i>0 and r+i<7:
                i += 1
                if self.board[r+i][c-i][0] == "-":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                elif self.board[r+i][c-i][0] == "b":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                    running_down_left = False
                else:
                    running_down_left = False

        if not self.white_to_move:
            running_up_right = True
            running_up_left = True
            running_down_right = True
            running_down_left = True

            i = 0
            while running_up_right and c-i>0 and r+i<7:
                i += 1
                if self.board[r+i][c-i][0] == "-":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                elif self.board[r+i][c-i][0] == "w":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                    running_up_right = False
                else:
                    running_up_right = False

            i = 0
            while running_up_left and c+i<7 and r+i<7:
                i += 1
                if self.board[r+i][c+i][0] == "-":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                elif self.board[r+i][c+i][0] == "w":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                    running_up_left = False
                else:
                    running_up_left = False

            i = 0
            while running_down_right and c-i>0 and r-i>0:
                i += 1
                if self.board[r-i][c-i][0] == "-":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                elif self.board[r-i][c-i][0] == "w":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                    running_down_right = False
                else:
                    running_down_right = False

            i = 0
            while running_down_left and c+i<7 and r-i>0:
                i += 1
                if self.board[r-i][c+i][0] == "-":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                elif self.board[r-i][c+i][0] == "w":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                    running_down_left = False
                else:
                    running_down_left = False

    def get_queen_moves(self, r, c, moves):
        # abstraction
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)


class Move():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v:k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_king_side_castling_move=False, is_queen_side_castling_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.pawn_promotion = False
        if self.piece_moved[1]=="p":
            self.pawn_promotion = (self.piece_moved == "wp" and self.end_row==0) or (self.piece_moved == "bp" and self.end_row==7)

        self.is_enpassant_move = is_enpassant_move
        self.is_king_side_castling_move = is_king_side_castling_move
        self.is_queen_side_castling_move = is_queen_side_castling_move

        if self.piece_moved[0]==self.piece_captured[0]:
            if self.piece_moved[1]=="K":
                if self.piece_captured[1]=="R":
                    self.is_castling = True

        self.move_id = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r] # I don't understand this
