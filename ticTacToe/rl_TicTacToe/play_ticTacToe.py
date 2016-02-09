import random
import sys
import pickle

with open('policy.pickle', 'rb') as handle:
  value = pickle.load(handle)

player1Char = "X"
player2Char = "Y"

def getOpponentChar(playerChar):
    if playerChar == "X":
        return "O"
    return "X"
        

#returns the symbol used by the AI.
def getAIChar():
    if turn == "X":
        return "O"
    return "X"

#checks if a position is free or not..
def isPositionFree(tup):
    if map[tup[0]][tup[1]] == " ":
        return True
    return False

def getAllFreePos():
    freeList = []
    for i in range(0, 3):
        for j in range(0, 3):
            if isPositionFree((i, j)):
                freeList.append((i,j))
    return freeList    

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
         else:
                value[state][pos] = 0.5

    board[pos[0]][pos[1]] = " "
    return value[state][pos]
        
#generates the next move by the computer..
def generateNextMove():
    #TODO
    random.seed()
    freeList = getAllFreePos()
    maxValue = -10000000
    maxPos = random.choice(freeList)
    for pos in freeList:
        val = getValue(map, getAIChar(), pos)
        print pos,": ",val
        if val > maxValue:
            maxValue = val
            maxPos = pos   
    map[maxPos[0]][maxPos[1]] = getAIChar()  
             
#prints the board..
def print_board():
    for i in range(0,3):
        for j in range(0,3):
            print map[2-i][j],
            if j != 2:
                print "|",
        print ""

#checks whether the game is done or not..
def check_done():
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
        print_board()
        return True

    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        print "Draw"
        return True
        
    return False

map = [[" "," "," "],
       [" "," "," "],
       [" "," "," "]]
done = False

turn = ""
while turn != "X" and turn != "O":
    turn = raw_input("Press 'X' for playing first, and 'O' for playing second: ")
    print "You Chose : ", turn

if turn == "O":
    generateNextMove()

while done != True:
    print_board()
    print turn, "'s turn"
    print
    
    moved = False
    while moved != True:
        
        print "Please select position by typing in a number between 1 and 9, see below for which number that is which position..."
        print "7|8|9"
        print "4|5|6"
        print "1|2|3"
        print

        try:
            pos = input("Select: ")
            if pos <=9 and pos >=1:
                Y = pos/3
                X = pos%3
                if X != 0:
                    X -=1
                else:
                     X = 2
                     Y -=1
                    
                if map[Y][X] == " ":
                    map[Y][X] = turn
                    moved = True
                    done = check_done()
                    if not done:
                        generateNextMove()
                        done = check_done()
            
        except Exception as error:
            print "You need to add a numeric value", error
        

