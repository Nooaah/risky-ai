#!env python3
"""
HackaGame player interface 
"""
import sys, random

import hackapy as hg
import gameRisky.gameEngine as game

def main():
    player= Player()
    player.takeASeat()

class Player(hg.AbsPlayer) :
    
    # Player interface :
    def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
        #print( f'---\nwake-up player-{iPlayer} ({numberOfPlayers} players)')
        self.playerId= chr( ord("A")+iPlayer-1 )
        self.game= game.GameRisky()
        self.game.update(gameConf)
        self.numberOfTestedAction= 8
        self.numberOfSimulation= 10

    def perceive(self, gameState):
        self.game.update( gameState )
    
    def decide(self):
        actions= self.game.searchActions( self.playerId )
        
        # Get the best action in X random actions with Y random simulation
        best= -100
        for i in range(self.numberOfTestedAction) :
            action= self.randomAction( actions )
            score= 0
            for i in range(self.numberOfSimulation) :
                score+= self.simulate(action)
            score/= self.numberOfSimulation
            if score > best :
                best= score
                selection= action
        return selection
    
    # Simulation:
    def randomAction( self, aListOfactions ):
        action= random.choice( aListOfactions )
        if action[0] == 'move':
            action[3]= random.randint(1, action[3])
        action= ' '.join( [ str(x) for x in action ] )
        return action

    def simulate(self, anAction):
        simulator= self.game.copy()
        iPlayer= simulator.playerNum( self.playerId )
        endTurn= simulator.applyPlayerAction( iPlayer, anAction )
        # tanque le jeu n'est pas terminé:
        while not simulator.isEnded() :
            # tanque c'est le tour du iPlayer:
            while not endTurn :
                actions= simulator.searchActions( simulator.playerLetter(iPlayer) )
                action= self.randomAction( actions )
                endTurn= simulator.applyPlayerAction( iPlayer, action )
            # switch player :
            iPlayer+= 1
            if iPlayer > simulator.numberOfPlayers :
                simulator.tic()
                iPlayer= 1
        return simulator.playerScore( simulator.playerNum( self.playerId ) )

# script
if __name__ == '__main__' :
    main()
