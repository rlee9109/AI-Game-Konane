'''
GameState object class. GameState object is used to maintain internal representation of the game board.
'''

class GameState:
    
    ''' 
    Constructor
    '''
    def __init__(self, prevGameState = None):
        # If no previous game board is provided, then create a new board
        if (prevGameState is None):
            self.board = [  ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'], \
                            ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'], \
                            ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'], \
                            ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'], \
                            ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'], \
                            ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'], \
                            ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'], \
                            ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']]
        
        # If a previous game board is provided, create a copy of the board
        else:
            self.board = prevGameState.getBoard()


    '''
    Accessor which returns 2D array of board rather than the memory location of the board
    '''        
    def getBoard(self):
        arrayBoard = []
        for row in range(8):
            tempRow = []
            for col in range(8):
                tempRow.append(self.board[row][col])
            arrayBoard.append(tempRow)
        return arrayBoard


    '''
    This function finds and returns all possible actions for the current player.
    Accepts the current and opponent player colors.
    Returns a 3D list of tuples including coordinate of start and end location(s).
    '''
    def getLegalActions(self, curColor, opponentColor):
        legalActions = []
        for row in range(8):
            for col in range(8):

                # Identifies where there are empty spaces
                if self.board[row][col] == '.':

                    # Check if there is a move into the empty space from above
                    if (row > 1):
                        if (self.board[row-1][col] == opponentColor and self.board[row-2][col] == curColor):
                            if (row < 6):
                                if (self.board[row+1][col] == opponentColor and self.board[row+2][col] == '.'):
                                    if (row < 4):
                                        if (self.board[row+3][col] == opponentColor and self.board[row+4][col] == '.'):
                                            # action with 3 jumps
                                            action = [[row-2, col], [row, col], [row+2, col], [row+4, col]]
                                            legalActions.append(action)
                                    # action with 2 jumps
                                    action = [[row-2, col], [row, col], [row+2, col]]
                                    legalActions.append(action)
                            # action with 1 jump
                            action = [[row-2, col], [row, col]]
                            legalActions.append(action)

                    # Check if there is a move into the empty space from below
                    if (row < 6):
                        if (self.board[row+1][col] == opponentColor and self.board[row+2][col] == curColor):
                            if (row > 1):
                                if (self.board[row-1][col] == opponentColor and self.board[row-2][col] == '.'):
                                    if (row > 3):
                                        if (self.board[row-3][col] == opponentColor and self.board[row-4][col] == '.'):
                                            action = [[row+2, col], [row, col], [row-2, col], [row-4, col]]
                                            legalActions.append(action)
                                    action = [[row+2, col], [row, col], [row-2, col]]
                                    legalActions.append(action)
                            action = [[row+2, col], [row, col]]
                            legalActions.append(action)

                    # Check if there is a move into the empty space from left
                    if (col > 1):
                        if (self.board[row][col-1] == opponentColor and self.board[row][col-2] == curColor):
                            if (col < 6):
                                if (self.board[row][col+1] == opponentColor and self.board[row][col+2] == '.'):
                                    if (col < 4):
                                        if (self.board[row][col+3] == opponentColor and self.board[row][col+4] == '.'):
                                            action = [[row, col-2], [row, col], [row, col+2], [row, col+4]]
                                            legalActions.append(action)
                                    action = [[row, col-2], [row, col], [row, col+2]]
                                    legalActions.append(action)
                            action = [[row, col-2], [row, col]]
                            legalActions.append(action)

                    # Check if there is a move into the empty space from right
                    if (col < 6):
                        if (self.board[row][col+1] == opponentColor and self.board[row][col+2] == curColor):
                            if (col > 1):
                                if (self.board[row][col-1] == opponentColor and self.board[row][col-2] == '.'):
                                    if (col > 3):
                                        if (self.board[row][col-3] == opponentColor and self.board[row][col-4] == '.'):
                                            action = [[row, col+2], [row, col], [row, col-2], [row, col-4]]
                                            legalActions.append(action)
                                    action = [[row, col+2], [row, col], [row, col-2]]
                                    legalActions.append(action)
                            action = [[row, col+2], [row, col]]
                            legalActions.append(action)

        return legalActions


    '''
    This function applys an action to the gameboard
    Accepts action which should be a 2D list: atleast 2 coordinates of start location and end location(s)
    Returns the number of jumps, or None if action is not legal
    '''
    def applyAction(self, action, curColor, opponentColor):

        # starting moves only provide 1 coordinate, because just remove
        if (action[1] is None):
            yCoord = action[0][0]
            xCoord = action[0][1]
            self.board[yCoord][xCoord] = '.'
            return 0

        # non-starting moves have start coordinate and end coordinate(s)
        else:
            allLegalActions = self.getLegalActions(curColor, opponentColor)
            if (action in allLegalActions):
                numOfJumps = len(action) - 1
                for jump in range(len(action)-1):
                    # extract the indices from the action
                    yCoordStart = action[jump][0]
                    xCoordStart = action[jump][1]
                    yCoordEnd = action[jump+1][0]
                    xCoordEnd = action[jump+1][1]
                    yCoordMid = (int) ((yCoordStart + yCoordEnd) / 2)
                    xCoordMid = (int) ((xCoordStart + xCoordEnd) / 2)

                    # make changes to the board to reflect the given action
                    self.board[yCoordStart][xCoordStart] = '.'
                    self.board[yCoordEnd][xCoordEnd] = curColor
                    self.board[yCoordMid][xCoordMid] = '.'                
                return numOfJumps
            return None


    '''
    This function provides a string formated version of the gameboard that can be printed
    '''
    def getPrintBoard(self):
        stringBoard = '\n'
        stringBoard = stringBoard + '  1 2 3 4 5 6 7 8'
        for row in range(len(self.board)):
            stringBoard = stringBoard + '\n' + (str)(row+1) + ' '
            for piece in self.board[row]:
                stringBoard = stringBoard + piece + ' '
        stringBoard = stringBoard + "\n"
        return stringBoard
