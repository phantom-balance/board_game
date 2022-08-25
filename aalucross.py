import pygame as p
import aalucrossEngine

WIDTH = HEIGHT = 513
DIMENSION = 3
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ["aalu", "cross"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Image/"+piece+".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = aalucrossEngine.GameState()
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse event
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if gs.board[row][col]=="--":
                    gs.make_move(row, col)
                    gs.aaluturn = not gs.aaluturn
                # print(gs.board)
            # keyboard event
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    gs.aaluturn = not gs.aaluturn

        if gs.check_board()=="aalu":
            print("aalu won")
            running = False
        elif gs.check_board()=="cross":
            print("cross won")
            running = False
        elif gs.check_board()=="draw":
            print("draw game")
            running = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],  p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()