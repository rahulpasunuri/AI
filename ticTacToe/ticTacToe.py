import random
import sys

#returns the symbol used by the AI.
def getAIChar():
    if turn == "X":
        return "O"
    return "X"

#critical move is a either a step which makes the computer win...or prevents the human from winning..
def getCriticalMove(move):    
    #check in every row..
    for i in range(0,3):
        countEmpty = 0
        countMatch = 0
        colCount = 0
        emptyPos = ()
        for elem in map[i]:
            if elem == move:
                countMatch = countMatch+1
            elif elem == " ":
                countEmpty = countEmpty+1
                emptyPos = (i, colCount)
            colCount = colCount + 1 
            
        if countMatch == 2 and countEmpty == 1:
            return emptyPos
                  
    #check in every column..
    for i in range(0, 3):
        countMatch = 0
        countEmpty = 0
        rowCount = 0
        emptyPos = ()
        while rowCount <= 2:
            if map[rowCount][i] == move:
                countMatch = countMatch + 1
            elif map[rowCount][i] == " ":
                countEmpty = countEmpty + 1
                emptyPos = (rowCount, i)
            rowCount = rowCount + 1
        if countMatch == 2 and countEmpty == 1:
            return emptyPos
    
    
    #check the two diagonals..
    #first diagonal from top left to bottom right..
    countMatch = 0
    countEmpty = 0
    rowCount = 0
    emptyPos = ()
    for i in range(0, 3):        
        if map[i][i] == move:
            countMatch = countMatch + 1;
        elif map[i][i] == " ":
            countEmpty = countEmpty + 1;
            emptyPos = (i,i)
    
    if countMatch == 2 and countEmpty == 1:
        return emptyPos
    
    #check the other diagonal:
    countMatch = 0
    countEmpty = 0
    rowCount = 0
    emptyPos = ()
    for i in range(0, 3):        
        if map[i][2-i] == move:
            countMatch = countMatch + 1;
        elif map[i][2-i] == " ":
            countEmpty = countEmpty + 1;
            emptyPos = (i,2-i)
    
    if countMatch == 2 and countEmpty == 1:
        return emptyPos    
    
    return ()
    
#return the number of x's and o's as a tuple
def getBoardCount():
    xCount = 0
    oCount = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if map[i][j] == "X":
                xCount = xCount+1
            elif map[i][j] == "O":
                oCount = oCount+1
    return (xCount, oCount)

center = (1, 1)
edges = [(0, 1), (1, 2), (1, 0), (2,1)]
corners = [(0, 0), (0, 2), (2, 0), (2,2)]

#checks if a position is free or not..
def isPositionFree(tup):
    if map[tup[0]][tup[1]] == " ":
        return True
    return False

#returns a diagonal position which is free..
def getFreeCornerPosition():
    for corner in corners:
        if isPositionFree(corner):
            return corner

#returns a edge position which is free..
def getEdgeCornerPosition():
    for edge in edges:
        if isPositionFree(edge):
            return edge

#returns a random free position in the board..
def getFreePosition():
    freeList = []
    for i in range(0, 3):
        for j in range(0, 3):
            if isPositionFree((i, j)):
                freeList.append((i,j))
    print "Free List is "
    print "Free List is ", random.choice(freeList)
    return random.choice(freeList)

#generates the next move by the computer..
def generateNextMove():
    print getAIChar()+"'s turn"
    print
 
    xCount, oCount = getBoardCount()
    if xCount + oCount == 0:
        #initial choice being made by the computer..
        initialChoice = random.randrange(0,2)
        if initialChoice == 0:
            map[1][1] = getAIChar()
        elif initialChoice == 1:
            map[0][0] = getAIChar()
    elif xCount + oCount == 1:
        #second choice being made by the computer..
        if isPositionFree((1, 1)):
            map[1][1] = getAIChar()
        else:
            map[0][0] = getAIChar()
    elif xCount + oCount == 2:
        #third choice being made by the computer..
        if map[1][1] == getAIChar():
            isDecisionMade = False
            for edge in edges:
                if not isPositionFree(edge):
                    #one of the edge position was filled by the human, in his 2nd turn..
                    map[edge[1]][edge[2]] = getAIChar()
                    isDecisionMade = True
                    break
            if not isDecisionMade:
                #this means that one of the corner position was marked by the human..
                pos = getFreeCornerPosition()
                map[pos[0]][pos[1]] = getAIChar()
                    
        elif isPositionFree((1, 1)):
            i, j = getFreeCornerPosition()
            map[i][j] = getAIChar()
        else:
            map[1][1] = getAIChar()
    else:
        #first check if there is move for winning...
        criticalMove = getCriticalMove(getAIChar())
        if criticalMove == ():
            #check for a move not to loose..
            criticalMove = getCriticalMove(turn)
            
        if criticalMove != ():
            #us the critical move, if there is a critical move..
            map[criticalMove[0]][criticalMove[1]] = getAIChar()
        else:
            #if there is no critical move...then just find an empty position, and use it..
            i,j =  getFreePosition()
            map[i][j] = getAIChar()

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
        

