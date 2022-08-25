
class GameState():
    def __init__(self):
        self.board = [
            ["--", "--", "--"],
            ["--", "--", "--"],
            ["--", "--", "--"]]
        self.aaluturn = True
        self.list = [1,2,3]
        self.log = []

    def make_move(self, row, col):
        move = (row, col)
        self.log.append(move)
        if self.aaluturn:
            self.board[row][col] = "aalu"
            # print(self.board)
            # print("allu", row, col)
        else:
            self.board[row][col] = "cross"
            # print("cross", row, col)

    def undo_move(self):
        row, col=self.log[-1]
        self.log.pop()
        self.board[row][col] = "--"

    def check_board(self):
        winner = ""
        draw_status=0
        for row in range(3):
            for col in range(3):
                if self.board[row][col]=="--":
                    draw_status+=1
        if draw_status == 0:
            winner = "draw"
        for row in range(3):
            if (self.board[row][0]==self.board[row][1]==self.board[row][2]) and self.board[row][0] != "--":
                winner = self.board[row][0]

        for col in range(3):
            if (self.board[0][col]==self.board[1][col]==self.board[2][col]) and self.board[0][col] != "--":
                winner = self.board[0][col]

        if (self.board[0][0]==self.board[1][1]==self.board[2][2]) and self.board[0][0] != "--":
            winner = self.board[0][0]

        if (self.board[0][2]==self.board[1][1]==self.board[2][0]) and self.board[0][2] != "--":
            winner = self.board[0][2]

        return winner
