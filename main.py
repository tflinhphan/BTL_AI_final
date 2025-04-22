"""
Main file of the graphical version of Santorini
"""
import pygame
import pygame.mixer

pygame.init()
pygame.mixer.init()

from santorini.screens.game import Game
from santorini.utils.assets import BUILD_ICON
from santorini.algorithms import greedy, minimax
from santorini.screens.menus import Start, Options, Winner, Gods
from santorini.utils.functions import get_row_col_from_mouse
from santorini.utils.constants import HEIGHT, WIDTH, FPS, PLAYER_TWO


class Santorini:
    """
    Used to start playing the game
    """
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"  # First screen to be displayed
        self.user_select = False

        # Different screens to be used
        self.game = Game(self.window, self.user_select)
        self.start = Start(self.window)
        self.options = Options(self.window)
        self.gods = Gods(self.window)
        self.winner = Winner(self.window)
        pygame.mixer.music.load("assets/background_music.mp3")
        pygame.mixer.music.set_volume(0.4)  # Âm lượng từ 0.0 -> 1.0
        pygame.mixer.music.play(-1)  # -1 để loop vô hạn

    def run(self):
        """
        Call to run game
        """
        pygame.display.set_icon(BUILD_ICON)
        pygame.display.set_caption('Santorini')

        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif self.state == "start":
                    self.game = Game(self.window, self.user_select)
                    new_state = self.start.update(event)
                    # Detect if user switching to options menu or starting game
                    if new_state:
                        self.state = new_state

                elif self.state == "options":
                    self.options.update(event)
                    self.state = self.options.state
                    self.user_select = self.options.start_select

                elif self.state == "gods":
                    self.gods.update(event)
                    self.state = self.gods.state

                elif self.state == "ai_play":
                    self.options.game_type = "Minimax"
                    self.state = "play"
                    self.game = Game(self.window, self.user_select)

                elif self.game.is_over or self.state == "win_screen":
                    self.winner.update(event, self.game.turn)
                    if self.winner.state == "play":
                        self.game = Game(self.window, self.user_select)  # reset game
                    self.state = self.winner.state

                elif self.state == "play":
                    if self.gods.mode == "Simple Gods":
                        self.game.using_gods = True
                        self.game.gods = [self.gods.player_one_god, self.gods.player_two_god]
                    elif self.gods.mode == "None":
                        self.game.using_gods = False
                        self.game.gods = []
                    else:
                        self.game.using_gods = True
                        self.game.gods = []

                    # Algorithm always uses player two
                    if self.game.turn == PLAYER_TWO and self.options.game_type != "Two Player":
                        if self.options.game_type == "Minimax":
                            
                            # OLD VERSION: COMPARE MOVE-STEP & BUILD-STEP 
                            # Evaluating both moving and building
                            # move_score, move_board = minimax.play(self.game.board, 3, float('-inf'),
                            #                                       float('inf'), True, False, self.game)
                            # build_score, build_board = minimax.play(self.game.board, 3, float('-inf'),
                            #                                         float('inf'), True, True, self.game)
                            # # Update the current board with the higher scoring minimax board
                            # if move_score > build_score:
                            #     self.game.board = move_board
                            # else:
                            #     self.game.board = build_board

                            # Step 1: Find the most valuable move
                            move_score, move_board = minimax.play(self.game.board, 2, float('-inf'),
                                                                  float('inf'), True, False, self.game)
                            self.game.board = move_board  # Make the move

                            # Check if any AI worker has reached height 3
                            for worker in self.game.board.get_player_workers(PLAYER_TWO):
                                if worker.height == 3:
                                    self.game.is_over = True
                                    print("AI has won by reaching height 3!")
                                    break
                    
                            # Step 2: Find the most valuable build after the move
                            build_score, build_board = minimax.play(self.game.board, 2, float('-inf'),
                                                                    float('inf'), True, True, self.game)
                            self.game.board = build_board  # Make the build

                        else:
                            game_over, greedy_board = greedy.play(self.game, PLAYER_TWO)
                            self.game.board = greedy_board

                        # Ensuring game has not finished
                        if not self.game.is_over:
                            self.game.change_turn()

                    # Enable user worker selection
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        self.game.select(row, col)

                    self.game.update(event)

                    if self.game.state == "start":
                        self.state = "start"  # Redirect to start menu


if __name__ == "__main__":
    game = Santorini()
    game.run()
