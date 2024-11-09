import sys
from typing import Literal
import pygame as pg
import time
from dataclasses import dataclass


WIDTH = 400
HEIGHT = 400
WHITE = (255, 255, 255)
LINE_COLOR = (10, 10, 10)

Board = list[list[str | None]]

OPENING = pg.image.load("opening_img.png")
O_IMG = pg.image.load("o.png")
X_IMG = pg.image.load("x.png")


@dataclass
class GameState:
    draw: bool
    winner: str | None
    screen: pg.Surface
    TTT: Board = None  # type: ignore
    xo: Literal["x", "o"] = "x"

    def __post_init__(self):
        if self.TTT is None:
            self.TTT = [[None] * 3, [None] * 3, [None] * 3]


def init_game() -> GameState:
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)
    pg.display.set_caption("Tic Tac Toe")

    global O_IMG, X_IMG

    O_IMG = pg.transform.scale(O_IMG, (80, 80))
    X_IMG = pg.transform.scale(X_IMG, (80, 80))
    opening = pg.transform.scale(OPENING, (WIDTH, HEIGHT + 100))

    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(2)
    screen.fill(WHITE)

    # vertical lines
    pg.draw.line(screen, LINE_COLOR, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pg.draw.line(screen, LINE_COLOR, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)
    # Drawing horizontal lines
    pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)

    game_state = GameState(False, None, screen)
    return game_state


def draw_status(game: GameState):
    if game.winner is None:
        message = game.xo.upper() + "'s turn"
    else:
        message = game.winner.upper() + " won"

    if game.draw:
        message = "Draw"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, WHITE)

    game.screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rec = text.get_rect(center=(WIDTH / 2, 500 - 50))
    game.screen.blit(text, text_rec)
    pg.display.update()


def check_win(game: GameState):
    for i in range(3):
        # Check for winning rows
        if game.TTT[i][0] and all(x == game.TTT[i][0] for x in game.TTT[i]):
            game.winner = game.TTT[i][0]
            pg.draw.line(
                game.screen,
                (250, 0, 0),
                (0, (i + 1) * HEIGHT / 3 - HEIGHT / 6),
                (WIDTH, (i + 1) * HEIGHT / 3 - HEIGHT / 6),
                4,
            )
            break

        # Check for winning columns
        if game.TTT[0][i] and all(game.TTT[j][i] == game.TTT[0][i] for j in range(3)):
            game.winner = game.TTT[0][i]
            pg.draw.line(
                game.screen,
                (250, 0, 0),
                ((i + 1) * WIDTH / 3 - WIDTH / 6, 0),
                ((i + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT),
                4,
            )
            break

    # Check for diagonal winners
    if game.TTT[0][0] and game.TTT[0][0] == game.TTT[1][1] == game.TTT[2][2]:
        game.winner = game.TTT[0][0]
        pg.draw.line(game.screen, (250, 70, 70), (50, 50), (WIDTH - 50, HEIGHT - 50), 4)

    elif game.TTT[0][2] and game.TTT[0][2] == game.TTT[1][1] == game.TTT[2][0]:
        game.winner = game.TTT[0][2]
        pg.draw.line(game.screen, (250, 70, 70), (WIDTH - 50, 50), (50, HEIGHT - 50), 4)

    # Check for a draw (board full, no winner)
    if all(all(row) for row in game.TTT) and game.winner is None:
        game.draw = True

    draw_status(game)


def drawXO(row, column, game: GameState):
    if row == 1:
        posx = 30
    if row == 2:
        posx = WIDTH / 3 + 30
    if row == 3:
        posx = WIDTH / 3 * 2 + 30

    if column == 1:
        posy = 30
    if column == 2:
        posy = HEIGHT / 3 + 30
    if column == 3:
        posy = HEIGHT / 3 * 2 + 30
    game.TTT[row - 1][column - 1] = game.xo  # type: ignore
    if game.xo == "x":
        game.screen.blit(X_IMG, (posy, posx))  # type: ignore
        game.xo = "o"

    else:
        game.screen.blit(O_IMG, (posy, posx))  # type: ignore
        game.xo = "x"
    pg.display.update()


def user_click(game: GameState):
    x, y = pg.mouse.get_pos()

    row, col = None, None
    if x < WIDTH / 3:
        col = 1
    elif x < WIDTH / 3 * 2:
        col = 2
    elif x < WIDTH:
        col = 3
    else:
        col = None

    if y < HEIGHT / 3:
        row = 1
    elif y < HEIGHT / 3 * 2:
        row = 2
    elif y < HEIGHT:
        row = 3
    else:
        row = None

    if row and col and game.TTT[row - 1][col - 1] is None:
        drawXO(row, col, game)
        check_win(game)


if __name__ == "__main__":
    game = init_game()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                # the user clicked; place an X or O
                user_click(game)
                if game.winner or game.draw:
                    time.sleep(3)
                    game = init_game()

        pg.display.update()
