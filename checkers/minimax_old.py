import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves
import evals
import simpleGreedy

myColor = ""
opponentColor = ""

def nextMove(board, color, time, movesRemaining):
    global myColor
    global opponentColor

    myColor = color
    opponentColor = gamePlay.getOpponentColor(color)

    #result =  minimax_simple(board, color, 7, True)
    result =  minimax_pruning(board, 5, -1000000000000, 1000000000000, True)
    #print "$"*40
    #print result[0]
    #print time, "\t", movesRemaining
    return result[0]
    
def isTerminal(node, color):
    return not gamePlay.isAnyMovePossible(node, color)

def heuristic(node):
    global myColor
    #return simpleGreedy.evaluation(node, myColor)
    return evals.eval_old(node, myColor)
#TODO: define currPlayer..
'''
Code inspired from pseudo code in https://en.wikipedia.org/wiki/Minimax 
'''
#simple minimax without alpha-beta pruning
def minimax_simple(node, depth, maximizingPlayer):
    global myColor
    global opponentColor
    color = opponentColor
    if maximizingPlayer:
        color = myColor
        
    if depth == 0 or isTerminal(node, color):
        return (None, heuristic(node))
    bestMove = None
    moves = getAllPossibleMoves(node, color)
    if maximizingPlayer:
        bestValue = -1000000000000
        for move in moves:
            newBoard = deepcopy(node)
            gamePlay.doMove(newBoard,move)
            moveVal = minimax_simple( newBoard, depth-1, False)
            if bestValue < moveVal[1]:
                bestValue = moveVal[1]
                bestMove = move
    else:
        bestValue = 1000000000000
        for move in moves:
            newBoard = deepcopy(node)
            gamePlay.doMove(newBoard,move)
            moveVal = minimax_simple( newBoard, depth-1, True)
            if bestValue > moveVal[1]:
                bestValue = moveVal[1]
                bestMove = move

    return (bestMove, bestValue)
    
'''
Code inspired from pseudo code in https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
'''
#minimax with alpha-beta pruning
def minimax_pruning(node, depth, alpha, beta, maximizingPlayer):
    global myColor
    global opponentColor
    color = opponentColor
    if maximizingPlayer:
        color = myColor

    if depth == 0 or isTerminal(node, color):
        return (None, heuristic(node))
    #gamePlay.printBoard(node)
    bestMove = None
    moves = getAllPossibleMoves(node, color)
    if maximizingPlayer:
        bestValue = -1000000000000
        for move in moves:
            newBoard = deepcopy(node)
            gamePlay.doMove(newBoard,move)
            moveVal = minimax_pruning( newBoard, depth-1, alpha, beta, False)
            if bestValue < moveVal[1]:
                bestValue = moveVal[1]
                bestMove = move #TODO: check this logic..
            alpha = max(bestValue, alpha)
            if beta <= alpha:
                break
    else:
        bestValue = 1000000000000
        for move in moves:
            newBoard = deepcopy(node)
            gamePlay.doMove(newBoard,move)
            moveVal = minimax_pruning( newBoard, depth-1, alpha, beta, True)
            if bestValue > moveVal[1]:
                bestValue = moveVal[1]
                bestMove = move #TODO: check this logic..
            beta = min(beta, bestValue)
            
            if beta <= alpha:
                break

    return (bestMove, bestValue)

