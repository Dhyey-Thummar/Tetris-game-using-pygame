# Importing the required libraries.

import pygame
import random
import sys
from pygame import mixer

# Initializing the pygame module.

pygame.init()

# Creatiing the clock object for tracking time.

clock = pygame.time.Clock()

# Creating the screen; dimensions (width, height).
window_height = 750
window_width = 560
game_screen = pygame.display.set_mode((window_width, window_height))

# Name and icon of the game.

pygame.display.set_caption("TETRIS REMASTERED")
game_icon = pygame.image.load("text-editor.png")
pygame.display.set_icon(game_icon)

# Adding background music on loop.

back_sound = mixer.Sound("_ghost_-_Ice_and_Chilli-[AudioTrimmer.com] (1).wav")
back_sound.play(-1)

# Creating a function to display score on screen.
score_font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    score = score_font.render('Score : ' + str(play.game_score), True, (76, 0, 153))
    game_screen.blit(score, (x, y))


# Creating a function to display GAME OVER screen.
game_over_font = pygame.font.SysFont('dejavuserif', 30)


def game_over(x, y):
    over = game_over_font.render('GAME OVER', True, (76, 0, 153))
    game_screen.blit(over, (x, y))


# Creating a list of various colors for differeent blocks.

color_list = [(255, 51, 51),
              (255, 153, 51),
              (0, 153, 0),
              (51, 51, 255),
              (153, 51, 255),
              (255, 51, 255), ]


# Creating a class for all the blocks and initializing it.

class Blocks:
    # Each different type of shape corresponds to a list of numbers from the grid
    # For eg. 'I' shaped block will be any of the colums from the grid i.e. 0,4,88,12 or 2,6,10,14
    # figure grid =   [00][01][02][03]
    #                 [04][05][06][07]
    #                 [08][09][10][11]
    #                 [12][13][14][15]

    # Creating a matrix/ list that stores all the possible forms and their different types of orientations
    shapes_list = [
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # Inverted L shaped block
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # I shaped block
        [[1, 2, 5, 6]],  # Square shaped block
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L shaped block
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T shaped block
        [[4, 5, 9, 10], [2, 5, 6, 9]],  # Z shaped block
        [[5, 6, 8, 9], [1, 5, 6, 10]]  # S shaped block
    ]

    # Initializing method and creating properties of class

    def __init__(object, pos_X, pos_Y):
        object.pos_X = pos_X
        object.pos_Y = pos_Y
        object.block_shape = random.randint(0, len(object.shapes_list) - 1)
        object.block_color = random.randint(1, len(color_list) - 1)
        object.orientation = 0

    # Getting the shape and orientation of the selected/current block

    def figure(object):
        return object.shapes_list[object.block_shape][object.orientation]

    # Creating a function that changes the orientation of the block by 90 degrees once
    def rotate_once(object):
        object.orientation = (object.orientation + 1) % len(object.shapes_list[object.block_shape])


# Creating a new class for the game variables and functions

class Game:
    # Initializing some required variables

    game_score = 0  # for storing score
    game_state = 'ready'  # for checking whether game is running or over

    matrix_height = 0 #
    matrix_width = 0

    w = 100
    h = 60
    z = 30

    current_block = None

    # Initialising the game class and Creating a grid in which the game is to be played ,
    # and assigning it all values 0 to denote that it is empty.
    game_matrix = []

    def __init__(self, matrix_height, matrix_width):
        self.matrix_height = matrix_height
        self.matrix_width = matrix_width
        for g in range(matrix_height):
            next_row = []
            for h in range(matrix_width):
                next_row.append(0)
            self.game_matrix.append(next_row)

    # Creating a function that returns a random block from Blocks class at a random place

    def next_block(self):
        self.current_block = Blocks(random.randint(0, 8), 0)

    # Creating a function to detect collision with existing blocks as well as boundaries

    def isCollision(self):
        collision = False
        for a in range(4):
            for b in range(4):
                if b + (a * 4) in self.current_block.figure(): # Since our shapes were a
                    if self.current_block.pos_Y + a > self.matrix_height - 1:  #
                        collision = True
                    elif self.current_block.pos_X + b > self.matrix_width - 1:  #
                        collision = True
                    elif self.game_matrix[a + self.current_block.pos_Y][b + self.current_block.pos_X] > 0:  #
                        collision = True
                    elif self.current_block.pos_X + b < 0:
                        collision = True
        return collision

    # Fixing the unmovable blocks

    def fix(self):
        for c in range(4):
            for d in range(4):
                if d + (c * 4) in self.current_block.figure():
                    self.game_matrix[self.current_block.pos_Y + c][
                        self.current_block.pos_X + d] = self.current_block.block_color

        # breaking fixed row if it is complete in above operation
        self.remove_row()
        #
        self.next_block()
        #
        if self.isCollision():
            play.game_state = 'over'
            game_over_sound = mixer.Sound('382310__myfox14__game-over-arcade.wav')
            back_sound.stop()
            game_over_sound.play()

    # creating a function to remove completed lines

    def remove_row(self):
        row = 0
        for e in range(1, self.matrix_height):
            empty_blocks = 0
            for f in range(0, self.matrix_width):
                if self.game_matrix[e][f] == 0:
                    empty_blocks += 1

            if empty_blocks == 0:
                row = row + 1
                for a in range(e, 1, -1):  #
                    for b in range(self.matrix_width):
                        self.game_matrix[a][b] = self.game_matrix[a - 1][b]  #
                # sound for clearing row
                row_clear_sound = mixer.Sound('109662__grunz__success.wav')
                row_clear_sound.play()
        # for removing each line we increase score

        self.game_score = self.game_score + (row * 10)

    def move_down(self):
        self.current_block.pos_Y = self.current_block.pos_Y + 1
        if self.isCollision():
            self.current_block.pos_Y -= 1
            self.fix()

    def move_right(self):
        self.current_block.pos_X += 1
        if self.isCollision():
            self.current_block.pos_X -= 1

    def move_left(self):
        self.current_block.pos_X -= 1
        if self.isCollision():
            self.current_block.pos_X += 1

    def rotate(self):
        previous_orientation = self.current_block.orientation
        self.current_block.rotate_once()
        if self.isCollision():
            self.current_block.orientation = previous_orientation


play = Game(20, 12)

# GAME LOOP
game_running = True
while game_running:

    if play.current_block is None:
        play.next_block()

    if play.game_state == "ready":
        play.move_down()

    for event in pygame.event.get():
        # exit condition statement
        if event.type == pygame.QUIT:
            game_running = False
            sys.exit()

        #
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                play.move_right()

            if event.key == pygame.K_LEFT:
                play.move_left()

            if event.key == pygame.K_SPACE:
                play.rotate()

    # Colorfill for background
    game_screen.fill((204, 204, 255))

    for i in range(play.matrix_height):
        for j in range(play.matrix_width):
            pygame.draw.rect(game_screen, (128, 128, 128), [play.w + play.z * j, play.h + play.z * i, play.z, play.z],
                             1)
            if play.game_matrix[i][j] > 0:
                pygame.draw.rect(game_screen, color_list[play.game_matrix[i][j]],
                                 [play.w + play.z * j + 1, play.h + play.z * i + 1, play.z - 2, play.z - 1])

    if play.current_block is not None:
        for i in range(4):
            for k in range(4):
                place = k + (i * 4)
                if place in play.current_block.figure():
                    pygame.draw.rect(game_screen, color_list[play.current_block.block_color],
                                     [play.w + play.z * (k + play.current_block.pos_X) + 1,
                                      play.h + play.z * (i + play.current_block.pos_Y) + 1, play.z - 2,
                                      play.z - 2])

    # showing score
    show_score(10, 10)

    # game over condition
    if play.game_state is 'over':
        game_over(50, window_height - 80)

    # Updating the screen
    pygame.display.update()

    # Capping the max frames per second
    clock.tick(8)

pygame.quit()
