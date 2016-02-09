import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves
#import evals

myColor = ""
opponentColor = ""
xyPositions = {}
cornerPositions = {}

def handleError(board, color, time, movesRemaining):
    #fall back to simple greedy, when there is an error in the code.. :)
    moves = getAllPossibleMoves(board, color)
    #Trying to find the move where I have best score
    best = None
    for move in moves:
        newBoard = deepcopy(board)
        gamePlay.doMove(newBoard,move)
        moveVal = evaluation(newBoard, color)
        if best == None or moveVal > best:
            bestMove = move
            best = moveVal
    return bestMove

def nextMove(board, color, time, movesRemaining):
    global myColor
    global opponentColor

    myColor = color
    opponentColor = gamePlay.getOpponentColor(color)
    result = []

    timePerMove = 2*time/float(movesRemaining)

    depth = 1    
    
    if timePerMove <= 0.04:
        depth = 1
    elif timePerMove <= 0.06:
        depth = 2
    elif timePerMove <= 0.1:
        depth = 3
    elif timePerMove <= 0.33:
        depth = 3
    elif timePerMove <= 0.45:
        depth = 4
    elif timePerMove <= 0.6:
        depth = 5
    else:
        depth = 6

    try:
        #result =  minimax_simple(board, color, 7, True)
        result =  minimax_pruning(board, depth, -1000000000000, 1000000000000, True)
    except:
        return handleError(board, color, time, movesRemaining)
    
    if len(result) == 0 or result[0] == None:
        return handleError(board, color, time, movesRemaining)
    
    #print time, "\t", movesRemaining
    return result[0]
    
def isTerminal(node, color):
    return not gamePlay.isAnyMovePossible(node, color)

def heuristic(node):
    global myColor
    #return simpleGreedy.evaluation(node, myColor)
    return evaluation(node, myColor)

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

#utility function..
def evaluation(board, color):
    init() #intitiate all the constants
    # Evaluation function 1
    # Count how many more normal and king pieces I have than the opponent
    global xyPositions 
    global cornerPositions
    opponentColor = gamePlay.getOpponentColor(color)
    
    #count much have the pieces advanced in their y position..
    advancements = 0
    oppAdvancements = 0
    
    #count the pieces..
    man = 0
    king = 0
    opp = 0
    oppKing = 0
    
    #count the corner.. (Corner pieces are the pieces which are along the edges of the square (which cannot be captured at their position..))
    cornerMan = 0
    cornerKing = 0
    cornerOpp = 0
    cornerOppKing = 0
    
    #if a piece is surrounded by the colors of same type, they are better defended by or are defending other pieces. So, they get extra weight..
    neighbors = 0
    oppNeighbors = 0
    
    # Loop through all board positions
    for piece in range(1, 33):
        x, y = xyPositions[piece]
        if board[x][y] == " ":
            continue        #skip if the board position is empty..
        if board[x][y] == color:
            #'''
            if color == "r":
                #these are the advancements in the y position.
                advancements += y 
            else:
                advancements += 7-y
            #''' computing the pieces along the edges..
            man += 1
            if piece in cornerPositions:
                cornerMan += 1    
                
            #computing the similar neighbors surrounding the current piece..    
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == color or board[adv_move[0]][adv_move[1]] == color.upper()):
                    neighbors += 1
            
        elif board[x][y] == opponentColor:
            #'''
            if opponentColor == "r":
                oppAdvancements += y
            else:
                oppAdvancements += 7-y
            #'''
            opp += 1
            #''' computing the pieces along the edges..
            if piece in cornerPositions:
                cornerOpp += 1

            #computing the similar neighbors surrounding the current piece..
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == opponentColor or board[adv_move[0]][adv_move[1]] == opponentColor.upper()):
                    oppNeighbors += 1

        elif board[x][y] == color.upper():
            king += 1
            #''' computing the pieces along the edges..
            if piece in cornerPositions:
                cornerKing += 1
            
            #computing the similar neighbors surrounding the current piece..    
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == color or board[adv_move[0]][adv_move[1]] == color.upper()):
                    neighbors += 1

        elif board[x][y] == opponentColor.upper():
            oppKing += 1
            #''' computing the pieces along the edges..
            if piece in cornerPositions:
                cornerOppKing += 1

            #computing the similar neighbors surrounding the current piece..
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == opponentColor or board[adv_move[0]][adv_move[1]] == opponentColor.upper()):
                    oppNeighbors += 1

    #when the current player has won..
    if opp + oppKing ==0:
        #a very high value weighed by the number of pieces (winning earlier is better)..
        return (man+1.5*king) * 10000000
    
    return (man+0.2*cornerMan+1.4*(king)+0.6*cornerKing + 0.01*neighbors + 0.05*advancements )/(opp+0.2*cornerOpp+1.4*oppKing+0.6*cornerOppKing + 0.01*oppNeighbors + 0.05*oppAdvancements) 
    

#initiates the required constants used..
def init():
    global xyPositions 
    global cornerPositions
    corners = [1, 2, 3, 4, 5, 12, 13, 20, 21, 28, 29, 30, 31, 32] 
    for c in range(1,33):
        xy = gamePlay.serialToGrid(c)
        xyPositions[c] = (xy[0], xy[1]) 
        if c in corners:
            cornerPositions[c] = True       
    
#check whether a particular (x,y) exists on the board    
def isLegalPosition(x,y):
    if x>=0 and x<=7 and y>=0 and y<=7:
        return True
    return False

#get the front positions of the particular position    
def getForwardPositions(x, y, color):
    ret = []
    if color == "r":
        ret.append((x-1, y+1))
        ret.append((x+1, y+1))
    else:
        ret.append((x-1, y-1))
        ret.append((x+1, y-1))
        
    return ret

#get the backward positions of the particular position    
def getBackwardPositions(x, y, color):
    ret = []
    if color == "r":
        ret.append((x-1, y-1))
        ret.append((x+1, y-1))
    else:
        ret.append((x-1, y+1))
        ret.append((x+1, y+1))
        
    return ret        
   
#get the surrounding neighbor positions..   
def getNeighbors(x,y,color):
    ret = []
    ret.append((x-1, y-1))
    ret.append((x+1, y-1))
    ret.append((x-1, y+1))
    ret.append((x+1, y+1))
    return ret        
    


