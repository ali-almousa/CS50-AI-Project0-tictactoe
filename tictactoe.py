"""
Tic Tac Toe player
"""
import copy
import math
import random

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    :return: starting state of the board
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    :param board:
    :return: player who has the next turn on a given board
    """
    # if the board is empty it's X's turn
    if board == initial_state():
        return X
    # count how many Xs and Os in the board
    total_Xs = 0
    total_Os = 0
    for row in board:
        total_Xs += row.count("X")
        total_Os += row.count("O")
    # Xs more than Os it's O's turn
    if total_Xs > total_Os:
        return O
    # else it's X's turn
    else:
        return X

def actions(board):
    """
    :param board:
    :return: set of all possible actions (i, j) available on in the board
    """
    # create an empty set to hold tuples of possible moves
    possible_moves = set()
    # iterate through the board, for every empty cell add its coordinate to the set
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] is None:
                possible_moves.add((row, col))
    # return the set
    return possible_moves

def result(board, action):
    """
    :param board:
    :param action:an action (i, j)
    :return: the board that results from making the move action on the board
    """
    # validate the passed action
    if board[action[0]][action[1]] != EMPTY or action[0] >= 3 or action[1] >= 3:
        raise Exception("Invalid action!")
    # proceed with causious through the try block
    try:
        # create a deep copy to avoid modifying the original board
        copy_board = copy.deepcopy(board)
        turn = player(board)
        copy_board[action[0]][action[1]] = turn
        # return the board after applying the action
        return copy_board
    except Exception as e:
        print(f"Ops there is something wrong: {e}")


def winner(board):
    """
    :param board:
    :return:the winner of the game if there is
    """
    # check horizontally
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    # check diagonally
    left_diagonal = [board[i][i] for i in range(len(board))]
    right_diagonal = [board[i][2 - i] for i in range(len(board))]
    if left_diagonal.count(O) == 3 or right_diagonal.count(O) == 3:
        return O
    if left_diagonal.count(X) == 3 or right_diagonal.count(X) == 3:
        return X

    # check vertically
    cols = [[board[0][i], board[1][i], board[2][i]] for i in range(len(board))]
    for col in cols:
        if col.count(X) == 3:
            return X
        elif col.count(O) == 3:
            return O
    # otherwise return None
    return None

def terminal(board):
    """
    :param board:
    :return: True if game is over, False otherwise
    """
    # A True value returned from winner() means the game is over
    if winner(board):
        return True
    # if the board is completely filled with Xs and Os, the game is over
    return all(True if row.count(EMPTY) == 0 else False for row in board)

def utility(board):
    """
    :param board:
    :return: 1 if X has won the game, -1 if O has won, 0 otherwise
    """
    # X wins
    if winner(board) == X:
        return 1
    # O wins
    if winner(board) == O:
        return -1
    # No one wins
    else:
        return 0

def minimax(board):
    """
    :param board:
    :return: the optimal action for the current player on the board
    """
    # if the board is empty return any action to apply
    if board == initial_state():
        return list(actions(board))[random.randrange(0, 9)]
    # if the game is over return None
    elif terminal(board):
        return None
    # lists for moves and their value of state
    O_moves = []
    X_moves = []
    # if it's X's turn go here
    if player(board) == X:
        # iterate through all possible actions
        for action in actions(board):
            # append every action possible with its value of state
            X_moves.append((MIN_VALUE(result(board, action)), action))
            # sort the list then choose the last action of the list as it has the highest value of state
        return sort(X_moves)[-1][1]
    # if it's O's turn go here
    elif player(board) == O:
        # iterate through all possible actions
        for action in actions(board):
            # append every action possible with its value of state
            O_moves.append((MAX_VALUE(result(board, action)), action))
            # sort the list then choose the first action of the list as it has the smallest value of state
        return sort(O_moves)[0][1]



def MAX_VALUE(board):
    """
    :param board: current board
    :return: the value of the state after terminating the recursive process
    """
    # if the board is in terminal state then return the utility of that board
    if terminal(board):
        return utility(board)
    # set v to the lowest value possible so we can be sure that anything would be greater
    v = -math.inf
    # keep iterating through the actions recursively with MIN_VALUE until reaching the terminal state
    for action in actions(board):
        v = max(v, MIN_VALUE(result(board, action)))
    return v

def MIN_VALUE(board):
    """
    :param board: current board
    :return: the value of the state after terminating the recursive process
    """
    # if the board is in terminal state then return the utility of that board
    if terminal(board):
        return utility(board)
    # set v to the highest value possible so we can be sure that anything would be smaller
    v = math.inf
    # keep iterating through the actions recursively with MIN_VALUE until reaching the terminal state
    for action in actions(board):
        v = min(v, MAX_VALUE(result(board, action)))
    return v

def sort(lst):
    """
    :param lst: a list
    :return: a sorted copy of the list
    """
    sorted_list = sorted(lst)
    return sorted_list


