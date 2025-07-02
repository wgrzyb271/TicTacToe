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
        self.size = size
        self.board = [['-1'] * self.size] * self.size
        # self.board = [
        #
        #     ['-1', '-1', '-1'],
        #     ['-1', '-1', '-1'],
        #     ['O', 'O', '-1']

        # ['-1', '-1', 'O'],
        # ['-1', 'O', '-1'],
        # ['O', 'O', '-1']

        # ['O', '-1', '-1'],
        # ['-1', 'O', '-1'],
        # ['O', 'O', 'O']

        # ['-1', '-1', '-1'],
        # ['-1', '-1', '-1'],
        # ['O', 'O', 'O']

        # ['X', 'X', 'X'],
        # ['-1', '-1', '-1'],
        # ['-1', '-1', '-1']

        # ]
        self.player_mark = 'X'
        self.ai_mark = 'O'
        self.winner = None

    def __str__(self):
        for row in self.board:
            print(row, end=' ')
            print()

    def check_for_win(self) -> str:
        """
        Checks if there is a winner, if yes then return the winner.
        :return:
        """

        self.check_diagonal()
        self.check_rows()
        self.check_columns()

        return self.winner

    def check_diagonal(self) -> str:
        """
        Check diagonal for winner and mark the winner.
        :return:
        """
        for field in range(self.size):
            # check left diagonal
            if self.board[field][field] == self.board[field + 1][field + 1] == self.board[field + 2][field + 2] != '-1':
                self.winner = self.board[field + 1][field + 1]

            # check right diagonal
            if self.board[field + 2][field] == self.board[field + 1][field + 1] == self.board[field][field + 2] != '-1':
                self.winner = self.board[field + 1][field + 1]

            return self.winner

    def check_columns(self) -> str:
        """
        Check columns for winner and mark the winner.
        :return:
        """
        for col in range(self.size):
            for row in range(self.size):
                # check if there is a match any other than '-1'
                if self.board[row][col] != '-1':
                    self.winner = self.board[row][col]
                    return self.winner

    def check_rows(self) -> str:
        """
        Check row for winner and mark the winner.
        :return:
        """
        for row in self.board:
            # check if there is a match any other than ['-1', '-1', '-1']
            if row != ['-1', '-1', '-1']:
                self.winner = row[0]
                return self.winner
