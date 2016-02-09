import gamePlay
import math
import random
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves


maxColor = ''
def evaluation(board, color):
    # Evaluation function 1
    # Count how many more pieces I have than the opponent
	opponentColor = gamePlay.getOpponentColor(color)
    #print opponentColor, "OPPPPPPPPPPPPPPPPPPOOOOO"
	value = 0
	for piece in range(1, 33):
		xy = gamePlay.serialToGrid(piece)
		x = xy[0]
		y = xy[1]
		'''if gamePlay.countPieces(board, color) <=4 or gamePlay.countPieces(board, opponentColor) <=4:
			if board[x][y].upper() == color.upper():
				value = value + 2					
			if board[x][y].upper() == opponentColor.upper():
				value = value - 2
			if color == maxColor:
				if board[x][y].upper() == color.upper():
					value = value + 4					
				if board[x][y].upper() == opponentColor.upper():
					value = value - 4	
				if (x == 7):
					value = 4*value
				if (x == 0):
					value = 0.4 * value
			if color == gamePlay.getOpponentColor(maxColor):
				if board[x][y].upper() == color.upper():
					value = value - 4					
				if board[x][y].upper() == opponentColor.upper():
					value = value - 4	
				if (x == 7):
					value = 0.4*value
				if (x == 0):
					value = 4 * value'''
		#My evaluation function is currently simple as I am checking where I am currently present and if the board moves to opposite end, then I am giving extra weight to that coin since, it will change as king and similarly if the opponent's coin is in opponent's place then I will deduce more from it.If it is my starting place, then I am giving less weight for it and vice versa. It wins in both odd and even depth, Make sure, if you are increasing more depth, please increase the time limit, or it may get timed out. I have some of the evaluation strategies commented out as I would be using that in tournament and since It is getting timeout, if I use too much strategies, I used simple strategy now, which wins all the games out of 100 games that i tested in odd and even depths and with playing first and second
		#Evaluation starts here
		if board[x][y].upper() == color.upper():
			value = value + 1					
		if board[x][y].upper() == opponentColor.upper():
			value = value - 1
		if color == maxColor:   # Checking for whether I am playing with Max color
			if board[x][y].upper() == color.upper():
				value = value + 2					
			if board[x][y].upper() == opponentColor.upper():
				value = value - 2	
			if (x == 7):    # Checking whether the Player is in  end of the board
				value = 2*value
			if (x == 0):    # Checking whether the Player is in opposite end
				value = 0.2 * value
		if color == gamePlay.getOpponentColor(maxColor): # Taking the color of opponent
			if board[x][y].upper() == color.upper():
				value = value - 2					
			if board[x][y].upper() == opponentColor.upper():
				value = value - 2	
			if (x == 7):
				value = 0.2*value
			if (x == 0):
				value = 2 * value
		
				'''if gamePlay.canMoveToPosition(board, x, y, x-1, y-1) == True:			
					value = value
				if gamePlay.canMoveToPosition(board, x, y, x-1, y+1) == True:			
					value = 0.25*value
				if gamePlay.canMoveToPosition(board, x, y, x+1, y-1) == True:			
					value = 0.25*value
				if gamePlay.canMoveToPosition(board, x, y, x+1, y+1) == True:			
					value = 0.25*value
				#if gamePlay.countPieces(board, color) >=6 and gamePlay.countPieces(board, opponentColor) >=6:'''
	return value # returning the value
	'''for piece in range(1, 33):
		xy = gamePlay.serialToGrid(piece)
		x = xy[0]
		y = xy[1]
                
		if board[x][y].upper() == color.upper():
			value = value + 1
		elif board[x][y].upper() == opponentColor.upper():
			value = value - 1
	return value'''
	# Loop through all board positions
	'''for piece in range(1,33):
		xy = gamePlay.serialToGrid(piece)
		x = xy[0]
		y = xy[1]
	
	#print board[x][y], "Normal"       
	#print board[x][y].upper(), "Upper"
	#print gamePlay.countPieces(board, color), "piecessssss"
		if gamePlay.countPieces(board, color) >=6 and gamePlay.countPieces(board, opponentColor) >=6: 
			if board[x][y] == color:
				if (x == 7 and (y == 0 or y == 2 or y == 4 or y == 6)):
					value = value + 2
				if gamePlay.canMoveToPosition(board, x, y, x-1, y-1) == True:			
					value = value + 1
				if gamePlay.canMoveToPosition(board, x, y, x-1, y+1) == True:			
					value = value + 1
				if gamePlay.canMoveToPosition(board, x, y, x+1, y-1) == True:			
					value = value + 1
				if gamePlay.canMoveToPosition(board, x, y, x+1, y+1) == True:			
					value = value + 1		
				elif board[x][y].upper() == color.upper():
		    			value = value + 1
			elif board[x][y] == opponentColor:
			if (x == 0 and (y == 1 or y == 3 or y == 5 or y == 7)):
				value = value - 2
			if gamePlay.canMoveToPosition(board, x, y, x-1, y-1) == True:			
				value = value - 1
			if gamePlay.canMoveToPosition(board, x, y, x-1, y+1) == True:			
				value = value - 1
			if gamePlay.canMoveToPosition(board, x, y, x+1, y-1) == True:			
				value = value - 1
			if gamePlay.canMoveToPosition(board, x, y, x+1, y+1) == True:			
				value = value - 1
		elif ((gamePlay.countPieces(board, color) <=6) and (gamePlay.countPieces(board, opponentColor) >=6)):
			if board[x][y].upper() == color.upper():
		    		value = value + 4
			if (x == 7 and (y == 0 or y == 2 or y == 4 or y == 6)):
				value = value + 2
			if gamePlay.canMoveToPosition(board, x, y, x-1, y-1) == True:			
				value = value + 1
			if gamePlay.canMoveToPosition(board, x, y, x-1, y+1) == True:			
				value = value + 1
			if gamePlay.canMoveToPosition(board, x, y, x+1, y-1) == True:			
				value = value + 1
			if gamePlay.canMoveToPosition(board, x, y, x+1, y+1) == True:			
				value = value + 1		
		
		elif board[x][y] == opponentColor:
			if board[x][y].upper() == opponentColor.upper():
				value = value - 4
			if (x == 0 and (y == 1 or y == 3 or y == 5 or y == 7)):
				value = value - 1
			if gamePlay.canMoveToPosition(board, x, y, x-1, y-1) == True:			
				value = value - 0.5
			if gamePlay.canMoveToPosition(board, x, y, x-1, y+1) == True:			
				value = value - 0.5
			if gamePlay.canMoveToPosition(board, x, y, x+1, y-1) == True:			
				value = value - 0.5
			if gamePlay.canMoveToPosition(board, x, y, x+1, y+1) == True:			
				value = value - 0.5
	return value'''


def alphabetaPruning(board,color,alpha,beta, depth, maxval,movesRemaining):
	if depth == 0 or movesRemaining == 0:  # Checking whether I am in the end node, then I will return my evaluation value
		return evaluation(board, maxColor)
	moves = getAllPossibleMoves(board,color)	# Getting all values of the new board that I passed from nextMove
        opponentColor = gamePlay.getOpponentColor(color) # Getting the opponent color
	test = float("inf") # Assigning value for infinity
	if maxval:    #Checking whether maxval is Max
		value = -test #Assigning the value of -infnity to value
		for move in moves: # looping through all the moves
			evalBoard = deepcopy(board) #Taking the deepcopy of board
			gamePlay.doMove(evalBoard,move)
			#value = evaluation(evalBoard, color)
			#print value, "VALUE"
			value = max(value,alphabetaPruning(evalBoard,opponentColor,alpha,beta, depth-1, False,movesRemaining)) # performing recursive call and assigning the maximum value to the "value"
			alpha = max(alpha, value) # Assigning the max value to alpha
			if beta <= alpha: #checking whether beta is lesser than alpha
				break
		return value # returning the value
	else:
		value = test # Assigning the positive max value to alpha
		for move in moves: # iterating through all the values
			evalBoard = deepcopy(board) #Making a deepcopy
			#value = evaluation(evalBoard, color)	
			gamePlay.doMove(evalBoard,move)
			value = min(value,alphabetaPruning(evalBoard,opponentColor,alpha,beta, depth-1, True, movesRemaining))	# Performing the recursive call and assigning the minimum value to "value"		
			#value = min(move, alphabetaPruning(move, depth-1, True))
			beta = min(beta, value) # Assiging the minumum value to beta by comparing beta and value
			if beta <= alpha: # checking whether beta is lesser than   alpha
				break
		return value	# returning the value

def nextMove(board, color, time, movesRemaining):
    test = float("inf") # Assigning the inifinity to test
    global maxColor # making the maxColor global variable that has been assigned at the top
    maxColor = color #Assigning the max color to maxColor
    moves = getAllPossibleMoves(board, color) #getting all posible moves
    opponentColor = gamePlay.getOpponentColor(color) #getting the moves of opponent
    #Trying to find the move where I have best score
    best = None
    finalVal = 0
    for move in moves: #iterating throug the board
        newBoard = deepcopy(board) #making the newcopy of board
        gamePlay.doMove(newBoard,move) #performing the move action
	if movesRemaining >50:
		finalVal = alphabetaPruning(newBoard,opponentColor,-test,test, 5, False,movesRemaining) #calling alphabeta pruning function
	else:
		finalVal = alphabetaPruning(newBoard,opponentColor,-test,test, 3, False,movesRemaining)
        if best == None or finalVal > best: #checking the condition 
            bestMove = move
            best = finalVal
    return bestMove #Returning the best Move
