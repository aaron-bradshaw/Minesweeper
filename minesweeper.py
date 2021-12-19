import os
from math import floor
from random import randrange
from Square import Square
from Game import Game

def playGame():
    generateBoard()

    while not(gameData.gameEnd) :
        clear()
        print(gameData.grid)
        print(gameData.message)
        collectInput()
    notValid = True
    while notValid:
        repeat = input("Play again? (Y/N): ").lower()
        if repeat == 'y':
            notValid = False
            playGame()
        elif repeat == 'n':
            notValid = False
        else:
            print("Invalid Input. Input \"Y\" for yes or \"N\" for no")

        
        

    


def generateBoard():
    global squares
    global gameData
    success = False
    while not(success):
        try:
            valid = False
            while not(valid):
                gameSize  =  int(input("Enter the size of the game (min 4, max 26): "))
                if gameSize > 26 or gameSize < 4:
                    clear()
                    print("Invalid Input, enter an integer from 4 to 26")
                else:
                    valid = True
                    success = True
        except ValueError:
            clear()
            print("Invalid Input, enter an integer from 4 to 26")

    
    
    gameData = Game(gameSize, '', [], 0, False, False, False, '')
    mineLocations = generateMines()
    squares = generateSquares(squareValues(mineLocations), squarePositions())
    gameData.mines = mineLocations
    gameData.grid = drawGrid()
    gameData.numFlags = len(mineLocations)
    

def generateMines():
    numSquares = gameData.gameSize**2
    numMines = floor(numSquares * 0.2)
    mineLocations = []
    for i in range(numMines):
        valid = False
        while not(valid):
            location = randrange(numSquares)
            if location not in mineLocations:
                valid = True
                mineLocations.append(location)
    return(mineLocations)

def squareValues(mineLocations):
    numSquares = gameData.gameSize ** 2
    squareValues = []
    for i in range(numSquares):
        value = 0
        if i in mineLocations:
            value = -1
            squareValues.append(value)
        else:
            neighbors = getNeighbors(i)
            for neighbor in neighbors:
                if neighbor in mineLocations:
                    value += 1
            squareValues.append(value)

    return(squareValues)

def squarePositions():
    positions = []
    tempPos = (gameData.gameSize * 4)
    for y in range(gameData.gameSize):
        for x in range(gameData.gameSize):
            tempPos += 4
            positions.append(tempPos)
        if y < 9:
            tempPos += (gameData.gameSize * 4)+6
        else:
            tempPos += (gameData.gameSize * 4)+7
    return(positions)



def generateSquares(squareValues, squarePositions):
    squares = []
    for i in range(len(squareValues)):
        squares.append(Square(i, squareValues[i], False, False, squarePositions[i]))
    
    return(squares)

def flagSquare(location):
    if gameData.numFlags > 0:
        if not(squares[location].isRevealed):
            gameData.numFlags -= 1
            squares[location].isFlagged = True
            pos = squares[location].position
            gameData.grid = gameData.grid[0:pos] + 'F' + gameData.grid[pos+1:]
            winGame()
        else:
            gameData.message = 'Cannot flag already revealed squares'
    else:
        gameData.message = 'You have no flags remaining'

def unFlagSquare(location):
    if squares[location].isFlagged:
        gameData.numFlags += 1
        squares[location].isFlagged = False
        pos = squares[location].position
        gameData.grid = gameData.grid[0:pos] + ' ' + gameData.grid[pos+1:]
    else:
        gameData.message = 'Square is not flagged'    

def revealSquare(location):
    pos = squares[location].position
    value = squares[location].value
    if squares[location].isFlagged:
        gameData.message = 'Flagged Square'
    elif value > 0:
        squares[location].isRevealed = True
        gameData.grid = gameData.grid[0:pos] + str(value) + gameData.grid[pos+1:]
        winGame()
    elif value == 0:
        squares[location].isRevealed = True
        gameData.grid = gameData.grid[0:pos] + str(value) + gameData.grid[pos+1:]
        adjacent = getNeighbors(location)
        for i in adjacent:
            if not(squares[i].isRevealed):
                revealSquare(i)
        winGame()
    elif value == -1:
        gameData.grid = gameData.grid[0:pos] + 'M' + gameData.grid[pos+1:]
        squares[location].isRevealed = True
        hitMine()
    
def hitMine():
    gameData.loseGame = True
    for mine in gameData.mines:
        if not(squares[mine].isRevealed):
            revealSquare(mine)
    endGame()

def winGame():
    flaggedCount = 0
    revealedCount = 0
    for mine in gameData.mines:
        if squares[mine].isFlagged == True:
            flaggedCount += 1
    for square in range(len(squares)):
        if squares[square].isRevealed:
            revealedCount += 1
    if flaggedCount == len(gameData.mines):
        gameData.winGame = True
        endGame()
    elif revealedCount == (len(squares) - len(gameData.mines)):
        gameData.winGame = True
        endGame()



def collectInput():
    print("Flags:("+str(gameData.numFlags)+"/"+str(len(gameData.mines))+")")
    action  = input("Choose a square: ")
    action = action.replace(' ', '').lower()
    if "instructions" in action:
        gameData.message = "To select a square input the column number followed by the row number. ex. a10\nTo flag a square input flag followed by the square selection. ex. flag a10\nTo unflag a square type unflag followed by the square selection. ex. unflag a10"
        return()
    try:
        if ord(action[-2]) > 60:
            row = ord(action[-1]) - 48
            col = ord(action[-2]) - 96
        else:
            row = ((ord(action[-2])-48) * 10) + (ord(action[-1])-48)
            col = ord(action[-3]) - 96
        pos = (((row-1)*gameData.gameSize)+col) - 1
        if 'unflag' in action:
            unFlagSquare(pos)
        elif 'flag' in action:
            
            flagSquare(pos)
        else:
            revealSquare(pos)
    except IndexError:
        gameData.message = "Invalid Input. type \"instructions\" for help"
    

def endGame():
    gameData.gameEnd = True
    clear()
    print(gameData.grid)
    if gameData.loseGame:
        print("You Lose")
    if gameData.winGame:
        print("You Win")



def drawGrid():
    n = 0
    output = ''
    for y in range((2*gameData.gameSize) + 1):
        for x in range(gameData.gameSize + 1):
            if y == 0:
                if x == 0:
                    output += "┌───"
                elif x < (gameData.gameSize):
                    output += "┬───"
                elif x == (gameData.gameSize):
                    output += "┐\n"
            elif (y % 2) != 0:
                if x < gameData.gameSize:
                    output += "│   "
                elif x == gameData.gameSize:
                    n += 1
                    if n < 10:
                        output += "│ "+str(n)+"\n"
                    else:
                        output += "│ "+str(floor(n/10))+str(n % 10)+"\n"
            elif y == (2*gameData.gameSize):
                if x == 0:
                    output += "└───"
                elif x < gameData.gameSize:
                    output += "┴───"
                elif x == gameData.gameSize:
                    output += "┘\n"
            elif (y % 2) == 0:
                if x == 0:
                    output += "├───"
                elif x < gameData.gameSize:
                    output += "┼───"
                elif x == gameData.gameSize:
                    output += "┤\n"
    output += "  A"
    for i in range(1,gameData.gameSize):
        output += "   "+chr(65+i)
    output += "\n"  
    return(output)


def getNeighbors(location):
    neighbors = []
    row = floor(location / gameData.gameSize)
    col = location % gameData.gameSize

    if row > 0:
        neighbors.append(location - gameData.gameSize) # adds up
        if col > 0:
            neighbors.append(location - (gameData.gameSize + 1)) # adds up left
        if col < (gameData.gameSize - 1):
            neighbors.append(location - (gameData.gameSize - 1)) # adds up right

    if row < (gameData.gameSize - 1):
        neighbors.append(location + gameData.gameSize) # adds down
        if col > 0:
            neighbors.append(location + (gameData.gameSize - 1)) # adds down left
        if col < (gameData.gameSize - 1):
            neighbors.append(location + (gameData.gameSize  + 1)) # adds down right

    if col > 0:
        neighbors.append(location - 1) # adds left
    if col < (gameData.gameSize - 1):
        neighbors.append(location + 1) #adds right
        
    return(neighbors)

def clear():
    os.system("cls")

playGame()