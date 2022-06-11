'''
Use this file to drive the program. Make changes to runGame() function in order to customize AI bot player.
'''

from game import Game
from gameState import GameState

'''
This function is used to set up players colors, AI algorithm, and depth.
'''
def runGame():

    '''To select an AI algorithm, uncomment an assignment of the algo variable'''
    #algo = 1 # AI move selection is random
    #algo = 2 # AI move selection uses minimax + static function evaluation 
    algo = 3 # AI move selection uses minimax with alpha beta pruning + static function evaluation

    '''To select a depth of search for minimax algorithm, change the value of depth variable'''
    boundDepth = 6

    # Accepts input of 'X' or 'O' to select player color
    validPlayerSelection = False 
    while (validPlayerSelection == False):
        playerColorInput = input('\nWhich piece are you playing as? Type "X" to indicate dark and "O" to indicate light: ')
        if (playerColorInput != 'X' and playerColorInput != 'O'):
            playerColorInput = input('\nNot a valid player piece option. Type "X" to indicate dark and "O" to indicate light: ')
        else:
            validPlayerSelection = True

    # Creates game and begins game
    if (playerColorInput == 'X'):
        game = Game('X', 'O', algo, boundDepth)
        game.run()
    else:
        game = Game('O', 'X', algo, boundDepth)
        game.run()
    return game


'''
This function initiates the program.
''' 
if __name__ == '__main__':
    runGame()