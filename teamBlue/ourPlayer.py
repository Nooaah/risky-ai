#!env python3
"""
HackaGame player interface
"""
import gameRisky.gameEngine as game
import hackapy as hg
import sys
import random

sys.path.insert(1, __file__.split('teamBlue')[0])


def main():
    player = Player()
    player.takeASeat()


class Player(hg.AbsPlayer):

    # Player interface :
    def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
        #print( f'---\nwake-up player-{iPlayer} ({numberOfPlayers} players)')
        self.playerId = chr(ord("A")+iPlayer-1)
        self.game = game.GameRisky()
        self.game.update(gameConf)
        self.viewer = game.ViewerTerminal(self.game)
        self.actions = []
        self.nb_actions = 0

    def perceive(self, gameState):
        self.game.update(gameState)
        if self.actions == []:
            if self.game.counter % 2 == 1:
                idcell = self.game.cellIds()
                for i in idcell:
                    adjacent = self.game.edgesFrom(i)
                    if self.game.armyOn(i):
                        if self.game.armyOn(i).status() == self.playerId:
                            if i == 9 and self.game.armyOn(i).attributes()[1] >= 24:
                                for j in adjacent:
                                    nb_cases_vides = 0
                                    if not self.game.armyOn(j):
                                        if nb_cases_vides == 0:
                                            self.actions.append(['move', i, j, 23])
                                            nb_cases_vides += 1
                            nb_army = self.game.armyOn(i).attributes()[1] // 4
                            start_point = 0
                            ally_army = 0
                            ennemy_army = 0
                            ennemies = []
                            nb_empty = 0
                            for j in adjacent:
                                if j != 9:
                                    army = self.game.armyOn(j)
                                    if not army:
                                        nb_empty += 1
                                        if nb_army != 0:
                                            self.actions.append(['move', i, j, nb_army])
                                    elif army.status() == self.playerId:
                                        if i == 1 or i == 2:
                                            start_point += 1
                                        else:
                                            ally_army += 1
                                    elif army.status() != self.playerId:
                                        ennemy_army += 1
                                        ennemies.append(j)
                                elif start_point == 3 and self.game.armyOn(i).attributes()[1] >= 24:
                                    self.actions.append(['move', i, j, 23])
                            if self.game.armyOn(i).attributes()[1] >= 24 and nb_empty == 0:
                                if ennemy_army == 1:
                                    if self.game.armyOn(ennemies[0]).attributes()[1] < 18:
                                        self.actions.append(['move', i, ennemies[0], 23])
                                elif ennemy_army > 1:
                                    nb_ennemy_army = []
                                    for j in ennemies:
                                        nb_ennemy_army.append(self.game.armyOn(j).attributes()[1])
                                    nb_less_ennemy_army = min(nb_ennemy_army)
                                    for j in ennemies:
                                        if self.game.armyOn(j).attributes()[1] == nb_less_ennemy_army:
                                            self.actions.append(['move', i, j, 23])
                for i in idcell:
                    if self.game.armyOn(i):
                        if self.game.armyOn(i).status() == self.playerId:
                            for k in range(self.game.armyOn(i).attributes()[0]):
                                self.actions.append(['grow', i])
            self.actions.append(['sleep'])
        # self.viewer.print( self.playerId )

    def decide(self):
        actions = self.game.searchActions(self.playerId)
        action = self.actions[self.nb_actions]
        action_str = ' '.join([str(x) for x in action])
        self.nb_actions += 1
        if action[0] == 'sleep':
            self.nb_actions = 0
            self.actions = []
        return action_str

    def sleep(self, result):
        True
        # print( f'---\ngame end\nresult: {result}')


# script
if __name__ == '__main__':
    main()
