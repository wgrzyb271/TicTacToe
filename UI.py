import time
from enum import Enum
from unittest import case

import pygame
from pygame import AUDIO_ALLOW_ANY_CHANGE


# TODO improve UI - add settings screen and option to play 1 vs 1 player

class Option(Enum):
    SINGLE_PLAYER = 0
    MULTIPLE_PLAYER = 1
    SETTINGS = 2


def print_fields(list) -> None:
    if len(list) > 0:
        print(list)



class UI:
    def __init__(self, board_class, ai, ai_mark, player_mark):
        # UI init and screen settings
        pygame.init()
        self.size = width, height = 800, 800
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe")

        # visuals
        self.background_color = pygame.Color("black")
        self.menu = Menu(self.screen, self._clear_screen, self.background_color)
        self.choice = None

        # music
        pygame.mixer.init(channels=2, allowedchanges=AUDIO_ALLOW_ANY_CHANGE)
        self.music_loaded = False

        # drawing fields

        self.running = None
        self.rect_size = 100
        self.board_class = board_class
        self.total_area = self.rect_size * self.board_class.field_number
        self.rect_list = []
        self.occupied_field = [False for _ in range(self.board_class.field_number)]

        # game fields

        self.ai = ai
        self.ai_mark = ai_mark
        self.player_mark = player_mark
        self.turn = self.board_class.turn

    def run(self) -> None:


        self._music_manager()
        self.running = True
        self.choice = self.menu.main_menu()

        self._draw_board()

        match Option(self.choice):
            case Option.SINGLE_PLAYER:
                self._single_player_game()
            case Option.MULTIPLE_PLAYER:
                self._multiple_player_game()
            case Option.SETTINGS:
                self._game_settings()
            case _:
                raise Exception("Invalid option")

        if self.board_class.is_full() and not self.board_class.check_for_win():
            print('Draw')
            # self._display_winner("Draw")
            pygame.time.wait(3000)
        self._clean_up()
        pygame.quit()

    def _single_player_game(self) -> None:
        while self.running and not self.board_class.is_full():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    break

                self._render_player(event)

            if not self.running:
                break

            self.render_ai()

            if self.board_class.check_for_win():
                # self._display_winner(self.board_class.winner)
                pygame.time.wait(3000)  # wait 3 seconds
                self.running = False
                break

    def _multiple_player_game(self) -> None:
        pass

    def _game_settings(self) -> None:
        pass


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
            self._mark_ai_move(move)

    def _mark_player_move(self, position: tuple) -> None:
        """
        Registers the move on the board.
        """
        x, y = position
        for field, rect in enumerate(self.rect_list):
            if rect.collidepoint(x, y) and not self.occupied_field[field]:
                self.occupied_field[field] = True
                x, y = rect.topleft
                self._draw_x(x, y)
                self.board_class.player_move(field)
                self.turn = self.ai_mark

    def _mark_ai_move(self, field) -> None:
        if field is not None and not self.occupied_field[field]:
            self.occupied_field[field] = True
            rect = self.rect_list[field]
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
        screen_width, screen_height = pygame.display.get_surface().get_size()
        for i in range(self.board_class.board_size):
            for j in range(self.board_class.board_size):
                center_x = (abs(screen_width - self.total_area / self.board_class.board_size)) / 2
                center_y = (abs(screen_height - self.total_area / self.board_class.board_size)) / 2
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
        pass
        # if not self.music_loaded:
        #     pygame.mixer.music.load('music/beatbox.mp3')
        #     self.music_loaded = True
        #     pygame.mixer.music.play(-1)
        # else:
        #     pygame.mixer.music.unload()
        #     pygame.mixer.quit()


def get_center(width, height):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    return (screen_width - width) / 2, (screen_height - height) / 2


class Menu:
    def __init__(self, screen: pygame.Surface, _clear_screen, background_color) -> None:
        self.running = True
        self.has_chosen = False
        self.choice = None


        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.background_color = background_color
        self._clear_screen = _clear_screen
        self.tile_list = list()
        self.tile_width = 10
        self.tile_height = 10
        self.tile_number = 3
        self.tile_color = pygame.Color('white')
        self.width_factor = 0.8
        self.tile_gap = 30
        self.tile_area_width = self.tile_width
        self.tile_area_height = (self.tile_height + self.tile_gap) * self.tile_number

        # fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)  # None = default font, 36 = font size
        self.font_color = pygame.Color('blue')
        self.texts = ['SINGLE-PLAYER', 'MULTI-PLAYER', 'SETTINGS']

    def main_menu(self) -> Option:
        self._draw_menu()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    self.clean_up()
                    return self.choice

                self._check_tile(event)

                if self.has_chosen:
                    self.reset_attr()
                    self._clear_screen()
                    return self.choice
        return self.choice

    def single_player(self) -> None:
        self.has_chosen = True
        self.choice = Option.SINGLE_PLAYER

    def multi_player(self) -> None:
        self.has_chosen = True
        self.choice = Option.MULTIPLE_PLAYER

    def settings(self):
        self.has_chosen = True
        self.choice = Option.SETTINGS

    def _check_tile(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx, tile in enumerate(self.tile_list):
                if tile.collidepoint(x, y):
                    match Option(idx):
                        case Option.SINGLE_PLAYER:
                            self.single_player()
                        case Option.MULTIPLE_PLAYER:
                            self.multi_player()
                        case Option.SETTINGS:
                            self.settings()
                        case _:
                            raise Exception("Invalid tile")

    def _draw_menu(self):
        # print title
        center_x, center_y = get_center(self.tile_area_width, self.tile_area_height)
        self._print_text(*get_center(0, self.screen_height - 200), text='Tic Tac Toe')
        for i in range(self.tile_number):
            # create tile
            tile = pygame.Rect(center_x, center_y + i * self.tile_gap, self.tile_width, self.tile_height)
            # render font and draw tile
            text_surface = self.font.render(self.texts[i], True, self.font_color, self.tile_color)
            text_rect = text_surface.get_rect(center=tile.center)
            self.tile_list.append(text_rect)
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def _print_text(self, x: int, y: int, text, font_name=None, font_color=pygame.Color('green'), font_background=None) -> None:
        font = pygame.font.Font(font_name, 36)
        if font_background is None:
            text_surface = font.render(text, True, pygame.Color(font_color))
        else:
            text_surface = font.render(text, True, pygame.Color(font_color), pygame.Color(font_background))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def reset_attr(self):
        self.tile_list.clear()

    def clean_up(self):
        self.reset_attr()
        pygame.font.quit()
