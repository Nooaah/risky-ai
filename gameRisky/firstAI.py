#!env python3
"""
HackaGame player interface 
"""
import sys, os, random

sys.path.insert(1, __file__.split('gameRisky')[0])

import hackapy as hg
import gameEngine as game
import json
import functools


def main():
  player = PlayerRandom()
  player.takeASeat()


class QPlayer(hg.AbsPlayer):

  def __init__(self,
               explorationRatio=0.1,
               discountFactor=0.99,
               learningRate=0.1):
    self.qvalue = self.jsonValue()  # valeur du qlearning enregistré
    self.results = []  # résultat du jeu
    self.epsilon = 0.1  # the exploration ratio, 0.1 over 1 chance to take a random action.
    self.gamma = 0.99  # the discount factors, interest of immediate reward regarding future gains
    self.alpha = 0.1  # the learning rate, speed that incoming experiences erase the oldest.
    self.actions = []
    self.currentAction = ""
    self.state = ""
    self.states = []
    self.turn = 0

  def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
    self.actions = []
    self.currentAction = ""
    self.state = ""
    self.states = []
    self.turn = 1
    self.iPlayer = iPlayer
    self.playerId = chr(ord("A") + iPlayer - 1)
    self.game = game.GameRisky()
    self.game.update(gameConf)
    self.viewer = game.ViewerTerminal(self.game)

  def perceive(self, gameState):
    self.game.update(gameState)
    self.viewer.print(self.playerId)

  def decide(self):
    actions = self.game.searchActions(self.playerId)
    if str(self.turn) not in self.qvalue.keys():
      self.qvalue[str(self.turn)] = {}
    action = self.train(actions)
    if "sleep" in action:
      self.qValuePath(self.qvalue, (str(self.turn),) + tuple(self.actions),
                                    self.game.playerScore(self.iPlayer))
      self.actions = []
      self.turn += 1
    return action

  def sleep(self, result):
    self.learnFromTraining()
    print(f'---\ngame end\nresult: {result}')

  def jsonValue(self):
    fileObject = open("dico.json", "r")
    jsonContent = fileObject.read()
    obj_python = json.loads(jsonContent)
    fileObject.close()
    if (obj_python):
      return obj_python

  def learnFromTraining(self):
    jsonString = json.dumps(self.qvalue)
    jsonFile = open("dico.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

#learning fonction

  def train(self, actions):
    action = random.choice(actions)
    if action[0] == 'move':
      action[3] = random.randint(1, action[3])
    actionString = ' '.join([str(x) for x in action])
    self.actions.append(actionString)
    if 'sleep' in actionString:
      self.qValuePath(self.qvalue, (str(self.turn),) + tuple(self.actions), 0)
    else:
      self.qValuePath(self.qvalue, (str(self.turn),) + tuple(self.actions), {})
    return actionString

  def get_nested_default(self,d, path):
    return functools.reduce(lambda d, k: d.setdefault(k, {}), path, d)
    
  def qValuePath(self, d, path, value):
    print(path)
    self.get_nested_default(d, path[:-1])[path[-1]] = value


#play fonction

# def recursiveFonction(self, actions, valueTurn, results, path):
#   for act in actions:
#     if act != "sleep":
#       if act.contains("move"):
#         game = self.game.actionMove()
#         self.recursiveFonction(game.searchActions(self.playreId), valueTurn)
#       else:
#         game = self.game.actionGrow()
#     else:
#       return result


class PlayerRandom(hg.AbsPlayer):

  # Player interface :
  def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
    print(f'---\nwake-up player-{iPlayer} ({numberOfPlayers} players)')
    self.playerId = chr(ord("A") + iPlayer - 1)
    self.game = game.GameRisky()
    self.game.update(gameConf)
    self.viewer = game.ViewerTerminal(self.game)

  def perceive(self, gameState):
    self.game.update(gameState)
    self.viewer.print(self.playerId)

  def decide(self):
    actions = self.game.searchActions(self.playerId)
    print(f"Actions: { ', '.join( [ str(a) for a in actions ] ) }")
    action = random.choice(actions)
    if action[0] == 'move':
      action[3] = random.randint(1, action[3])
    action = ' '.join([str(x) for x in action])
    print("Do: " + action)
    return action

  def sleep(self, result):
    print(f'---\ngame end\nresult: {result}')


# script
if __name__ == '__main__':
  main()
