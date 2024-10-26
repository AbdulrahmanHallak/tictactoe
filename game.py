import sys
import pygame as pg
import time

XO = "x"
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (10, 10, 10)

TTT = [[None] * 3, [None] * 3, [None] * 3]

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

opening = pg.image.load("opening_img.png")
o_img = pg.image.load("o.png")
x_img = pg.image.load("x.png")

o_img = pg.transform.scale(o_img, (80, 80))
x_img = pg.transform.scale(x_img, (80, 80))
opening = pg.transform.scale(opening, (width, height + 100))


def start():
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(2)
    screen.fill(white)

    # vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    # Drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)


def draws_status():
    global draw

    if winner is None:
        message = XO.upper() + "'s turn"
    else:
        message = winner.upper() + " won"

    if draw:
        message = "Draw"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, white)

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rec = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rec)
    pg.display.update()


def check_win():
    global TTT, winner, draw

    for i in range(3):
        # check for winning rows.
        if all(x == TTT[i][0] for x in TTT[i]) and TTT[i][0]:
            winner = TTT[i][0]
            pg.draw.line(
                screen,
                (250, 0, 0),
                (0, (i + 1) * height / 3 - height / 6),
                (width, (i + 1) * height / 3 - height / 6),
                4,
            )
            break

        # check for winning columns.
        if all(x == TTT[0][i] for x in TTT[i]) and TTT[0][i]:
            winner = TTT[0][i]
            pg.draw.line(
                screen,
                (250, 0, 0),
                ((i + 1) * width / 3 - width / 6, 0),
                ((i + 1) * width / 3 - width / 6, height),
                4,
            )
            break

        # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        winner = TTT[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if all([all(row) for row in TTT]) and winner is None:
        draw = True
    draws_status()


def drawXO(row, column):
    global TTT, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30

    if column == 1:
        posy = 30
    if column == 2:
        posy = height / 3 + 30
    if column == 3:
        posy = height / 3 * 2 + 30
    TTT[row - 1][column - 1] = XO  # type: ignore
    if XO == "x":
        screen.blit(x_img, (posy, posx))  # type: ignore
        XO = "o"
    else:
        screen.blit(o_img, (posy, posx))  # type: ignore
        XO = "x"
    pg.display.update()


def user_click():
    x, y = pg.mouse.get_pos()

    row, col = None, None
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and TTT[row - 1][col - 1] is None:
        global XO
        drawXO(row, col)
        check_win()


def reset_game():
    global TTT, winner, XO, draw
    time.sleep(3)
    XO = "x"
    draw = False
    start()
    winner = None
    TTT = [[None] * 3, [None] * 3, [None] * 3]


start()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            user_click()
            if winner or draw:
                reset_game()

    pg.display.update()
    CLOCK.tick(fps)
