import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 # square box for board to be render
DIMENSION = 8 # 8x8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 # for amination
IMAGES = {}


# to create a dictionary with keys as the piece type represented in the ChessEngine for easy access to image loading process
def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Image/"+piece+".png"), (SQ_SIZE, SQ_SIZE))
    # dictionary for image loading easily with key as piece type 'IMAGES['wN']'


# Performs the user interface side of things
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False # flag variable for when a move is made
    load_images()
    running = True
    sq_selected = () # tracks the last click of the user in tuple (row, col)
    player_clicks = [] # keeps track of players multiple clicks (list of tuples)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse event
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                # integer showing the piece selected
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = () # twice same position selection means deselect
                    player_clicks = []

                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected) # appends both 1st and second click
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            print(move.get_chess_notation())
                            gs.make_move(valid_moves[i])
                            move_made = True
                            sq_selected = ()
                            player_clicks = []
                    if not move_made:
                        player_clicks = [sq_selected]
            # keyboard event
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


# displays the game to the user
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


# helper function to draw_game_state to draw for a particular state
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# helper function to the draw_game_state to draw the total pieces postion
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()