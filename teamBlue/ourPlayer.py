#!env python3
"""
HackaGame player interface 
"""
import sys, random

sys.path.insert(1, __file__.split('teamBlue')[0])
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
        self.viewer= game.ViewerTerminal( self.game )
        self.actions = []
        self.nb_actions = 0

    def perceive(self, gameState):
        self.game.update( gameState )
        if self.actions == []:
            if self.game.counter %2 == 1:
                idcell = self.game.cellIds()
                for i in idcell:
                    adjacent = self.game.edgesFrom(i)
                    if self.game.armyOn(i) != False:
                        if self.game.armyOn(i).status() == self.playerId:
                            nb_army = self.game.armyOn(i).attributes()[1] // 4
                            for j in adjacent:
                                if j != 9:
                                    army = self.game.armyOn(j)
                                    if army == False:
                                        if nb_army != 0:
                                            self.actions.append(['move', i, j, nb_army])
                for i in idcell:
                    if self.game.armyOn(i) != False:
                        if self.game.armyOn(i).status() == self.playerId:
                            for k in range (self.game.armyOn(i).attributes()[0]):
                                self.actions.append(['grow', i])
            self.actions.append(['sleep'])

        #print(self.actions)

        #print( self.playerId )
        #self.viewer.print( self.playerId )
    
    def decide(self):
        actions= self.game.searchActions( self.playerId )
        action = self.actions[self.nb_actions]
        action_str = ' '.join( [ str(x) for x in action ] )
        self.nb_actions += 1
        if action[0] == 'sleep':
            self.nb_actions = 0
            self.actions = []
        return action_str
    
    """ def simulate(self, actions):
        game_copy = self.game.copy()
        for action in actions:
            if action[0] == 'move':
                #print(action)
                action[3]= random.randint(1, action[3])
            action= ' '.join( [ str(x) for x in action ] )

            print(action)

            game_copy.applyPlayerAction(2, action)
        print("ended") """

    
    def sleep(self, result):
        True
        #print( f'---\ngame end\nresult: {result}')

# script
if __name__ == '__main__' :
    main()
