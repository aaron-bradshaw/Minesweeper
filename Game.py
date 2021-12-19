class Game:
    def __init__(self, gameSize, grid, mines, numFlags, gameEnd, winGame, loseGame, message):
        self.gameSize = gameSize
        self.grid = grid
        self.mines = mines
        self.numFlags = numFlags
        self.gameEnd = gameEnd
        self.winGame = winGame
        self.loseGame = loseGame
        self.message = message
