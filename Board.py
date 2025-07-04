# TODO fix make_move and especially undo_move.
class Board:
    """
    Description of TicTacToe model
    representation - N
    acceptable operations - A
    initial state - S
    final state - G

    m_i - player/ai move at field i

    N = { [ [m_0, m_1, m_2], [m_3, m_4, m_5], [m_6, m_7, m_8] ],
    m_i ∈ { '-1', 'X', 'O'}, i ∈ {0, 1, 2, ..., 8} }

    free field -> -1
    player move - X
    ai move - O

    specific player move - Y
    any move - J

    A = { 'X', 'O' }
    S = { [ [-1, -1, -1], [-1, -1, -1], [-1, -1, -1] ] }
    G = {
    [
    [Y, Y, Y],
    [J, J, J],
    [J, J, J]
    ],
    [
    [J, J, J],
    [Y, Y, Y],
    [J, J, J]
    ],
    [
    [J, J, J],
    [J, J, J],
    [Y, Y, Y]
    ],
    [
    [Y, J, J],
    [J, Y, J],
    [J, J, Y]
    ],
    [
    [J, J, Y],
    [J, Y, J],
    [Y, J, J]
    ]}

    field numbering:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

    """

    def __init__(self, size=3):
        self.board_size = size
        self.field_number = self.board_size ** 2
        self.free_field = self.field_number
        self.board = ['-1'] * self.field_number

        self.remaining_move_list = [field for field in range(0, self.field_number)]
        self.ai_marked_field = None
        self.turn = 'X'
        self.index_element = None
        self.move_history = []  # list of tuples (field, index_before_removal)

        # self.board = [
        # '-1', '-1', '-1',
        # '-1', '-1', '-1',
        # 'O', 'O', '-1']

        # '-1', '-1', 'O',
        # '-1', 'O', '-1',
        # 'O', 'O', '-1']

        # 'O', '-1', '-1',
        # '-1', 'O', '-1',
        # 'O', 'O', 'O']

        # '-1', '-1', '-1',
        # '-1', '-1', '-1',
        # 'O', 'O', 'O']

        # 'O', 'O', 'O',
        # '-1', '-1', '-1',
        # 'O', 'O', 'O']

        # 'O', 'O', 'O', '-1',
        # '-1', '-1', '-1', '-1',
        # '-1', '-1', '-1', '-1',
        # '-1', '-1', '-1', '-1']

        # 'O', '-1', '-1',
        # 'O', '-1', '-1',
        # 'O', '-1', '-1']

        # '-1', '-1', 'O',
        # '-1', '-1', 'O',
        # '-1', '-1', 'O']

        # ['X', 'X', 'X'],
        # ['-1', '-1', '-1'],
        # ['-1', '-1', '-1']

        #
        self.player_mark = 'X'
        self.ai_mark = 'O'
        self.winner = None

    def __str__(self):
        print()
        for field in range(self.field_number):
            if field % self.board_size == 0 and field != 0:
                print()
                print('-----' * self.board_size)
            print("%2s |" % self.board[field], end=' ')
        print()

    def check_for_win(self) -> bool:
        """
        Checks if there is a winner, if yes then return the winner.
        :return:
        """
        self.winner = None # reset winner
        self.check_diagonal()
        self.check_rows()
        self.check_columns()
        if self.winner is not None:
            return True
        else:
            return False

    def check_diagonal(self) -> str:
        """
        Check diagonal for winner and mark the winner.
        :return:
        """
        # check left diagonal
        if self.board[0] == self.board[self.board_size + 1] == self.board[self.board_size * 2 + 2] != '-1':
            self.winner = self.board[0]
            return self.winner

        # check right diagonal
        if self.board[self.board_size - 1] == self.board[self.board_size + 1] == self.board[
            self.board_size * 2] != '-1':
            self.winner = self.board[self.board_size - 1]
            return self.winner

    def check_columns(self) -> str:
        """
        Check columns for winner and mark the winner.
        :return:
        """
        for col in range(0, self.board_size):
            if self.board[col] == self.board[col + self.board_size] == self.board[col + self.board_size * 2] != '-1':
                self.winner = self.board[col]
                return self.winner

    def check_rows(self) -> str:
        """
        Check row for winner and mark the winner.
        :return:
        """
        for row in range(0, self.field_number, self.board_size):
            if self.board[row] == self.board[row + 1] == self.board[row + 2] != '-1':
                self.winner = self.board[row]
                return self.winner

    def is_full(self) -> bool:
        """
        Checks if board is full.
        :return:
        """
        if self.free_field > 0:
            return False
        else:
            return True

    def available_moves(self) -> list:
        if self.is_full():
            return []
        else:
            self.remaining_move_list = [i for i, field in enumerate(self.board) if field == "-1"]
            return self.remaining_move_list

    def print_winner(self) -> None:
        """
        Print winner.
        """
        print(f'\n\nWinner: {self.winner}\n')

    def make_move(self, player: str, field: int) -> bool:
        if field is not None and self.board[field] == '-1':
            self.board[field] = player
            self.free_field -= 1
            return True
        return False

    def undo_move(self, field):
        self.board[field] = '-1'
        self.free_field += 1
        # self.__str__()

    def player_move(self, field):
        result = self.make_move(self.player_mark, field)

        return result


    def ai_move(self, field):
        self.make_move(self.ai_mark, field)
        # self.__str__()
