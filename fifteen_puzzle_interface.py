import pygame
import sys
import time
import random
#
pygame.init()
size = width, height = 600, 400
#
#  Colors
BG_COLOR = (11, 29, 70)
TYTLE_COLOR = ('cyan')
TABLE_COLOR = (255, 255, 255)
FONT_COLOR = ('cyan')

screen = pygame.display.set_mode(size)
largeFont = pygame.font.Font("MarkerFelt.ttc", 50)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
smallFont = pygame.font.Font("MarkerFelt.ttc", 20)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 50)


board_finish = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

# start the game with the finish board    
board = board_finish
focus_tile = (3, 3)


# the random board generation function
def randomize_board():
    global focus_tile
    sequence =  [i for i in range(16)]
    random.shuffle(sequence)
    
    for i in range(4):
        for j in range(4):
            board[i][j] = sequence[i * 4 + j]
            if board[i][j] == 0:
                focus_tile = (i, j)
    return board

# tile move function
def move_tile(board, tile):
    global focus_tile
    i, j = tile
    if i > 0 and board[i - 1][j] == 0:
        board[i][j], board[i - 1][j] = board[i - 1][j], board[i][j]
        return (i - 1, j)
    if i < 3 and board[i + 1][j] == 0:
        board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
        return (i + 1, j)
    if j > 0 and board[i][j - 1] == 0:
        board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
        return (i, j - 1)
    if j < 3 and board[i][j + 1] == 0:
        board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
        return (i, j + 1)
    #print(tile)
    #focus_tile = tile
    return board

def shaffle_board(board):
    while True:
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    break
            if board[i][j] == 0:
                break
        moves = []
        if i > 0:
            moves.append((i - 1, j))
        if i < 3:
            moves.append((i + 1, j))
        if j > 0:
            moves.append((i, j - 1))
        if j < 3:
            moves.append((i, j + 1))
        move = random.choice(moves)
        board[i][j], board[move[0]][move[1]] = board[move[0]][move[1]], board[i][j]
        if board == board_finish:
            break
    return board


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BG_COLOR)

    # Draw title
    title = largeFont.render("FIFTEEN PUZZLE", True, TYTLE_COLOR)
    titleRect = title.get_rect()
    titleRect.center = ((width / 2), 30)
    screen.blit(title, titleRect)

    # Draw Shaffle buttons
    shaffleButton = pygame.Rect((width - 80), (height - 60), 40 , 25)
    shaffle = smallFont.render("Shaffle", True, FONT_COLOR, BG_COLOR)
    shaffleRect = shaffle.get_rect()
    shaffleRect.center = shaffleButton.center
    pygame.draw.rect(screen, TABLE_COLOR, shaffleButton)
    screen.blit(shaffle, shaffleRect)
    

    # Draw game board
    tile_size = 80
    tile_origin = (width / 2 - (2 * tile_size),
                    height / 2 - (2 * tile_size) + 30)
    tiles = []
    for i in range(4):
        row = []
        for j in range(4):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            if focus_tile[0] == i and focus_tile[1] == j:
                text_color = BG_COLOR
                '''
                print(f"focus {focus_tile}")
                print(f"i {i} j {j}")
                print(f"board {board[i][j]}")
                '''
                pygame.draw.rect(screen, TYTLE_COLOR, rect)
                pygame.draw.rect(screen, BG_COLOR, rect, 4)
            else:
                text_color = FONT_COLOR

            pygame.draw.rect(screen, TABLE_COLOR, rect, 3)
            
            # Don't draw the 0 tile
            if board[i][j] != 0:
                move = moveFont.render(str(board[i][j]), True, text_color)
                moveRect = move.get_rect()
                moveRect.center = rect.center
                screen.blit(move, moveRect)
            row.append(rect)
        tiles.append(row)

    # Check if button is clicked
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if shaffleButton.collidepoint(mouse):
            print("shaffle")
            board = randomize_board()
        else:
            for i in range(4):
                for j in range(4):
                    if tiles[i][j].collidepoint(mouse):
                        focus_tile = move_tile(board, (i, j))
                        #focus_tile = (i, j)
                        #print(board[i][j])
                        #pygame.display.flip()
                        screen.blit(title, titleRect)
                        break
                #break
    time.sleep(0.1)
    pygame.display.flip()