import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves

xyPositions = {}
cornerPositions = {}

def init():
    global xyPositions 
    global cornerPositions
    corners = [1, 2, 3, 4, 5, 12, 13, 20, 21, 28, 29, 30, 31, 32] 
    for c in range(1,33):
        xy = gamePlay.serialToGrid(c)
        xyPositions[c] = (xy[0], xy[1]) 
        if c in corners:
            cornerPositions[c] = True       
    #print xyPositions
def eval_old(board, color):
    init()
    # Evaluation function 1
    # Count how many more normal and king pieces I have than the opponent
    global xyPositions 
    global cornerPositions
    opponentColor = gamePlay.getOpponentColor(color)
    
    
    #count the pieces..
    man = 0
    king = 0
    opp = 0
    oppKing = 0
    
    #count the defendedPieces..
    cornerMan = 0
    cornerKing = 0
    cornerOpp = 0
    cornerOppKing = 0
    
    neighbors = 0
    oppNeighbors = 0
    
    # Loop through all board positions
    for piece in range(1, 33):
        x, y = xyPositions[piece]          
        if board[x][y] == color:
            man += 1
            if piece in cornerPositions:
                cornerMan += 1    
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == color or board[adv_move[0]][adv_move[1]] == color.upper()):
                    neighbors += 1
        elif board[x][y] == opponentColor:
            opp += 1
            if piece in cornerPositions:
                cornerOpp += 1
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == opponentColor or board[adv_move[0]][adv_move[1]] == opponentColor.upper()):
                    oppNeighbors += 1
        elif board[x][y] == color.upper():
            king += 1
            if piece in cornerPositions:
                cornerKing += 1
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == color or board[adv_move[0]][adv_move[1]] == color.upper()):
                    neighbors += 1
        elif board[x][y] == opponentColor.upper():
            oppKing += 1
            if piece in cornerPositions:
                cornerOppKing += 1
            neigh = getNeighbors(x,y,color)
            for adv_move in neigh:
                if isLegalPosition(adv_move[0], adv_move[1]) and (board[adv_move[0]][adv_move[1]] == opponentColor or board[adv_move[0]][adv_move[1]] == opponentColor.upper()):
                    oppNeighbors += 1

    if opp + oppKing ==0:
        #a very high value weighed by the number of pieces (winning earlier is better)..
        return (man+1.5*king) * 10000000

    return (man+0.2*cornerMan+1.4*(king)+0.6*cornerKing + 0.01*neighbors)/(opp+0.2*cornerOpp+1.4*oppKing+0.6*cornerOppKing + 0.01*oppNeighbors) 
        
    
def isLegalPosition(x,y):
    if x>=0 and x<=7 and y>=0 and y<=7:
        return True
    return False
    
def getForwardPositions(x, y, color):
    ret = []
    if color == "r":
        ret.append((x-1, y+1))
        ret.append((x+1, y+1))
    else:
        ret.append((x-1, y-1))
        ret.append((x+1, y-1))
        
    return ret
    
def getBackwardPositions(x, y, color):
    ret = []
    if color == "r":
        ret.append((x-1, y-1))
        ret.append((x+1, y-1))
    else:
        ret.append((x-1, y+1))
        ret.append((x+1, y+1))
        
    return ret        
   
def getNeighbors(x,y,color):
    ret = []
    ret.append((x-1, y-1))
    ret.append((x+1, y-1))
    ret.append((x-1, y+1))
    ret.append((x+1, y+1))
    return ret        
