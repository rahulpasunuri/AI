import random
import sys
#import dill
import pickle

map = [[" "," "," "],
       [" "," "," "],
       [" "," "," "]]

player1Char = "X"
player2Char = "Y"

player1Moves = []
player2Moves = []
winner = 0

maxTrainGames = 0
maxLimit = 10000
#maxLimit = 2
alpha = 0.05

value = {}

def getOpponentChar(playerChar):
    if playerChar == "X":
        return "O"
    return "X"
        
#returns the symbol used by the AI.
def getAIChar():
    if turn == "X":
        return "O"
    return "X"


def isWinning(board, playerChar):
    wonSymbol = ""
    for i in range(0,3):
        #check row wise..
        if board[i][0] == board[i][1] == board[i][2] == playerChar:
            return True

        #check every column..
        if board[0][i] == board[1][i] == board[2][i] == playerChar:
            return True

    #check diagonals..
    if (board[0][0] == board[1][1] == board[2][2] == playerChar) or (board[0][2] == board[1][1] == board[2][0] == playerChar):
        return True

    return False  


def isLosing(board, playerChar):
    return isWinning(board, getOpponentChar(playerChar))

def setValue(board, playerChar, val, pos):
    print playerChar, val, pos
    state = getStateFromBoard(board, playerChar)
    if state not in value:
        value[state] = {}

    value[state][pos] = val

def getValue(board, playerChar, pos):
    state = getStateFromBoard(board, playerChar)
    if state not in value:
        value[state] = {}
    board[pos[0]][pos[1]] = playerChar
    if pos not in value[state]:    
         if isLosing(board, playerChar):
                value[state][pos] = 0
         elif isWinning(board, playerChar):
                value[state][pos] = 1
         elif "W" not in state: #its a draw..
                value[state][pos] = 0.5
         else:                
                value[state][pos] = 0.5

    board[pos[0]][pos[1]] = " "
    return value[state][pos]

def getStateFromBoard(board, playerChar):
    state = ""
    for i in range(0,3):
        for j in range(0,3):
            val = map[i][j]
            rep = "O"
            if val == playerChar:
                rep = "P"
            elif val == " ":
                rep = "W"
            state = state+rep
    return state

#checks if a position is free or not..
def isPositionFree(tup):
    if map[tup[0]][tup[1]] == " ":
        return True
    return False

#returns a random free position in the board..
def getFreePosition():
    return random.choice(getAllFreePos())

def getAllFreePos():
    freeList = []
    for i in range(0, 3):
        for j in range(0, 3):
            if isPositionFree((i, j)):
                freeList.append((i,j))
    return freeList    

#prints the board..
def print_board():
    for i in range(0,3):
        for j in range(0,3):
            print map[2-i][j],
            if j != 2:
                print "|",
        print ""

def convergence():
    #TODO
    if maxTrainGames > maxLimit:
        return True
    return False

def resetGame():
    print "Game Played:", maxTrainGames
    player1Moves = []
    player2Moves = []
    winner = 0
    for i in range(0, 3):
        for j in range(0, 3):
            map[i][j] = " "


def play(playerChar):
    global player1Moves
    global player2Moves

    freeList = getAllFreePos()
    choices = {}
    maxPos = freeList[0]
    maxValue = -10000000
    isMystery = False
    mispos = ()
    for pos in freeList:
        choices[pos] = getValue(map, playerChar, pos)
        if choices[pos] == 0.5:
            isMystery = True
            mispos = pos
            break
        if choices[pos] > maxValue:
            maxValue = choices[pos]
            maxPos = pos

    #two strategies with equal probability for picking the next move..
    if not isMystery:            
        pick = random.randint(1, 3)
        if pick == 2 or pick == 1:
            pos = maxPos
        else:
            pos = random.choice(freeList)
    else:
        pos = mispos
    #pos = random.choice(freeList)
    #print pos

    currValue = getValue(map, playerChar, pos)
    map[pos[0]][pos[1]] = playerChar
    
    #update the Q value..
    maxValue = -10000000
    for pos2 in freeList:
        if pos!=pos2:
            val = getValue(map, getOpponentChar(playerChar), pos2)
            if val > maxValue:
                maxValue = val

    map[pos[0]][pos[1]] = " "
    tup = (getStateFromBoard(map, playerChar), pos)
    map[pos[0]][pos[1]] = playerChar    
    
    if playerChar == "X":
        player1Moves.append(tup)
    else:
        player2Moves.append(tup)
    
#checks whether the game is done or not..

def check_done():
    global winner
    wonSymbol = ""
    for i in range(0,3):
        #check row wise..
        if map[i][0] == map[i][1] == map[i][2] != " ":
            wonSymbol = map[i][0]
            break
        
        #check every column..
        if map[0][i] == map[1][i] == map[2][i] != " ":
            wonSymbol = map[0][i]
            break

    #check diagonals..
    if wonSymbol == "":
        if map[0][0] == map[1][1] == map[2][2] != " ":
            wonSymbol = map[0][0]      
        elif map[0][2] == map[1][1] == map[2][0] != " ":
            wonSymbol = map[0][2]
    
    if wonSymbol != "":
        print wonSymbol, "won!!!"
        if wonSymbol == "X":
            winner = 1
        else:
            winner = -1
        print_board()
        return True

    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        print "Draw"
        print_board()
        return True
        
    return False

def decrementScore(state, pos):
    val = value[state][pos]
    if val!= 1 or val != 0:
        value[state][pos] = val - val*alpha

def updateScore(state, pos):
    val = value[state][pos]
    if val!= 1 or val != 0:
        value[state][pos] = val + (1-val)*alpha

random.seed()
while not convergence():
    i=0
    while not check_done():
        if i%2 == 0:
            play(player1Char)
        else:
            play(player2Char)
        i = i+1
    
    #reset all scores for the game..
    for tup in player1Moves:
        if winner == -1:
            decrementScore(tup[0], tup[1])
        elif winner == 1:
            updateScore(tup[0], tup[1])    
    
    for tup in player2Moves:
        if winner == 1:
            decrementScore(tup[0], tup[1])
        elif winner == -1:
            updateScore(tup[0], tup[1])    
    
    resetGame()
    maxTrainGames = maxTrainGames + 1

with open('policy.pickle', 'wb') as handle:
  pickle.dump(value, handle)

f = open("policy.txt", "w")
for state in value:
    for pos in value[state]:
            #print pos
            f.write(state+":"+str(pos[0])+":"+str(pos[1])+":"+str(value[state][pos])+"\n")
            #f.write(state+":"+str(pos[0])+":"+str(pos[1])+":")
f.close()
