import sys
import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves

RED = 'r'
WHITE = 'w'
RED_MAN = 'r'
RED_KING = 'R'
WHITE_MAN = 'w'
WHITE_KING = 'W'
RED_PIECE = [RED_MAN, RED_KING]
WHITE_PIECE = [WHITE_MAN, WHITE_KING]
KINGS = [RED_KING, WHITE_KING]
MEN = [RED_MAN, WHITE_MAN]

TOP_ROW = 0
BOTTOM_ROW = 7

DEATH_ROW_POINT = 200
KING_POINT = 100
ROW_POINT = 10
COLUMN_POINT = 2
PROTECTION_POINT = 3
ALIVE_POINT = 50

def getOpponentColor(color):
    # Returns the opposing color 'w' or 'r'
    if color.lower() == 'r':
        return 'w'
    elif color.lower() == 'w':
        return 'r'
    else:
        return ' '

def getValueBasedOnRow(board, x, y, color):
    value = 0
    # If current coin is red man
    if board[y][x] == color == RED_MAN:
        if y == TOP_ROW:
            value = DEATH_ROW_POINT
        else:
            value = y * ROW_POINT
    # If current coin is white man
    elif board[y][x] == color == WHITE_MAN:
        if y == BOTTOM_ROW:
            value = DEATH_ROW_POINT
        else:
            value = (7-y) * ROW_POINT
    # If current coin is a king
    elif board[y][x] == color.upper():
        value = KING_POINT
    return value

def getValueBasedOnAdjacentPieces(board, x, y, color):
    value = 0
    # Checks if the current coin has a backup.
    if board[y][x].upper() == color.upper() and color in RED_PIECE:
        if y-1 in range(0, 8):
            if x-1 in range(0, 8):
                if board[y-1][x-1].upper() == color.upper() and color in RED_PIECE:
                    value = value + y * PROTECTION_POINT
            if x+1 in range(0, 8):
                if board[y-1][x+1].upper() == color.upper() and color in RED_PIECE:
                    value = value + y * PROTECTION_POINT
    elif board[y][x].upper() == color.upper() and color in WHITE_PIECE:
        if y+1 in range(0, 8):
            if x-1 in range(0, 8):
                if board[y+1][x-1].upper() == color.upper() and color in WHITE_PIECE:
                    value = value + (7-y) * PROTECTION_POINT
            if x+1 in range(0, 8):
                if board[y+1][x+1].upper() == color.upper() and color in WHITE_PIECE:
                    value = value + (7-y) * PROTECTION_POINT
    return value

def getValueBasedOnColumn(board, x, y, color):
    if board[y][x] == color:
        return int(abs(3.5 - x)) * COLUMN_POINT
    return 0

def getValueBasedOnCoinDiff(board, x, y, color):
    opponentColor = gamePlay.getOpponentColor(color)
    # Count how many pieces I have more than the opponent
    value = 0
    if board[y][x] == color:
        value = value + ALIVE_POINT
    elif board[y][x] == opponentColor:
        value = value - ALIVE_POINT
    elif board[y][x] == color.upper():
        value = value + ALIVE_POINT * 2
    elif board[y][x] == opponentColor.upper():
        value = value - ALIVE_POINT * 2
    return value
    
def evaluation(board, color):
    value = 0
    # Loop through all board positions
    rowVal, colVal, alive, adj = 0, 0, 0, 0
    for piece in range(1, 33):
        yx = gamePlay.serialToGrid(piece)
        y = yx[0]
        x = yx[1]
        # Get value based on the difference in the number of coins
        alive = alive + getValueBasedOnCoinDiff(board, x, y, color)
        # Get value of the board based on row
        rowVal = rowVal + getValueBasedOnRow(board, x, y, color)
        # Get value of the board based on column
        colVal = colVal + getValueBasedOnColumn(board, x, y, color)
        # Get value based on adjacency of pieces
        adj = adj + getValueBasedOnAdjacentPieces(board, x, y, color)
    return rowVal + colVal + alive + adj

def getMoveVal(board, color, time, movesRemaining, depth, calculateMax, alpha, beta):
    if depth == 0 or movesRemaining == 0:
        if calculateMax:
            return evaluation(board, color)
        return evaluation(board, getOpponentColor(color))
    moves = getAllPossibleMoves(board, color)
    # Trying to find the move where I have best score
    bestChild = 0 if calculateMax else sys.maxint
    for move in moves:
        newBoard = deepcopy(board)
        gamePlay.doMove(newBoard,move)
        moveVal = getMoveVal(newBoard, getOpponentColor(color), time, movesRemaining, depth - 1, not calculateMax, alpha, beta)
        if calculateMax:
            bestChild = max(moveVal, bestChild)
            alpha = max(alpha, moveVal)
        else:
            bestChild = min(moveVal, bestChild)
            beta = min(beta, moveVal)
        if beta <= alpha:
            break
    return bestChild

def nextMove(board, color, time, movesRemaining):
    moves = getAllPossibleMoves(board, color)
    # Trying to find the move where I have best score
    best = bestMove = None
    for move in moves:
        newBoard = deepcopy(board)
        gamePlay.doMove(newBoard,move)
        moveVal = getMoveVal(newBoard, getOpponentColor(color), time, movesRemaining, 4, False, 0, sys.maxint)
        if best == None or moveVal > best:
            bestMove = move
            best = moveVal
    return bestMove
