"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    if count_x == count_o:
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (i, j)
    available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j)
    on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")

    new_board = [row.copy() for row in board]

    i, j = action

    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winning_lines = [
        # Horizontales
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        # Verticales
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        # Diagonales
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for line in winning_lines:
        values = [board[i][j] for i, j in line]

        if values[0] is not None and values.count(values[0]) == 3:
            return values[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Caso 1: algún jugador ganó
    if winner(board) is not None:
        return True

    # Caso 2: no quedan casillas disponibles
    if len(actions(board)) == 0:
        return True

    # Caso 3: la partida continúa
    return False


def utility(board):
    """
    Returns 1 if X has won the game,
    -1 if O has won, 0 otherwise.
    """

    game_winner = winner(board)

    if game_winner == X:
        return 1

    if game_winner == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    def max_value(state):
        if terminal(state):
            return utility(state)

        value = float("-inf")

        for action in actions(state):
            value = max(value, min_value(result(state, action)))

        return value

    def min_value(state):
        if terminal(state):
            return utility(state)

        value = float("inf")

        for action in actions(state):
            value = min(value, max_value(result(state, action)))

        return value

    current_player = player(board)
    best_action = None

    if current_player == X:
        best_value = float("-inf")

        for action in actions(board):
            value = min_value(result(board, action))

            if value > best_value:
                best_value = value
                best_action = action

    else:
        best_value = float("inf")

        for action in actions(board):
            value = max_value(result(board, action))

            if value < best_value:
                best_value = value
                best_action = action

    return best_action

