#!env python3
"""
HackaGame player interface 
"""
import sys, random

sys.path.insert(1, __file__.split('gameRisky')[0])
import hackapy as hg
import gameEngine as game
import json


def main():
  player = QPlayer()
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
    self.state = ""

  def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
    self.state = ""
    self.iPlayer = iPlayer
    self.playerId = chr(ord("A") + iPlayer - 1)
    self.game = game.GameRisky()
    self.game.update(gameConf)
    self.viewer = game.ViewerTerminal(self.game)

  def perceive(self, gameState):
    self.game.update(gameState)
    print(gameState)
    self.state = hash(gameState)
    if self.qvalue == None:
      self.qvalue = {self.state: {}}
    self.viewer.print(self.playerId)

  def decide(self):
    actions = self.game.searchActions(self.playerId)
    action = self.train(actions)
    if self.state not in self.qvalue.keys():
      self.qvalue[self.state] = {}
    if self.qvalue[self.state] == {}:
      self.qvalue[self.state][action] = self.game.playerScore(self.iPlayer)
    if action not in self.qvalue[self.state].keys():
      self.qvalue[self.state][action] = self.game.playerScore(self.iPlayer)
    else:
      self.qvalue[
        self.state][action] = (self.qvalue[self.state][action] +
                               self.game.playerScore(self.iPlayer)) / 2
    return action

  def sleep(self, result):
    self.learnFromTraining()
    print(f'---\ngame end\nresult: {result}')

  def jsonValue(self):
    fileObject = open("file.json", "r")
    jsonContent = fileObject.read()
    if jsonContent != "":
      obj_python = json.loads(jsonContent)
      fileObject.close()
      if (obj_python):
        return obj_python

  def learnFromTraining(self):
    jsonString = json.dumps(self.qvalue)
    jsonFile = open("file.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


#learning fonction

  def train(self, actions):
    action = random.choice(actions)
    if action[0] == 'move':
      action[3] = random.randint(1, action[3])
    actionString = ' '.join([str(x) for x in action])
    return actionString


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
