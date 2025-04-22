"""
Contains relevant classes to be used for presenting different menus/screens to the player. Contains the start and
options menu as well as the winning and worker position selection screen

When pages are initialised they must be updated for each pygame tick for proper functionality
"""
import pygame

from ..components.button import Button
from ..utils.functions import page_template, add_god_description, add_mode_description
from ..utils.assets import SUPPORTER, MESSAGE_FONT, BUTTON_FONT, OUTLINE_FONT, BG_NOTI, BG_NOTI_2, BUTTON_ICON, \
    CLOSE_ICON, YES_ICON, \
    NO_ICON, HOME_ICON, REPLAY_ICON, DESCRIPTION_FONT
from ..utils.constants import BUTTON_SIZE_ONE, BUTTON_SIZE_TWO, WHITE, GRAY, PLAYER_ONE, PLAYER_TWO, BUTTON_SIZE_BIG


class Start:
    """
    Start screen of the game, allows the user to either start a new game, view the options menu or exit the game
    """
    def __init__(self, win):
        self.win = win
        self.start_button = Button(300, 250, BUTTON_ICON, "CHƠI NGAY", BUTTON_SIZE_ONE)  # Begin new game
        self.options_button = Button(300, 250, BUTTON_ICON, "Options", BUTTON_SIZE_ONE)  # View options menu
        self.gods_button = Button(300, 300, BUTTON_ICON, "Gods", BUTTON_SIZE_ONE)
        self.ai_button = Button(300, 330, BUTTON_ICON, "CHƠI VỚI MÁY", BUTTON_SIZE_ONE)
        self.guide_button = Button(300, 410, BUTTON_ICON, "HƯỚNG DẪN", BUTTON_SIZE_ONE)# Change god mode
        self.exit_button = Button(300, 490, BUTTON_ICON, "THOÁT", BUTTON_SIZE_ONE)  # Close application
        self.close_guide_button = Button(500, 180, CLOSE_ICON, "", (40, 40))  # Close guide
        self.exit_yes_button = Button(230, 290, YES_ICON, "", BUTTON_SIZE_BIG)
        self.exit_no_button = Button(370, 290, NO_ICON, "", BUTTON_SIZE_BIG)
        self.showing_guide = False
        self.showing_exit_popup = False

    def update(self, event):
        """
        Used to generate the initial menu and enable the buttons to be functional.
        :param event: pygame event, used to decide button action
        :return: new game state
        """
        page_template(self.win, "Santorini")  # Set background and display title

        if self.showing_guide:
            self.win.blit(BG_NOTI_2, (80, 120))
            guide_title = OUTLINE_FONT.render('HƯỚNG DẪN CHƠI', True, WHITE)
            self.win.blit(guide_title, (210, 140))
            # Thêm hướng dẫn dạng nhiều dòng
            # font = pygame.font.SysFont("arial", 18)
            guide_lines = [
                "• Mỗi người chơi có 2 công nhân.",
                "• Mỗi lượt: Di chuyển 1 công nhân + xây 1 tầng bên cạnh.",
                "• Leo lên tầng 3 để chiến thắng.",
                "• Không thể nhảy từ tầng thấp lên tầng cao hơn 1.",
                "• Nếu không còn nước đi hợp lệ thì thua.",
            ]
            for i, line in enumerate(guide_lines):
                text_surface = DESCRIPTION_FONT.render(line, True, GRAY)
                self.win.blit(text_surface, (105, 200 + i * 30))

            self.close_guide_button.draw(self.win)
            self.close_guide_button.update_colour()

            if self.close_guide_button.handle_event(event, "close"):
                self.showing_guide = False
        elif self.showing_exit_popup:
            self.win.blit(BG_NOTI, (120, 120))
            confirm_text = OUTLINE_FONT.render("Bạn chắc chắn muốn thoát?", True, GRAY)
            self.win.blit(confirm_text, (150, 210))

            self.exit_yes_button.draw(self.win)
            self.exit_no_button.draw(self.win)
            self.exit_yes_button.update_colour()
            self.exit_no_button.update_colour()

            if self.exit_yes_button.handle_event(event, "agree"):
                exit()
            elif self.exit_no_button.handle_event(event, "cancel"):
                self.showing_exit_popup = False
        else:
        # Ensure buttons are highlighted
            self.start_button.update_colour()
            # self.options_button.update_colour()
            # self.gods_button.update_colour()
            self.ai_button.update_colour()
            self.guide_button.update_colour()
            self.exit_button.update_colour()

            # Display buttons
            self.start_button.draw(self.win)
            # self.options_button.draw(self.win)
            # self.gods_button.draw(self.win)
            self.ai_button.draw(self.win)
            self.guide_button.draw(self.win)
            self.exit_button.draw(self.win)

            # Handle button clicks
            start_clicked = self.start_button.handle_event(event, "display")
            # options_clicked = self.options_button.handle_event(event, "display")
            # gods_clicked = self.gods_button.handle_event(event, "display")
            ai_clicked = self.ai_button.handle_event(event, "display")
            guide_clicked = self.guide_button.handle_event(event, "display")
            exit_clicked = self.exit_button.handle_event(event, "display")

            if start_clicked:
                return "play"
            # elif options_clicked:
            #     return "options"
            # elif gods_clicked:
            #     return "gods"
            elif ai_clicked:
                return "ai_play"
            elif guide_clicked:
                self.showing_guide = True;
            elif exit_clicked:
                self.showing_exit_popup = True;

        pygame.display.update()


class Options:
    """
    Display options menu including the main menu button, player mode button (Two Player, Minimax or Greedy) and starting
     worker positions
    """
    def __init__(self, win):
        self.win = win
        self.state = "options"
        self.game_type = "Two Player"
        self.start_select = "Default Positions"
        self.return_button = Button(300, 200, BUTTON_ICON, "back", BUTTON_SIZE_TWO)  # Return to menu
        self.option_button = Button(300, 250, BUTTON_ICON, self.game_type, BUTTON_SIZE_TWO)  # Two player, Minimax or Greedy
        self.select_button = Button(300, 300, BUTTON_ICON, self.start_select, BUTTON_SIZE_TWO)  # User decides starting positions

    def update(self, event):
        """
        Used to generate the initial menu and enable the buttons to be functional.
        :param event: pygame event, used to decide button action
        :return:
        """
        page_template(self.win, "options")

        # Show buttons
        self.return_button.draw(self.win)
        self.option_button.draw(self.win)
        self.select_button.draw(self.win)

        # Update buttons for hovering
        self.return_button.update_colour()
        self.option_button.update_colour()
        self.select_button.update_colour()

        # Update state to go back to start menu
        if self.return_button.handle_event(event, "options"):
            self.state = "start"
        # Not changing screens
        else:
            self.state = "options"

        game_type = self.option_button.handle_event(event, "options")
        selection_type = self.select_button.handle_event(event, "options")

        # If button handler returns value then it has been pressed by user
        if game_type is not None:
            self.game_type = game_type
            self.option_button.update_text(self.game_type)
        if selection_type is not None:
            self.start_select = selection_type
            self.select_button.update_text(self.start_select)

        pygame.display.update()


class Gods:
    """
    Display options menu including the main menu button, player mode button (Two Player, Minimax or Greedy) and starting
     worker positions
    """
    def __init__(self, win):
        self.win = win
        self.state = "gods"
        self.cancel_button = Button(100, 200, BUTTON_ICON, "cancel", BUTTON_SIZE_TWO)  # Cancel, do not proceed with god functions
        self.mode_button = Button(300, 200, BUTTON_ICON, "None", BUTTON_SIZE_TWO)
        self.confirm_button = Button(500, 200, BUTTON_ICON, "confirm", BUTTON_SIZE_TWO)  # Confirm god selection
        self.player_one_god_button = Button(150, 300, BUTTON_ICON, "Select God", BUTTON_SIZE_TWO)
        self.player_two_god_button = Button(450, 300, BUTTON_ICON, "Select God", BUTTON_SIZE_TWO)
        self.player_one_god = None
        self.player_two_god = None
        self.mode = "None"

    def update(self, event):
        """
        Used to generate the initial menu and enable the buttons to be functional.
        :param event: pygame event, used to decide button action
        :return:
        """
        page_template(self.win, "gods")
        # Display buttons
        self.cancel_button.draw(self.win)
        self.mode_button.draw(self.win)
        self.confirm_button.draw(self.win)
        # Check if hovering
        self.cancel_button.update_colour()
        self.mode_button.update_colour()
        self.confirm_button.update_colour()

        # Only show god options if in god mode
        if self.mode == "Simple Gods":
            # Add descriptions of currently viewed gods
            add_god_description(self.win, PLAYER_ONE, self.player_one_god)
            add_god_description(self.win, PLAYER_TWO, self.player_two_god)

            # Update buttons
            self.player_one_god_button.draw(self.win)
            self.player_two_god_button.draw(self.win)
            self.player_one_god_button.update_colour()
            self.player_two_god_button.update_colour()
            player_one_god = self.player_one_god_button.handle_event(event, "gods")
            player_two_god = self.player_two_god_button.handle_event(event, "gods")

            if player_one_god is not None:
                self.player_one_god = player_one_god
                self.player_one_god_button.update_text(player_one_god)
            if player_two_god is not None:
                self.player_two_god = player_two_god
                self.player_two_god_button.update_text(player_two_god)

        # No gods and custom mode have same template, so only need a description to be shown
        else:
            add_mode_description(self.win, self.mode)

        if self.cancel_button.handle_event(event, "cancel"):
            # Cancelling so reset god values
            self.player_one_god = None
            self.player_two_god = None
            self.state = "start"
        elif self.confirm_button.handle_event(event, "confirm"):
            self.state = "start"
        else:
            self.state = "gods"

        mode = self.mode_button.handle_event(event, "god_mode")
        if mode is not None:
            self.mode = mode
            self.mode_button.update_text(mode)

        pygame.display.update()





class Winner:
    """
    Page to show when the game.is_over is true to congratulate the relevant player
    """
    def __init__(self, win):
        self.winner = ""
        self.win = win
        self.state = "win_screen"
        self.return_button = Button(300, 250, BUTTON_ICON, "return", BUTTON_SIZE_TWO)
        self.home_button = Button(230, 270, HOME_ICON, "", BUTTON_SIZE_BIG)  # Home icon
        self.replay_button = Button(370, 270, REPLAY_ICON, "", BUTTON_SIZE_BIG)

    def win_message(self):
        """
        Inserts message on window state congratulating relevant player
        """
        winner_worker = "đỏ" if self.winner == PLAYER_ONE else "vàng"
        text = OUTLINE_FONT.render(f'Công nhân {winner_worker} thắng', True, GRAY)
        text_rect = text.get_rect()
        text_rect.center = (300, 210)
        self.win.blit(BG_NOTI, (120, 120))
        self.win.blit(text, text_rect)  # Show victory text

        # self.win.blit(SUPPORTER, (50, 300))  # Show player supporter

    def update(self, event, winner):
        """
        Used to generate the initial menu and enable the buttons to be functional.
        :param event: pygame event, used to decide button action
        :param winner: winning player
        """
        page_template(self.win, "Winner")
        self.winner = winner
        self.win_message()
        #
        # self.return_button.draw(self.win)
        # self.return_button.update_colour()
        self.home_button.draw(self.win)
        self.replay_button.draw(self.win)
        self.home_button.update_colour()
        self.replay_button.update_colour()

        name_button_1 = OUTLINE_FONT.render("Trang chủ", True, GRAY)
        name_button_2 = OUTLINE_FONT.render("Chơi lại", True, GRAY)
        self.win.blit(name_button_1, (180, 310))
        self.win.blit(name_button_2, (335, 310))

        if self.home_button.handle_event(event, "home"):
            self.state = "start"
        elif self.replay_button.handle_event(event, "replay"):
            self.state = "play"
        else:
            self.state = "win_screen"

        # if self.return_button.handle_event(event, "options"):
        #     self.state = "start"
        # else:
        #     self.state = "win_screen"

        pygame.display.update()
        return self.state