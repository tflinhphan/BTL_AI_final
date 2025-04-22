"""
Contains the game class which is used to manage the mechanics of the game, this is the most import class and must be
updated for each pygame tick
"""
import pygame

from ..components.board import Board
from ..components.button import Button
from ..utils.functions import calc_pos, god_conditions
from ..utils.assets import MOVE_ICON, BUILD_ICON, BUTTON_ICON, EXIT_ICON, SETTING_ICON, CLOSE_ICON, MUSIC_ON_ICON, MUSIC_OFF_ICON, SOUND_OFF_ICON, SOUND_ON_ICON, BG_NOTI, DESCRIPTION_FONT, MESSAGE_FONT, OUTLINE_FONT, BUILD_SOUND, MOVE_SOUND
from ..utils.constants import BUTTON_SIZE_ONE, PLAYER_ONE, PLAYER_TWO, DEFAULT_POSITIONS, BUTTON_SIZE, \
    BUTTON_SIZE_SMALL, GRAY, BUTTON_SIZE_BIG, WHITE


class Game:
    """
    Class to manage the mechanics of the game
    """
    def __init__(self, win, starting_positions):
        if starting_positions is None:
            starting_positions = DEFAULT_POSITIONS

        self.state, self.selected, self.last_move = None, None, None
        self.using_gods, self.is_over = False, False
        self.valid_moves, self.valid_builds = [], []
        self.mode = "moving"  # Player either moving or building
        self.turn = PLAYER_ONE  # Current players move
        self.board = Board(starting_positions)
        self.gods = []
        self.win = win
        self.mode_button = Button(550, 20, BUTTON_ICON, self.mode, BUTTON_SIZE_ONE)  # Switch between moving and building
        # self.confirm_button = Button(300, 20, BUTTON_ICON, "confirm", BUTTON_SIZE_ONE)  # Confirm start positions
        self.exit_button = Button(50, 30, EXIT_ICON, "", BUTTON_SIZE)  # Return to start menu
        self.setting_button = Button(550, 30, SETTING_ICON, "", BUTTON_SIZE)
        #=======
        self.show_settings_popup = False
        self.sound_on = True
        self.music_on = True

        self.sound_button = Button(235, 230, SOUND_ON_ICON, "", BUTTON_SIZE_BIG)
        self.music_button = Button(370, 230, MUSIC_ON_ICON, "", BUTTON_SIZE_BIG)
        self.close_popup_button = Button(460, 160, CLOSE_ICON, "", BUTTON_SIZE_SMALL)

    def select(self, row, col):
        """
        Given a row and column select the relevant worker or position and check if the selection is valid
        :param row: board row
        :param col: board column
        :return: True if valid selection, otherwise False
        """
        if self.show_settings_popup:
            return False
        result = None

        if self.selected:
            if not self.board.user_select:
                old_heights = [self.board.player_one_heights + self.board.player_two_heights]
                result = self.action(row, col)
                if result:
                    if self.using_gods:
                        new_heights = [self.board.player_one_heights + self.board.player_two_heights]
                        self.update_last_move(old_heights, new_heights, row, col)
                    else:
                        if self.mode == "moving": 
                            self.change_turn()
            else:
                self.change_start_pos(row, col)

            if not result:
                self.selected = None

        worker = self.board.get_worker(row, col)
        # Ensure valid selection made
        if worker != 0 and worker.player == self.turn:
            self.selected = worker
            # If using gods the valid moves/builds are different
            # if self.using_gods:
            #     self.valid_moves, self.valid_builds = self.board.god_moves(worker, self.current_god(), self.last_move)
            # else:
            #     self.valid_moves, self.valid_builds = self.board.valid_moves(worker)
            self.valid_moves, self.valid_builds = self.board.valid_moves(worker)
            return True

        return False

    def update_last_move(self, old_heights, new_heights, row, col):
        """
        When using gods the last move needs to be recorded, this is used to track when to end turns and ensure valid
        moves are correct
        :param old_heights: heights before move
        :param new_heights: heights after move
        :param row:
        :param col:
        """
        if old_heights != new_heights:
            self.last_move = "climbing"
        elif self.last_move is not None:
            if self.last_move[0] == "building":
                self.last_move = "second_build"
            elif self.mode == "building":
                self.last_move = ["building", [row, col]]
        else:
            self.last_move = self.mode

    def draw_valid_moves(self, moves, icon):
        """
        Draw possible worker moves on the screen with the relevant icon
        :param moves: valid moves
        :param icon: move type icon (Move or Build)
        """
        for move in moves:
            row, col = move
            x, y = calc_pos(col, row, 25)
            self.win.blit(icon, (x, y))

    def action(self, row, col):
        """
        Perform action of moving a player or building on the board, changing the turn and detecting a win
        :param row: board row
        :param col: board column
        :return: True if action performed, otherwise False
        """
        if self.selected:

            if self.mode == "moving" and [row, col] in self.valid_moves:
                if self.sound_on:
                    MOVE_SOUND.play()
                self.board.move(self.selected, row, col)
                print("Moving to: ", row, col)
                self.mode = "building"  # Change mode to building
                
                # Player has reached winning height
                if self.board.get_worker(row, col).height == 3:
                    self.is_over = True
                return True

            elif self.mode == "building" and [row, col] in self.valid_builds:
                if self.sound_on:
                    BUILD_SOUND.play()
                self.board.build(row, col)
                print("Building at: ", row, col)
                self.mode = "moving"
                return True

        else:
            return False

    def change_start_pos(self, row, col):
        """
        Update the starting position of a worker
        :param row: selected row
        :param col: selected column
        :return: True if selection is valid
        """
        # Check selected position is not occupied and user is not hovering over the confirm button
        if self.selected and [row, col] not in self.board.occupied and not self.confirm_button.hovered:
            self.board.move(self.selected, row, col)

            return True

    def change_turn(self):
        """
        Switch the turn of the game
        """
        # Reset valid options
        self.valid_moves, self.valid_builds = [], []

        # Switch turn
        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        else:
            self.turn = PLAYER_ONE

    def current_god(self):
        """
        Get current player's god
        :return: god reference
        """
        if self.using_gods and self.gods != []:
            if self.turn == PLAYER_ONE:
                return self.gods[0]
            else:
                return self.gods[1]

    def update(self, event):
        """
        Update board contents, used mainly for buttons and detecting game_mode
        :param event: pygame event
        """
        self.board.draw(self.win)  # Display board
        self.mode_button.update_text(self.mode)  # Change button text so correct mode shown to user
        worker = "đỏ" if self.turn == PLAYER_ONE else "vàng"
        action = "di chuyển" if self.mode == "moving" else "xây tháp"
        status_text = f"Công nhân {worker} đang {action}"
        status_surface = DESCRIPTION_FONT.render(status_text, True, GRAY)
        pygame.draw.rect(self.win, WHITE, (170, 555, status_surface.get_width() + 20, status_surface.get_height() + 10), border_radius=10)
        # background_surface.fill((0, 0, 0, 150))
        # self.win.blit(background_surface, (170, 555))
        self.win.blit(status_surface, (180, 560))
        # Show relevant moves
        if self.mode == "moving":
            self.draw_valid_moves(self.valid_moves, MOVE_ICON)
        else:
            self.draw_valid_moves(self.valid_builds, BUILD_ICON)

        self.exit_button.update_colour()
        # self.mode_button.update_colour()
        self.setting_button.update_colour()

        self.exit_button.draw(self.win)
        # self.mode_button.draw(self.win)
        self.setting_button.draw(self.win)

        # Hiển thị popup cài đặt nếu cần
        if self.show_settings_popup:
            self.win.blit(BG_NOTI, (120, 120))
            self.sound_button.image = SOUND_ON_ICON if self.sound_on else SOUND_OFF_ICON
            self.music_button.image = MUSIC_ON_ICON if self.music_on else MUSIC_OFF_ICON

            self.sound_button.update_colour()
            self.music_button.update_colour()
            self.close_popup_button.update_colour()

            self.sound_button.draw(self.win)
            self.music_button.draw(self.win)
            self.close_popup_button.draw(self.win)
            name_button_1 = OUTLINE_FONT.render("Hiệu ứng", True, GRAY)
            name_button_2 = OUTLINE_FONT.render("Âm nhạc", True, GRAY)
            self.win.blit(name_button_1, (190, 280))
            self.win.blit(name_button_2, (325, 280))

            # Xử lý sự kiện khi nhấn các nút trong popup
            if self.sound_button.handle_event(event, "sound", self.sound_on):
                self.sound_on = not self.sound_on  # Đảo trạng thái âm thanh
                print("Tắt/bật âm thanh:", self.sound_on)

            if self.music_button.handle_event(event, "music", self.sound_on):
                self.music_on = not self.music_on
                print("Tắt/bật nhạc:", self.music_on)
                if self.music_on:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

            if self.close_popup_button.handle_event(event, "close", self.sound_on):
                self.show_settings_popup = False

        else:
            mode = self.mode_button.handle_event(event, None)
            state = self.exit_button.handle_event(event, "mode")
            setting = self.setting_button.handle_event(event, "setting", self.sound_on)

            if setting == "setting":  # ========
                self.show_settings_popup = True

            if mode:  # Update mode
                self.mode = mode
            elif state == "start":  # Return to start screen
                self.state = "start"
            else:  # No change required
                self.state = None

            # Only shows if user changing starting positions or gods are active
            if self.board.user_select or self.using_gods:
                self.confirm_button.update_colour()
                self.confirm_button.draw(self.win)
                change_turn = self.confirm_button.handle_event(event, "confirm", self.sound_on)

                if self.using_gods and self.gods != []:
                    god = self.current_god()

                    condition = god_conditions(self.last_move, god)

                    if condition == "move":
                        self.mode = "moving"
                    elif condition in ["upto l2", "new", "build"]:
                        self.mode = "building"

                    # Can only continue turn if they do not climb
                    if god == "Prometheus" and self.last_move == "climbing":
                        self.change_turn()
                    # Only able to build again if built first
                    elif god in ["Hephaestus", "Demeter"] and self.last_move in ["moving", "second_build"]:
                        self.change_turn()
                    # Unlimited moves until they climb or build
                    elif god == "Hermes" and self.last_move in ["climbing", "building"]:
                        self.change_turn()

                if change_turn:
                    if self.turn == PLAYER_TWO:
                        self.board.user_select = False
                        self.mode = "moving"

                    self.last_move = None
                    self.change_turn()

        pygame.display.update()
