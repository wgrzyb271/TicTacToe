import pygame

# TODO create GUI with user interaction.

def print_fields(list) -> None:
    if len(list) > 0:
        print(list)


class UI:
    def __init__(self, board, board_size, board_fields):
        pygame.init()
        self.size = width, height = 800, 800
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe")
        self.board = board
        self.board_size = board_size
        self.board_fields = board_fields
        self.rect_size = 100
        self.total_area = self.rect_size * self.board_fields
        self.rect_list = []
        self.occupied_field = [False for _ in range(board_fields)]
        self.player_move_list = []

    def run(self) -> None:
        """
        Runs the UI.
        :return:
        """
        running = True

        self._draw_board()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self._render(event)
        pygame.quit()

    def get_player_moves(self) -> list:
        return self.player_move_list

    def _render(self, event) -> None:
        """
        Renders the UI with table for Tic Tac Toe.
        Allows user to click on the specific cell to mark player move as 'X'.
        :return:
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            self._mark_player_move(position)
        pygame.display.flip()

    def _mark_player_move(self, position: tuple) -> None:
        """
        Registers the move on the board.
        """
        x, y = position
        for field, rect in enumerate(self.rect_list):
            if rect.collidepoint(x, y) and not self.occupied_field[field]:
                self.player_move_list.append(field)
                self.occupied_field[field] = True
                x, y = rect.topleft
                self._draw_x(x, y)
                print_fields(self.player_move_list)

    def _mark_ai_move(self, field) -> None:
        if not self.occupied_field[field]:
            self.occupied_field[field] = True
            rect = self.rect_list[field]
            x, y = rect.center
            self._draw_o(x, y)

    def _draw_o(self, x: int, y: int) -> None:
        """
        Draws the O mark (move).
        """
        # offset so there is no holes in rects
        offset = 1
        radius = self.rect_size / 2 - offset
        pygame.draw.circle(self.screen, pygame.Color('red'), (x, y), radius, 2)

    def _draw_x(self, x: int, y: int) -> None:
        """
        Draws the X mark (move).
        """
        pygame.draw.line(self.screen, pygame.Color('green'), (x, y), (x + self.rect_size, y + self.rect_size), 2)
        pygame.draw.line(self.screen, pygame.Color('green'), (x + self.rect_size, y), (x, y + self.rect_size), 2)

    def _draw_board(self):
        """
        Draws the board specific size on the screen.
        """
        screen_width, screen_height = pygame.display.get_surface().get_size()
        for i in range(self.board_size):
            for j in range(self.board_size):
                center_x = (abs(screen_width - self.total_area / self.board_size)) / 2
                center_y = (abs(screen_height - self.total_area / self.board_size)) / 2
                current_rect = pygame.Rect(center_x + self.rect_size * j, center_y + self.rect_size * i, self.rect_size,
                                           self.rect_size)
                # save rect cords for later usage
                self.rect_list.append(current_rect)
                pygame.draw.rect(self.screen, pygame.Color('blue'), current_rect, 2)
        pygame.display.flip()


