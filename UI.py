import pygame

# TODO create GUI with user interaction.

class UI:
    def __init__(self, board):
        pygame.init()
        self.size = width, height = 500, 500
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe")
        self.board = board

    def render(self) -> None:
        """
        Renders the UI with table for Tic Tac Toe.
        Allows user to click on the specific cell to mark player move as 'X'.
        :return:
        """
        pass

    def run(self) -> None:
        """
        Runs the UI.
        :return:
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))  # clear screen to black
            pygame.display.flip()
        pygame.quit()
