"""
Wormy (a Nibbles clone)
By Al Sweigart al@inventwithpython.com
http://inventwithpython.com/pygame
Released under a "Simplified BSD" license
Modifications by Valdemar Svabensky valdemar@mail.muni.cz
"""

import sys, random, pygame
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, 'Window width must be a multiple of cell size.'
assert WINDOWHEIGHT % CELLSIZE == 0, 'Window height must be a multiple of cell size.'
NUM_CELLS_X = WINDOWWIDTH//CELLSIZE  # TODO done
NUM_CELLS_Y = WINDOWHEIGHT//CELLSIZE  # TODO done

BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)

# No other constants go here!


def main():
    global DISPLAYSURF, FPS_CLOCK, BASICFONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Snake')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def terminate():
    """Exit the program."""
    pygame.quit()
    sys.exit()


def was_key_pressed(event):
    """Exit game on QUIT event, or return True if key was pressed."""
    if event.type == QUIT:
        terminate()
    if event.type == KEYUP:
        return True
    else:
        return False


def wait_for_key_pressed():
    """Wait for a player to press any key."""
    msg_surface = BASICFONT.render('Press a key to play.', True, GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(msg_surface, msg_rect)
    pygame.display.update()
    
    true = True
    while true:
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

        for event in pygame.event.get():
            if was_key_pressed(event):
                print("Break")
                true = False


def show_start_screen():
    """Show a welcome screen at the first start of the game. (Do not modify.)"""
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)
    wait_for_key_pressed()


def show_game_over_screen():
    """Show a game over screen when the player loses. (Do not modify.)"""
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    wait_for_key_pressed()


def get_new_snake():
    """Set a random start point for a new snake and return its coordinates."""
    # gamep plan: 
    snake_head_cor = (random.randint(2, NUM_CELLS_X - 2), random.randint(1, NUM_CELLS_Y - 2))
    second_snake_part = (snake_head_cor[0]-1, snake_head_cor[1])
    third_snake_part = (snake_head_cor[0]-2, snake_head_cor[1])
    cor = [snake_head_cor, second_snake_part, third_snake_part]
    return cor, "right"


def get_random_location():
    """Return a random cell on the game plan."""
    return random.randint(0, NUM_CELLS_X-1), random.randint(0, NUM_CELLS_Y-1)


def run_game():
    """Main game logic. Return on game over."""
    snake, direction = get_new_snake()
    apple_cor = get_random_location()

    print(snake)
    print(apple_cor)
    print(NUM_CELLS_Y)

    true = True

    while true:

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

        draw_game_state(snake, apple_cor)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_LEFT and direction != "right":
                    direction = "left"
                if event.key == K_RIGHT and direction != "left":
                    direction = "right"
                if event.key == K_UP and direction != "down":
                    direction = "up"
                if event.key == K_DOWN and direction != "up":
                    direction = "down"
                
        if direction == "left":
            new_head = (snake[0][0] - 1, snake[0][1])
            snake.insert(0, new_head)
            if snake[0] == apple_cor:
                apple_cor = get_random_location()
            else:
                snake.pop()
        if direction == "right":
            new_head = (snake[0][0] + 1, snake[0][1])
            snake.insert(0, new_head)
            if snake[0] == apple_cor:
                apple_cor = get_random_location()
            else:
                snake.pop()
        if direction == "up":
            new_head = (snake[0][0], snake[0][1] - 1)
            snake.insert(0, new_head)
            if snake[0] == apple_cor:
                apple_cor = get_random_location()
            else:
                snake.pop()
        if direction == "down":
            new_head = (snake[0][0], snake[0][1] + 1)
            snake.insert(0, new_head)
            if snake[0] == apple_cor:
                apple_cor = get_random_location()
            else:
                snake.pop()
        
        if snake[0] in snake[1:]:
            true = False
        if snake[0][0] > NUM_CELLS_X:
            true = False
        if snake[0][0] < 0:
            true = False
        if snake[0][1] > NUM_CELLS_Y:
            true = False
        if snake[0][1] < 0:
            true = False


def draw_game_state(snake, apple):
    """Draw the contents on the screen. (Do not modify.)"""

    # Draw grid
    DISPLAYSURF.fill(BGCOLOR)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

    # Draw snake
    for body_part in snake:
        x = body_part[0] * CELLSIZE
        y = body_part[1] * CELLSIZE
        outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
        pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)

    # Draw apple
    x = apple[0] * CELLSIZE
    y = apple[1] * CELLSIZE
    apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, apple_rect)

    # Draw score
    score_surface = BASICFONT.render('Score: ' + str(len(snake) - 3), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(score_surface, score_rect)


if __name__ == '__main__':
    main()