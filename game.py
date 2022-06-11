'''
Game object class. Game object actually runs an instance of the game and maintains all of the
details, logic, algorithms, players, etc.
'''

from gameState import GameState
import random
import math

class Game:

    '''
    Constructor
    '''
    def __init__(self, playerColor, botColor, algo, boundDepth):
        self.playerColor = playerColor
        self.botColor = botColor 
        self.algo = algo
        self.boundDepth = boundDepth
        #self.staticEvaluationCount = 0


    '''
    This function parses commandline input and handles input errors. 
    Accepts string input. Returns an action as a 2D array.
    '''
    def parseMoveInput(self, moveInput):
        allMoves = moveInput.split(' ')
        action = []
        if (len(allMoves) > 1):
            try:
                for move in allMoves:
                    coordinate = [int(move[1]), int(move[3])]
                    action.append(coordinate)
                return(action)
            except:
                print('\nERROR: Invalid input type/format')
                return None
        else:
            print('\nERROR: Invalid number of coordinates')
            return None

    
    '''
    This function prints move information and board representation to commandline.
    Accepts player, action, and gameboard info.
    '''
    def printMove(self, curColor, action, game):
        if (curColor == "X"):
            printMoveStatement = "\nDark moves "
        else:
            printMoveStatement = "\nLight moves " 
        for coordinate in action:
            printMoveStatement = printMoveStatement + "<" + str(coordinate[0]+1) + ',' + str(coordinate[1]+1) + "> to "
        print(printMoveStatement[:len(printMoveStatement)-3])
        print(game.getPrintBoard())
        return None


    '''
    This function is the simplest AI algorithm.
    Returns a randomly selected move from all of the possible moves.
    '''
    def selectRandom(self, allLegalActions):
        return allLegalActions[random.randrange(len(allLegalActions))]


    '''
    This function begins the MiniMax AI algorithm. It calls upon recurMiniMax for recursion.
    Accepts current gameboard possible moves. Returns the best move based on the MiniMax algorithm.
    '''
    def selectMiniMax(self, gameState, allLegalActions):
        cbv = -math.inf
        bestAction = None
        for action in allLegalActions:
            nextGameState = GameState(gameState)
            nextGameState.applyAction(action, self.botColor, self.playerColor)
            bv, prevAction = self.recurMiniMax(nextGameState, 1, self.playerColor, self.botColor, False, action)
            if (bv > cbv):
                cbv = bv
                bestAction = action
        return bestAction


    '''
    This is the recursive function for MiniMax algorithm.
    Accepts details about recursive iteration. Returns the evaluated best value and best move of iteration.
    '''
    def recurMiniMax(self, curGameState, curDepth, curColor, opponentColor, isMax, prevAction):
        # Base cases to end the recursion
        if (curDepth == self.boundDepth):
            return self.evaluation(curGameState, prevAction), prevAction
        allLegalActions = curGameState.getLegalActions(curColor, opponentColor)
        if (len(allLegalActions) == 0):
            return self.evaluation(curGameState, prevAction), prevAction

        # If MAX state, looks for the action that maximizes the cbv
        if (isMax == True):
            cbv = -math.inf
            bestAction = None
            for action in allLegalActions:
                nextGameState = GameState(curGameState)
                nextGameState.applyAction(action, curColor, opponentColor)
                bv, prevAction = self.recurMiniMax(nextGameState, curDepth+1, opponentColor, curColor, False, action)
                if (bv > cbv):
                    cbv = bv
                    bestAction = action
            return cbv, bestAction

        # If MIN state, looks for the action that minimizes the cbv
        else:
            cbv = math.inf
            bestAction = None
            for action in allLegalActions:
                nextGameState = GameState(curGameState)
                nextGameState.applyAction(action, curColor, opponentColor)
                bv, prevAction = self.recurMiniMax(nextGameState, curDepth+1, opponentColor, curColor, True, action)
                if (bv < cbv):
                    cbv = bv
                    bestAction = action
            return cbv, bestAction


    '''
    This function begins the MiniMax AI algorithm using alpha beta prunning. It calls upon recurMiniMaxAB for recursion.
    Accepts current gameboard possible moves. Returns the best move based on algorithm.
    '''
    def selectMiniMaxAB(self, gameState, allLegalActions, alpha, beta):
        bestAction = None
        for action in allLegalActions:
            nextGameState = GameState(gameState)
            nextGameState.applyAction(action, self.botColor, self.playerColor)
            bv, prevAction = self.recurMiniMaxAB(nextGameState, 1, self.playerColor, self.botColor, False, action, alpha, beta)
            if (bv > alpha):
                alpha = bv
                bestAction = action
            if (alpha >= beta):
                return bestAction
        return bestAction


    '''
    This is the recursive function for MiniMax algorithm using alpha beta prunning.
    Accepts details about recursive iteration. Returns the evaluated best value and best move of iteration.
    '''
    def recurMiniMaxAB(self, curGameState, curDepth, curColor, opponentColor, isMax, prevAction, alpha, beta):
        # Base cases to end the recursion
        if (curDepth == self.boundDepth):
            return self.evaluation(curGameState, prevAction), prevAction
        allLegalActions = curGameState.getLegalActions(curColor, opponentColor)
        if (len(allLegalActions) == 0):
            return self.evaluation(curGameState, prevAction), prevAction

        # If MAX state, looks for the action that maximizes the alpha
        if (isMax == True):
            bestAction = None
            for action in allLegalActions:
                nextGameState = GameState(curGameState)
                nextGameState.applyAction(action, curColor, opponentColor)
                bv, prevAction = self.recurMiniMaxAB(nextGameState, curDepth+1, opponentColor, curColor, False, action, alpha, beta)
                if (bv > alpha):
                    alpha = bv
                    bestAction = action
                if (alpha >= beta):
                    return beta, bestAction
            return alpha, bestAction
        
        # If MAX state, looks for the action that minimizes the beta
        else:
            bestAction = None
            for action in allLegalActions:
                nextGameState = GameState(curGameState)
                nextGameState.applyAction(action, curColor, opponentColor)
                bv, prevAction = self.recurMiniMaxAB(nextGameState, curDepth+1, opponentColor, curColor, True, action, alpha, beta)
                if (bv < beta):
                    beta = bv
                    bestAction = action
                if (beta <= alpha):
                    return alpha, bestAction
            return beta, bestAction


    '''
    This function evaluates how good an action is using static evaluation fuction.
    Accepts gameboard, action, and player info. Returns integer score for action.
    '''
    def evaluation(self, curGameState, prevAction):
        score = 0
        #self.staticEvaluationCount = self.staticEvaluationCount + 1
        #print("static eval HERE: ", self.staticEvaluationCount)

        # Adds value to moves that are made up more than 1 jump
        jumps = len(prevAction)
        score = score + (jumps-2)*2

        # Adds value to moves that have the potential for more options next time
        allLegalCurActions = curGameState.getLegalActions(self.botColor, self.playerColor)
        score = score + len(allLegalCurActions)    

        allLegalOpponentActions = curGameState.getLegalActions(self.playerColor, self.botColor)
        # Adds value to the move that causes opponent to have no further moves
        if (len(allLegalOpponentActions) == 0):
            score = math.inf
        # Subtracts value from the move that causes opponent to have moves with more than 1 jump
        else:
            for action in allLegalOpponentActions:
                if (len(action) > 2):
                    score = score - (len(action) - 2)*2

        # Devalues the moves that are in the corners
        if (prevAction[0][0] == 0 and prevAction[0][1] == 0) or (prevAction[0][0] == 7 and prevAction[0][1] == 7) or (prevAction[0][0] == 0 and prevAction[0][1] == 7) or (prevAction[0][0] == 7 and prevAction[0][1] == 0):
            score = 1   

        return score


    '''
    This function executes the main game play.
    '''
    def run(self):

        allPotentialMoves = 0
        allMadeMoves = 0

        gameBoard = GameState()
        print("\nStarting Board:", gameBoard.getPrintBoard())

        # Starting move
        startActionDark = [[3, 3], None]
        gameBoard.applyAction(startActionDark, 'X', 'O')
        startActionLight = [[3, 4], None]
        gameBoard.applyAction(startActionLight, 'O', 'X')
        print("\nDark removes <4,4> \nLight removes <4,5>", gameBoard.getPrintBoard())

        # If human player is light, then the computer is dark and must go first.
        if (self.playerColor == 'O'):
            allLegalBotActions = gameBoard.getLegalActions(self.playerColor, self.botColor)
            print("bot actions: ", allLegalBotActions, len(allLegalBotActions))
            firstBotMove = [[5,3], [3,3]]
            gameBoard.applyAction(firstBotMove, 'X', 'O')
            self.printMove(self.botColor, firstBotMove, gameBoard)
            allPotentialMoves = allPotentialMoves + len(allLegalBotActions)
            allMadeMoves = allMadeMoves + 1

        winner = None
        while (winner == None):

            # Human Player Turn
            allLegalPlayerActions = gameBoard.getLegalActions(self.playerColor, self.botColor)
            print("player actions: ", allLegalPlayerActions, len(allLegalPlayerActions))
            if (len(allLegalPlayerActions) == 0):
                winner = self.botColor
                continue


            
            actionInput = input('\nFor the piece you would like to move, enter the current coordinate position and what position(s) you would like to move it to, as separated by spaces (e.g. "<6,4> <4,4>" or "<6,4> <4,4> <2,4>"): ')
            action = self.parseMoveInput(actionInput)
            if (action == None):
                continue

            # Convert action coordinates to indices
            for coordinate in range(len(action)):
                action[coordinate][0] = action[coordinate][0] - 1
                action[coordinate][1] = action[coordinate][1] - 1
            
            
            #action = self.selectRandom(allLegalPlayerActions)

            actionResult = gameBoard.applyAction(action, self.playerColor, self.botColor)
            if (actionResult == None):
                print("\nERROR: Selected move was not legal, please try different coordinates.")
                continue
            self.printMove(self.playerColor, action, gameBoard)
            allPotentialMoves = allPotentialMoves + len(allLegalPlayerActions)
            allMadeMoves = allMadeMoves + 1


            # Bot Player Turn
            allLegalBotActions = gameBoard.getLegalActions(self.botColor, self.playerColor)
            print("bot actions: ", allLegalBotActions, len(allLegalBotActions))
            if (len(allLegalBotActions) == 0):
                winner = self.playerColor
                continue

            if (self.algo == 1):
                action = self.selectRandom(allLegalBotActions)
            elif (self.algo == 2):
                action = self.selectMiniMax(gameBoard, allLegalBotActions)
            else:
                action = self.selectMiniMaxAB(gameBoard, allLegalBotActions, -math.inf, math.inf)
            
            gameBoard.applyAction(action, self.botColor, self.playerColor)
            self.printMove(self.botColor, action, gameBoard)
            allPotentialMoves = allPotentialMoves + len(allLegalBotActions)
            allMadeMoves = allMadeMoves + 1

        # After game is complete (player runs out of moves), print final result
        if (winner == 'X'):
            print("\nDark piece player wins!\n")
        elif (winner == 'O'):
            print("\nLight piece player wins!\n")
        else:
            print("\nLight and Dark piece players tied!\n")
        
        allMadeMoves = allMadeMoves * 1.0
        print("Average branching factor: ", allPotentialMoves/allMadeMoves)

        #print ("Total Static Evaluations: ", self.staticEvaluationCount)