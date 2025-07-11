import os
import time
from enum import Enum

import pygame
import pygame_gui
from pygame import AUDIO_ALLOW_ANY_CHANGE

# TODO add _draw_winner animation for _draw_winner (cross out winner)

class Option(Enum):
    SINGLE_PLAYER = 0
    MULTIPLE_PLAYER = 1
    SETTINGS = 2
    EXIT = 3
    MAIN_MENU = 4


def print_fields(list) -> None:
    if len(list) > 0:
        print(list)


def print_text(screen: pygame.Surface, x: int, y: int, text, font_name=None, font_color='green',
               font_background=None) -> None:
    font = pygame.font.Font(font_name, 36)
    if font_background is None:
        text_surface = font.render(text, True, pygame.Color(font_color))
    else:
        text_surface = font.render(text, True, pygame.Color(font_color), pygame.Color(font_background))
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


class UI:
    def __init__(self, board_class, ai, ai_mark, player_mark):
        # UI init and screen settings
        pygame.init()
        self.size = width, height = 800, 800
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        pygame.display.set_caption("Tic Tac Toe")

        # game fields
        self.board_class = board_class
        self.ai = ai
        self.ai_mark = ai_mark
        self.player_mark = player_mark
        self.turn = self.board_class.turn

        # turn
        self.turn_rect = None
        self.turn_position = None

        # multiplayer
        self.fist_player_mark = self.board_class.fist_player_mark
        self.second_player_mark = self.board_class.second_player_mark

        # visuals
        self.background_color = pygame.Color("black")
        self.manager = pygame_gui.UIManager(self.screen.get_size())
        # self.manager = pygame_gui.UIManager(self.screen.get_size(), 'styles/theme.json')
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen, self._clear_screen, self.background_color, self.manager, self.clock)
        self.choice = None
        self.settings = Settings(self.screen, self._clear_screen, self.background_color, self.manager, self.clock)

        # music
        pygame.mixer.init(channels=2, allowedchanges=AUDIO_ALLOW_ANY_CHANGE)
        self.music_loaded = False

        # drawing fields

        self.running = None
        self.rect_size = 100
        self.total_area = self.rect_size * self.board_class.field_number
        self.rect_list = []
        self.occupied_field = [False for _ in range(self.board_class.field_number)]



    def run(self) -> None:

        self._music_manager()
        self.running = True
        while self.running:
            self.choice = self.menu.main_menu()

            match self.choice:
                case Option.SINGLE_PLAYER:
                    self.board_class.set_board_size(3)
                    self.board_class.size = 3
                    self._single_player_game()
                case Option.MULTIPLE_PLAYER:
                    self.board_class.set_board_size(self.settings.get_board_size(), True)
                    self.board_class.size = self.settings.get_board_size()
                    self._multiple_player_game()
                case Option.SETTINGS:
                    self.choice, self.player_mark, self.ai_mark = self.settings.game_settings(self.player_mark, self.ai_mark)
                    self.fist_player_mark = self.player_mark
                    self.second_player_mark = self.ai_mark
                    self.board_class.set_marks(self.player_mark, self.ai_mark)
                    self.running = self.settings.get_running_status()
                case Option.MAIN_MENU:
                    continue
                case Option.EXIT:
                    self._clean_up()
                    pygame.quit()
                    exit(0)
                case _:
                    raise Exception("Invalid option")

        # if self.board_class.is_full() and not self.board_class.check_for_win():
        #     print('Draw')
        #     # self._display_winner("Draw")
        #     pygame.time.wait(3000)

    def reset_game(self):
        self.rect_list = []
        self.occupied_field = [False for _ in range(self.board_class.field_number)]
        self.turn = self.board_class.turn
        self.running = True
        self.board_class.reset_board()


    def _single_player_game(self) -> None:
        self.reset_game()
        self._draw_board()
        self._print_turn()
        while self.running and not self.board_class.is_full():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    break

                self._print_turn()
                self._render_player(event)

            if not self.running:
                break

            self.render_ai()


            if self.board_class.check_for_win() or self.board_class.is_tie():
                # self.board_class.__str__()
                # self._display_winner(self.board_class.winner)
                # print(self.board_class.get_winner())
                self._print_turn(True, self.board_class.get_winner())
                pygame.time.wait(3000)  # wait 3 seconds
                break

    def _multiple_player_game(self) -> None:
        self.reset_game()
        self._draw_board()
        self.turn = self.fist_player_mark
        self._print_turn()
        while self.running and not self.board_class.is_full():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    break

                self._print_turn()
                self._render_multiplayer(event)

            if not self.running:
                break


            if self.board_class.check_for_win() or self.board_class.is_tie():
                # self.board_class.__str__()
                # self._display_winner(self.board_class.winner)
                self._print_turn(True, self.board_class.get_winner())
                pygame.time.wait(3000)  # wait 3 seconds
                break

    def _print_turn(self, game_over=False, winner=None) -> None:
        font = pygame.font.SysFont(None, 48)

        x = self.screen.get_width() // 2
        y = self.turn_position - 35

        if hasattr(self, 'turn_rect') and self.turn_rect:
            self.screen.fill(self.background_color, self.turn_rect)

        text = ''
        if not game_over:
            text = f"Player {self.turn} turn"
        elif game_over and winner is not None:
            text = f"Player {winner} wins"
            self._draw_winner()
        elif game_over and winner is None:
            text = "Tie"

        text_surface = font.render(text, True, pygame.Color('white'), self.background_color)
        self.turn_rect = text_surface.get_rect(center=(x, y))

        self.screen.blit(text_surface, self.turn_rect)

        pygame.display.flip()

    def _draw_winner(self) -> None:
        path = self.board_class.get_winner_path()
        if path is None:
            return None

        winner = self.board_class.get_winner()
        # color = pygame.Color('green') if winner == 'X' else pygame.Color('red')
        color = pygame.Color('purple')
        start_rect = self.rect_list[path[0]]
        end_rect = self.rect_list[path[-1]]

        dx = end_rect.centerx - start_rect.centerx
        dy = end_rect.centery - start_rect.centery

        # row
        if dy == 0:
            start_pos = (start_rect.left, start_rect.centery)
            end_pos = (end_rect.right, end_rect.centery)
            print(start_pos, end_pos)
        # column
        elif dx == 0:
            start_pos = (start_rect.centerx, start_rect.top)
            end_pos = (end_rect.centerx, end_rect.bottom)
        # left diagonal
        elif dx > 0 and dy > 0:
            start_pos = start_rect.topleft
            end_pos = end_rect.bottomright
        # right diagonal
        else:
            start_pos = start_rect.topright
            end_pos = end_rect.bottomleft

        pygame.draw.line(self.screen, color, start_pos, end_pos, width=5)
        pygame.display.flip()
        return None

    def _render_multiplayer(self, event):
        if self.turn == self.fist_player_mark and event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            self._mark_player(position, self.fist_player_mark, self.second_player_mark)
        elif self.turn == self.second_player_mark and event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            self._mark_player(position, self.second_player_mark, self.fist_player_mark)

    def _render_player(self, event) -> None:
        """
        Renders the UI with table for Tic Tac Toe.
        Allows user to click on the specific cell to mark player move.
        :return:
        """
        if self.turn == self.player_mark and event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            self._mark_player_move(position)

    def render_ai(self) -> None:
        """
        Renders the UI with table for Tic Tac Toe.
        Allows user to click on the specific cell to mark player move.
        :return:
        """
        if self.turn == self.ai_mark:
            move = self.ai.get_best_move()
            time.sleep(0.3)
            self._mark_ai_move(move)

    def _mark_player(self, position: tuple, player, opponent) -> None:
        """
        Registers the move on the board.
        """
        x, y = position
        for field, rect in enumerate(self.rect_list):
            if rect.collidepoint(x, y) and not self.occupied_field[field]:
                self.occupied_field[field] = True
                if player == 'X':
                    x, y = rect.topleft
                    self._draw_x(x, y)
                else:
                    x, y = rect.center
                    self._draw_o(x, y)
                self.board_class.multiplayer_move(field, player)
                self.turn = opponent



    def _mark_player_move(self, position: tuple) -> None:
        """
        Registers the move on the board.
        """
        x, y = position
        for field, rect in enumerate(self.rect_list):
            if rect.collidepoint(x, y) and not self.occupied_field[field]:
                self.occupied_field[field] = True
                if self.player_mark == 'X':
                    x, y = rect.topleft
                    self._draw_x(x, y)
                else:
                    x, y = rect.center
                    self._draw_o(x, y)
                self.board_class.player_move(field)
                self.turn = self.ai_mark

    def _mark_ai_move(self, field) -> None:
        if field is not None and not self.occupied_field[field]:
            self.occupied_field[field] = True
            rect = self.rect_list[field]
            if self.ai_mark == 'X':
                x, y = rect.topleft
                self._draw_x(x, y)
            else:
                x, y = rect.center
                self._draw_o(x, y)
            self.board_class.ai_move(field)
            self.turn = self.player_mark

    def _draw_o(self, x: int, y: int) -> None:
        """
        Draws the O mark (move).
        """
        # offset so there is no holes in rects
        offset = 1
        radius = self.rect_size / 2 - offset
        pygame.draw.circle(self.screen, pygame.Color('red'), (x, y), radius, 2)
        pygame.display.flip()

    def _draw_x(self, x: int, y: int) -> None:
        """
        Draws the X mark (move).
        """
        pygame.draw.line(self.screen, pygame.Color('green'), (x, y), (x + self.rect_size, y + self.rect_size), 2)
        pygame.draw.line(self.screen, pygame.Color('green'), (x + self.rect_size, y), (x, y + self.rect_size), 2)
        pygame.display.flip()

    def _draw_board(self):
        """
        Draws the board specific size on the screen.
        """
        self._clear_screen()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.total_area = self.board_class.board_size * self.rect_size

        center_x = (screen_width - self.total_area) / 2
        center_y = (screen_height - self.total_area) / 2
        self.turn_position = center_y

        for i in range(self.board_class.board_size):
            for j in range(self.board_class.board_size):
                current_rect = pygame.Rect(center_x + self.rect_size * j, center_y + self.rect_size * i, self.rect_size,
                                           self.rect_size)
                # save rect cords for later usage
                self.rect_list.append(current_rect)
                pygame.draw.rect(self.screen, pygame.Color('blue'), current_rect, 2)
        pygame.display.flip()

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        """
        self.screen.fill(self.background_color)

    def _clean_up(self) -> None:
        """
            Cleans up the UI by quitting pygame and resetting any necessary variables.
            """
        self._music_manager()
        pygame.quit()
        self.running = False
        self.rect_list.clear()
        self.occupied_field = [False for _ in range(self.board_class.field_number)]

    def _music_manager(self) -> None:
        """
        Manages music playback.
        """
        if not self.music_loaded:
            pygame.mixer.music.load('music/0.mp3')
            self.music_loaded = True
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.unload()
            pygame.mixer.quit()


def get_center(width, height):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    return (screen_width - width) / 2, (screen_height - height) / 2


class Menu:
    def __init__(self, screen: pygame.Surface, _clear_screen, background_color, manager, clock) -> None:
        self.screen = screen
        self._clear_screen = _clear_screen
        self.background_color = background_color

        self.running = True
        self.has_chosen = False
        self.choice = None

        self.manager = manager
        self.clock = clock

        self.buttons = []


    def _create_gui_elements(self):
        self.manager.clear_and_reset()
        self._clear_screen()
        # self.buttons.clear()


        screen_width, screen_height = self.screen.get_size()
        center_x = screen_width // 2
        start_y = screen_height // 2 - 100
        button_width = 200
        button_height = 50
        spacing = 60

        # title label
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((center_x - 100, start_y - 100), (200, 50)),
            text='Tic Tac Toe',
            manager=self.manager,
            object_id="#title_label"
        )

        # buttons
        options = [
            ("SINGLE-PLAYER", Option.SINGLE_PLAYER),
            ("MULTI-PLAYER", Option.MULTIPLE_PLAYER),
            ("SETTINGS", Option.SETTINGS),
            ("EXIT", Option.EXIT)
        ]

        for i, (text, opt_enum) in enumerate(options):
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((center_x - button_width // 2,
                                           start_y + i * spacing),
                                          (button_width, button_height)),
                text=text,
                manager=self.manager,
                object_id=f"@{opt_enum.name}"
            )
            self.buttons.append((btn, opt_enum))

    def main_menu(self) -> Option:
        self._create_gui_elements()

        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    self.clean_up()
                    return Option.EXIT

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    for btn, opt_enum in self.buttons:
                        if event.ui_element == btn:
                            self.reset_attr()
                            self._clear_screen()
                            return opt_enum

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.screen.fill(self.background_color)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        return self.choice

    def reset_attr(self):
        self.has_chosen = False
        self.choice = None
        self.buttons.clear()
        self.manager.clear_and_reset()

    def clean_up(self):
        self.reset_attr()


def get_total_music():
    file_list = os.listdir('music')
    return len(file_list)


class Settings:
    def __init__(self, screen: pygame.Surface, _clear_screen, background_color, manager, clock) -> None:
        self.running = True
        self.screen = screen
        self.manager = manager
        self._clear_screen = _clear_screen
        self.background_color = background_color
        self.clock = pygame.time.Clock()
        self.rect_size = 40

        self.current_music = 1
        self.total_music = get_total_music()

        self.board_size_dropdown = None
        self.selected_board_size = '3x3'

        self.texts = [
            ('Settings', 'green'),
            ('Change Player Mark - X is default', None),
            ('Change Multiplayer board size', None),
            ('Music: Toggle ON/OFF', None),
            ('Change Music Track - Use Left/Right Arrows', None),
            ('Volume: Use Up/Down Arrows to Adjust', None),
        ]

        # elements
        self.labels = []
        self.slider = None
        self.volume_label = None
        self.volume = 50


        self.x_button = None
        self.o_button = None
        self.selected_mark = 'X'
        self.music_on = True
        self.music_toggle_button = None
        self.prev_track_button = None
        self.next_track_button = None
        self.go_back_button = None

        # load images
        self.x_image = pygame.image.load("image/X.png")
        self.o_image = pygame.image.load("image/O.png")
        self.x_image = pygame.transform.scale(self.x_image, (40, 40))
        self.o_image = pygame.transform.scale(self.o_image, (40, 40))

    def get_running_status(self):
        return self.running

    def get_board_size(self):
        return int(self.selected_board_size[0])

    def game_settings(self, player, ai):
        self._draw_settings()

        while self.running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    break

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.x_button:
                            self.selected_mark = 'X'
                            player = 'X'
                            ai = 'O'
                        elif event.ui_element == self.o_button:
                            self.selected_mark = 'O'
                            player = 'O'
                            ai = 'X'

                        elif event.ui_element == self.music_toggle_button:
                            self.music_on = not self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                                self.music_toggle_button.set_text("Music: ON")
                            else:
                                pygame.mixer.music.pause()
                                self.music_toggle_button.set_text("Music: OFF")
                        elif event.ui_element == self.prev_track_button:
                            pygame.mixer.music.unload()
                            self.current_music = (self.current_music - 1) % self.total_music
                            pygame.mixer.music.load(f'music/{self.current_music}.mp3')
                            pygame.mixer.music.play(-1)
                        elif event.ui_element == self.next_track_button:
                            pygame.mixer.music.unload()
                            self.current_music = (self.current_music + 1) % self.total_music
                            pygame.mixer.music.load(f'music/{self.current_music}.mp3')
                            pygame.mixer.music.play(-1)
                        elif event.ui_element == self.go_back_button:
                            return Option.MAIN_MENU, player, ai

                    elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self.board_size_dropdown:
                            self.selected_board_size = event.text

                    elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == self.slider:
                        self.volume = self.slider.get_current_value()
                        pygame.mixer.music.set_volume(self.volume / 100.0)
                        self.volume_label.set_text(f'{int(self.volume)}%')

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self._clear_screen()
            self.manager.draw_ui(self.screen)
            self.draw_images_on_buttons()
            self._draw_selected_border()
            pygame.display.flip()
        return Option.MAIN_MENU, player, ai


    def _draw_selected_border(self):
        if self.selected_mark == 'X' and self.x_button:
            pygame.draw.rect(self.screen, pygame.Color('red'), self.x_button.rect, 3)
        elif self.selected_mark == 'O' and self.o_button:
            pygame.draw.rect(self.screen, pygame.Color('red'), self.o_button.rect, 3)

    def _draw_settings(self):
        self.manager.clear_and_reset()
        self._clear_screen()
        center_x, start_y = get_center(0, self.screen.get_height() - 200)
        line_spacing = 100

        y = start_y
        for i, (text, color) in enumerate(self.texts):
            y =+ i * line_spacing
            label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(center_x - 200, y, 400, 30),
                text=text,
                manager=self.manager,
                object_id=f"@settings_label_{i}"
            )
            self.labels.append(label)

            if text.startswith('Change Player Mark'):
                self.x_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(center_x - 60, y + 40, 40, 40),
                    text='',
                    manager=self.manager
                )
                self.o_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(center_x + 20, y + 40, 40, 40),
                    text='',
                    manager=self.manager
                )


            elif text.startswith('Change Multiplayer board size'):

                self.board_size_dropdown = pygame_gui.elements.UIDropDownMenu(

                    options_list=['3x3', '4x4', '5x5', '6x6'],

                    starting_option=self.selected_board_size,

                    relative_rect=pygame.Rect(center_x - 60, y + 40, 120, 30),

                    manager=self.manager

                )




            elif text.startswith('Music: Toggle'):
                self.music_toggle_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(center_x - 60, y + 40, 120, 30),
                    text='Music: ON' if self.music_on else 'Music: OFF',
                    manager=self.manager
                )

            elif text.startswith('Change Music Track'):
                self.prev_track_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(center_x - 100, y + 40, 40, 30),
                    text='<',
                    manager=self.manager
                )
                self.next_track_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(center_x + 60, y + 40, 40, 30),
                    text='>',
                    manager=self.manager
                )

            elif text.startswith('Volume'):
                self.slider = pygame_gui.elements.UIHorizontalSlider(
                    relative_rect=pygame.Rect(center_x - 100, y + 40, 200, 25),
                    start_value=self.volume,
                    value_range=(0, 100),
                    manager=self.manager
                )
                self.volume_label = pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect(center_x + 110, y + 40, 80, 25),
                    text=str(self.slider.get_current_value()) + '%',
                    manager=self.manager
                )

         # draw "Go back" button below all other settings
        y += line_spacing
        self.go_back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(center_x - 60, y + 40, 120, 30),
                text='Go back',
            manager=self.manager
        )

        pygame.display.flip()

    def draw_images_on_buttons(self):
        if self.x_button:
            self.screen.blit(self.x_image, self.x_button.rect.topleft)
        if self.o_button:
            self.screen.blit(self.o_image, self.o_button.rect.topleft)
