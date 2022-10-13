#!env python3
"""
HackaGame player interface 
"""

# Local HackaGame:
from . import interprocess

class AbsPlayer() :

    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):
        pass

    def perceive(self, gameState):
        pass
    
    def decide(self):
        pass
    
    def sleep(self, result):
        pass

    # Player interface :
    def takeASeat(self, host='localhost', port=1400 ):
        client= interprocess.Client(self)
        return client.takeASeat( host, port )

class PlayerIHM(AbsPlayer) :
    # PLayer interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):
        print( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        print( gameConf )

    def perceive(self, gameState):
        print( f'---\ngame state\n' + str(gameState) )
    
    def decide(self):
        action = input('Enter your action: ')
        return action
    
    def sleep(self, result):
        print( f'---\ngame end\nresult: {result}')
