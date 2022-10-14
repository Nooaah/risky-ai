#!env python3
"""
HackaGame player interface 
"""
import sys, os

sys.path.insert( 1, __file__.split('gameRisky')[0] )
import hackapy as hg
import gameEngine as game

class RiskyPlayer(hg.AbsPlayer) :
    # Conscructor :
    def __init__(self, clear= False):
        self.clear= clear

    # Player interface :
    def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
        print( f'---\nwake-up player-{iPlayer} ({numberOfPlayers} players)')
        self.playerId= chr( ord("A")+iPlayer-1 )
        self.game= game.GameRisky()
        self.game.update(gameConf)
        self.viewer= game.ViewerTerminal( self.game )

    def perceive(self, gameState):
        if self.clear :
            os.system("clear")
        self.game.update( gameState )
        self.viewer.print(self.playerId)
    
    def decide(self):
        action = input('Enter your action: ')
        return action
    
    def sleep(self, result):
        print( f'---\ngame end\nresult: {result}')

    