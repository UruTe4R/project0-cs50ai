"""
Tic Tac Toe Player
"""

import math
import copy

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
    MAX_TURN = 9
    empty_count = 0
    for row in board:
        for cell in row:
            if cell == EMPTY:
                empty_count += 1
    
    turn = MAX_TURN - empty_count
    if turn % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_moves.add((i, j))

    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    # Valid Move?
    if board[i][j] != EMPTY or action not in actions(board):
        raise Exception("Invalid Action")
    board_copy = copy.deepcopy(board)
    board_copy[i][j] = player(board_copy)

    return board_copy
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    left_vertical = []
    center_vertical = []
    right_vertical = []
    diagonals = [[],[]]
    for i, row in enumerate(board):
        # Horizontal Win
        if all(X == cell_in_row for cell_in_row in row):
            return X
        
        if all(O == cell_in_row for cell_in_row in row):
            return O

        # Create Column
        left_vertical.append(row[0])
        center_vertical.append(row[1])
        right_vertical.append(row[2])

        # Create Diagonal
        diagonals[0].append(row[i])
        diagonals[1].append(row[2 - i])

    # Vertical Win
    if all(X == cell_in_column for cell_in_column in left_vertical) or all(X == cell_in_column for cell_in_column in center_vertical) or all(X == cell_in_column for cell_in_column in right_vertical):
        return X

    if all(O == cell_in_column for cell_in_column in left_vertical) or all(O == cell_in_column for cell_in_column in center_vertical) or all(O == cell_in_column for cell_in_column in right_vertical):
        return O

    # Diagonal Win
    if all(X == cell_in_diagonal for cell_in_diagonal in diagonals[0]) or all(X == cell_in_diagonal for cell_in_diagonal in diagonals[1]):
        return X

    if all(O == cell_in_diagonal for cell_in_diagonal in diagonals[0]) or all(O == cell_in_diagonal for cell_in_diagonal in diagonals[1]):
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Assume board is fullfilled
    fullfilled = True

    for row in board:
        for cell in row:
            # if cell is empty, board is not fulfilled
            if cell == EMPTY:
                fullfilled = False

    # There is a winner
    if winner(board) is not None:
        return True
    # End with tie
    if winner(board) is None and fullfilled:
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Tie
    if winner(board) == None:
        return 0
    # X is the winner
    if winner(board) == X:
        return 1
    # O is the winner
    if winner(board) == O:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
        
    score_and_action = []
    if player(board) == X:
        for action in actions(board):
            v = min_value(result(board, action))
            score_and_action.append((v, action))
            if v == 1:
                return action
        return max(score_and_action, key=lambda x: x[0])[1]

    if player(board) == O:
        for action in actions(board):
            v = max_value(result(board, action))
            score_and_action.append((v, action))
            if v == -1:
                return action
        return min(score_and_action, key=lambda x: x[0])[1]
    

def max_value(board):

    # Assume the value is -infinity because the player is trying to maximize its value
    value = -math.inf

    # if the game is over, return the utility point
    if terminal(board):
        return utility(board)
    
    # What are min's possible moves
    for action in actions(board):
        board_after_move = result(board, action)
        min_move_v = min_value(board_after_move)
        value = max(value, min_move_v)
    return value

def min_value(board):

    # Assume the value is infinity because the player is trying to minimize its value
    value = math.inf

    # if the game is over, return the utility point
    if terminal(board):
        return utility(board)
    
    # What are possible moves
    for action in actions(board):
        board_after_move = result(board, action)
        max_move_v = max_value(board_after_move)
        value = min(value, max_move_v)
    return value
