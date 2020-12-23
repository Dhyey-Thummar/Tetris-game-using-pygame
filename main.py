# Hello and welcome to my code.

# Importing the required libraries.
import pygame
import random
from pygame import mixer


# Creating a main function to start, restart the game whenever 'main()' is called.

def main():
    # Initializing the pygame module.
    pygame.init()

    # Creating the clock object for controlling the speed of the game or fps.
    clock = pygame.time.Clock()

    # Creating the screen; dimensions (width, height).
    window_height = 750  # These variables can be changed if want a bigger or a smaller window
    window_width = 560
    game_screen = pygame.display.set_mode((window_width, window_height))  # set_mode defines the size of the game window

    # Name and icon of the game; will be displayed on the game window.
    pygame.display.set_caption(
        "TETRIS REMASTERED")  # set_caption will decide the name of the game that will be displlayed on window
    game_icon = pygame.image.load("text-editor.png")  # image.load assigns the image to the given variable
    pygame.display.set_icon(game_icon)  # similarly set_icon will display the image in variable to the game window title

    # Adding background music on loop to the game using mixer library.
    back_sound = mixer.Sound(
        "_ghost_-_Ice_and_Chilli-[AudioTrimmer.com] (1).wav")  # Sound loads the music to the given variable.
    back_sound.set_volume(
        0.3)  # set_volume is to control the volume of the music played. It can take values from (0.0) to (1.0).
    back_sound.play(
        -1)  # play function will play the music and the (-1) paramter while play it in loop till the game is running.

    # Adding background image to the game.
    back_image = pygame.image.load('20287026(e).jpg')

    # Creating a function to display score on the game screen
    score_font = pygame.font.Font('freesansbold.ttf', 32)  # font method defines the font as well as the text size.

    def show_score(x, y):  # (x, y) parameters contain the info as to where to display.
        score = score_font.render('Score : ' + str(play.game_score), True,
                                  (255, 255, 255))  # render will creates a surface object
        game_screen.blit(score, (x, y))  # blit will display the object on the game screen at some position

    # Creating a function to display GAME OVER screen.
    game_over_font = pygame.font.SysFont('dejavuserif', 30)

    def game_over(x, y):
        over = game_over_font.render('GAME OVER. Press R to restart.', True,
                                     (255, 255, 255))  # Showing message when the game ends.
        game_screen.blit(over, (x, y))

    # Creating a list of various colors in RGB format for different blocks.
    color_list = [(3, 65, 174),
                  (114, 203, 59),
                  (255, 213, 0),
                  (255, 151, 28),
                  (255, 50, 19), ]

    # Creating a class for all the blocks and initializing it.
    class Blocks:
        # Each different type of shape corresponds to a list of numbers from the grid
        # For eg. 'I' shaped block will be any of the colums from the grid i.e. 0,4,88,12 or 2,6,10,14
        # figure grid =   [00][01][02][03]
        #                 [04][05][06][07]
        #                 [08][09][10][11]
        #                 [12][13][14][15]

        # Creating a matrix/list that stores all the possible forms and their different types of orientations
        shapes_list = [
            [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L shaped block
            [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # Inverted L shaped block
            [[1, 5, 9, 13], [4, 5, 6, 7]],  # I shaped block
            [[1, 5, 9, 13], [4, 5, 6, 7]],  # Adding an extra I shaped block to maintain the frequency of all shapes
            [[1, 2, 5, 6]],  # Square shaped block
            [[1, 2, 5, 6]],  # Adding an extra square shaped block to maintain the frequency of all shapes
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T shaped block
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
            # Adding an extra T shaped block to maintain the frequency of all shapes
            [[4, 5, 9, 10], [2, 5, 6, 9]],  # Z shaped block
            [[5, 6, 8, 9], [1, 5, 6, 10]]  # S shaped block
        ]

        # Initializing method and creating properties of class
        def __init__(object, pos_X, pos_Y):
            object.pos_X = pos_X  # declaring a property to denote its Y coordinate
            object.pos_Y = pos_Y  # declaring a property to denote its X coordinate
            object.block_shape = random.randint(0, len(
                object.shapes_list) - 1)  # for choosing a random shape from the shape list
            object.block_color = random.randint(1,
                                                len(color_list) - 1)  # for choosing a random color from the color list
            object.orientation = 0  # declaring a property to control the orientation of the shape

        # Getting the shape and orientation of the selected/current block
        def figure(object):
            return object.shapes_list[object.block_shape][object.orientation]

        # Creating a function that changes the orientation of the block by 90 degrees once
        def rotate_once(object):
            # since a shape cannot have more than the orientations listed in the shpaes list we need to use modulo operator
            object.orientation = (object.orientation + 1) % len(object.shapes_list[object.block_shape])

    # Creating a new class for the game variables and functions
    class Game:
        # Initializing some required variables
        game_score = 0  # for storing score
        game_state = 'ready'  # for checking whether game is running or over
        matrix_height = 0  # these 2 variables store the size of the grid to be formed for the game
        matrix_width = 0

        current_block = None  # Creating a variable that will act as an object of the class "Blocks" on which we can,
        # apply various functions of the game

        # Initialising the game class and Creating a grid in which the game is to be played ,
        # and assigning it all values 0 to denote that it is empty.
        game_matrix = []

        def __init__(self, matrix_height, matrix_width):
            self.matrix_height = matrix_height  # Property to denote the size of the matrix/grid
            self.matrix_width = matrix_width
            for g in range(matrix_height):  # using loops to assign value 0 to every cell of the grid
                next_row = []
                for h in range(matrix_width):
                    next_row.append(0)
                self.game_matrix.append(next_row)

        # Creating a function that returns a random block from Blocks class at a random place
        def next_block(self):
            # since the spawn position of the block can be anything on the X axis, I used the random function and
            # to prevent collision with wall subtracted 4 from the width of the grid.
            # Also the spawn position for Y axis is 0, so block looks like it comes from top.
            self.current_block = Blocks(random.randint(0, self.matrix_width - 4), 0)

        # Creating a function to detect collision with existing blocks as well as boundaries.

        def isCollision(self):
            # creating a variable that stores the value TRUE if collision will occur and vice-versa.
            # the default value is false
            collision = False

            # Since our block shapes were all defined in a 4x4 grid(refer line 61-64 of code/comment above) containing numbers,
            # we would have to use nested loop to check whether any part of the piece is colliding or not.
            for a in range(4):  # here "a" denotes the rows in the 4x4 grid  (refer line 61-64 of code/comment above)
                for b in range(4):  # here "b" denotes the columns in the 4x4 grid
                    # since we used only one variable to represent the cell in 4x4 grid, we used (4a+b) to denote its no.
                    # we first need to check whether the cell of the 4x4 grid is occupied by current block or not
                    if b + (a * 4) in self.current_block.figure():
                        if self.current_block.pos_Y + a > self.matrix_height - 1:  # This is for collision with down edge of game matrix
                            collision = True
                        elif self.current_block.pos_X + b > self.matrix_width - 1:  # This is for collision with right edge of the game matrix
                            collision = True
                        elif self.current_block.pos_X + b < 0:  # This is for collision with left edge of game matrix
                            collision = True
                        # Next is for collision with existing, fixed blocks in the matrix.
                        # During fixing/locking a block in the matrix, I will change the value of cell of that postion from 0.
                        elif self.game_matrix[a + self.current_block.pos_Y][b + self.current_block.pos_X] != 0:
                            collision = True

            return collision

        # Creating a function to fix the block in its place
        def fix(self):
            for c in range(4):
                for d in range(4):
                    if d + (c * 4) in self.current_block.figure():
                        # So whenever fix function is called, it will change the value of cell from 0 to the color of the block we need to fix
                        self.game_matrix[self.current_block.pos_Y + c][
                            self.current_block.pos_X + d] = self.current_block.block_color

            # Calling the remove_row function to remove any fully completed row after a block has been fixed
            self.remove_row()
            # Calling the next_block function to spawn a new block as the previous block has been fixed
            self.next_block()
            # This is the game over condition.
            # So after fixing the block and spawining a new one leads to collision immediately,
            # that means the tower/formation has reached the top edge of matrix and we need to declare game is over.
            if self.isCollision():
                play.game_state = 'over'  # Changing the game_state from 'ready' to 'over'
                back_sound.stop()  # Stopping the background music
                game_over_sound = mixer.Sound('382310__myfox14__game-over-arcade.wav')  # playing the game-over sound
                game_over_sound.play()

        # Creating a function to remove completed lines

        def remove_row(self):
            row = 0
            for e in range(1, self.matrix_height):  # Going through each and every block of the matrix,
                empty_blocks = 0  # it checks whether it is empty or not
                for f in range(0, self.matrix_width):
                    if self.game_matrix[e][f] == 0:
                        empty_blocks += 1

                if empty_blocks == 0:  # If there are no empty blocks that means the row is complete
                    row = row + 1  # and we can remove it
                    for a in range(e, 1, -1):  # Since we need to check from bottom to top, -1 is used.
                        for b in range(self.matrix_width):
                            self.game_matrix[a][b] = self.game_matrix[a - 1][
                                b]  # This line brings all the blocks down by one space

                    # sound for clearing row
                    row_clear_sound = mixer.Sound('109662__grunz__success.wav')
                    row_clear_sound.play()

            # for removing each line we increase score
            self.game_score = self.game_score + (row * 10)

        # defining a function to move current block down while checking for collision
        def move_down(self):
            self.current_block.pos_Y = self.current_block.pos_Y + 1
            if self.isCollision():
                self.current_block.pos_Y -= 1
                self.fix()

        # defining a function to move current block right while checking for collision
        def move_right(self):
            self.current_block.pos_X += 1
            if self.isCollision():
                self.current_block.pos_X -= 1

        # defining a function to move current block left while checking for collision
        def move_left(self):
            self.current_block.pos_X -= 1
            if self.isCollision():
                self.current_block.pos_X += 1

        # defining a function to rotate current block while checking for collision
        def rotate(self):
            previous_orientation = self.current_block.orientation
            self.current_block.rotate_once()
            if self.isCollision():
                self.current_block.orientation = previous_orientation

    play = Game(20, 12)  # Creating a Game object
    level = 5  # A new variable to regulate speed as and when the score increases

    # GAME LOOP
    game_running = True  # while this variable is true the below loop will continue to run
    while game_running:

        if play.game_score > 20:  # This block of code is for
            level = 7  # increasing speed of the game
            if play.game_score > 30:  # while checking the score
                level = 9
                if play.game_score > 40:
                    level = 12
                    if play.game_score > 50:
                        level = 15
                        if play.game_score > 60:
                            level = 20

        if play.current_block is None:  # for spawning the first block of game
            play.next_block()

        if play.game_state == 'ready':  # constantly moving down the curent block as long as game is running
            play.move_down()

        for event in pygame.event.get():
            # exit condition statement
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.KEYDOWN:
                # When the the game is over and 'R' key is pressed the game will start again
                if event.key == pygame.K_r and play.game_state == 'over':
                    main()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # Moving right if D or right arrow is pressed
                    play.move_right()

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # Moving left if A or left arrow is pressed
                    play.move_left()

                if event.key == pygame.K_SPACE or event.key == pygame.K_w:  # Rotating the block when Spacebar is pressed
                    play.rotate()

        # Colorfill for background if background image was not present
        game_screen.fill((204, 204, 255))
        # Adding background image to screen.
        game_screen.blit(back_image, (0, 0))
        # The next line draws the outer big rectangle by using the draw.rect function
        pygame.draw.rect(game_screen, (255, 255, 255), [100, 60, 364, 604], 2)

        for i in range(play.matrix_height):
            for j in range(play.matrix_width):
                if play.game_matrix[i][j] > 0:
                    # The next line fills all the colors of the fixed or exisiting blocks
                    pygame.draw.rect(game_screen, color_list[play.game_matrix[i][j]],
                                     [102 + 30 * j, 62 + 30 * i, 30, 30])

        if play.current_block is not None:
            for i in range(4):
                for k in range(4):
                    place = k + (i * 4)
                    if place in play.current_block.figure():
                        # The next line fills the color of the current block or the one that is moving down
                        pygame.draw.rect(game_screen,
                                         color_list[play.current_block.block_color],
                                         [102 + 30 * (k + play.current_block.pos_X),
                                          62 + 30 * (i + play.current_block.pos_Y), 30, 30])

        # showing score
        show_score(10, 10)

        # game over condition
        if play.game_state == 'over':
            game_over(50, window_height - 80)

        # Updating the screen
        pygame.display.update()

        # Capping the max frames per second and for controlling the speed of the game
        clock.tick(level)

    pygame.quit()


# Calling the main function to start the game
main()
