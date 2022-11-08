#!/usr/bin/env python3
"""
HackaGame player interface 
"""
import sys, random

sys.path.insert(1, __file__.split('teamBlue')[0])
import hackapy as hg
import gameRisky.gameEngine as game
import json


def main():
  player = Player()
  player.takeASeat()


class Player(hg.AbsPlayer):

  def __init__(self):
    self.qvalue = self.jsonValue()

  # Player interface :
  def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
    self.state = ""
    self.iPlayer = iPlayer
    self.playerId = chr(ord("A") + iPlayer - 1)
    self.game = game.GameRisky()
    self.game.update(gameConf)

  def perceive(self, gameState):
    self.game.update(gameState)
    self.state = hash(gameState)
    idcell = self.game.cellIds()
    state = []
    for i in idcell:
      res = self.game.armyOn(i)
      if res == False:
        state.append([])
      else:
        state.append([res.status(), res.attributes()[0], res.attributes()[1]])
    state.append(self.playerId)
    self.state = str(state)


  def decide(self):
    actions = self.game.searchActions(self.playerId)
    if self.state not in self.qvalue.keys():
      print("Not Dico")
      action = random.choice(actions)
      if action[0] == 'move':
        action[3] = random.randint(1, action[3])
      action = ' '.join([str(x) for x in action])
      return action
    else:
      print("GO to dico")
      listeActions = []
      valeurAction = []
      print(actions)
      for actionInfo in actions:
        if actionInfo[0] == 'move':
          for i in range (1, actionInfo[3] + 1):
            actionInfo[3] = i
            simpleAction = ' '.join([str(x) for x in actionInfo])
            if simpleAction in self.qvalue[self.state].keys():
              listeActions.append(simpleAction)
              valeurAction.append(self.qvalue[self.state][simpleAction])
        simpleAction = ' '.join([str(x) for x in actionInfo])
        print(actionInfo)
        print(self.qvalue[self.state].keys())
        print(simpleAction)
        if simpleAction in self.qvalue[self.state].keys():
          listeActions.append(simpleAction)
          valeurAction.append(self.qvalue[self.state][simpleAction])
          print(listeActions)
          print(valeurAction)
      index = valeurAction.index(max(valeurAction))
      return listeActions[index]

  def sleep(self, result):
    results = result

  def jsonValue(self):
    fileObject = open("teamBlue/file.json", "r")
    jsonContent = fileObject.read()
    obj_python = json.loads(jsonContent)
    fileObject.close()
    return obj_python


# script
if __name__ == '__main__':
  main()
