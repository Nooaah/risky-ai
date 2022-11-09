#!env python3
"""
HackaGame player interface 
"""
import sys, os, random, math
import numpy as np

sys.path.insert(1, __file__.split('gameRisky')[0])

import hackapy as hg
import gameRisky.gameEngine as game
from time import time as clock
from .MCTS2 import MCTS

import json

def main():
	player = QPlayer()
	player.takeASeat()


class QPlayer(hg.AbsPlayer):

	def __init__(self, explorationRatio=0.1, discountFactor=0.99, learningRate=0.1 ):
		super().__init__()
		self.epsilon= explorationRatio
		self.gamma= discountFactor
		self.alpha= learningRate
		self.episode = 0
		self.qvalues = self.loadQTable()

	### Helper Functions

	def score(self):
		return self.game.playerScore(self.game.playerNum( self.playerId ))

	def state_to_string(self):
		states= ['0-0-0' for c in self.game.cellIds() ]
		for i in range(len(states)) :
			army = self.game.armyOn(i+1)
			if army :
				states[i]= f'{army.status()}-{army.attribute(2)}-{army.attribute(1)}'
		return '|'.join(states)
		
	def updateQ( self, aStateT0, anAction, aStateT1, aReward ) : 
		oldValue= self.qvalues[aStateT0][anAction]
		futureGains= self.qvalues[aStateT1][ self.bestAction(aStateT1) ]
		self.qvalues[aStateT0][anAction]= (1 - self.alpha) * oldValue + self.alpha * ( aReward + self.gamma * futureGains )

	def bestAction( self, aState ) : 
		option= random.choice( list(self.qvalues[aState].keys()) )
		for a in self.qvalues[aState] :
			if self.qvalues[aState][a] > self.qvalues[aState][option] :
				option= a 
		return option

	def loadQTable(self):
		f = open('teamBlue/qtable.json', 'r')
		values = json.load(f)
		f.close()
		return values
		

	def dumpQTable(self):
		jsonString = json.dumps(self.qvalues)
		jsonFile = open("teamBlue/qtable.json", "w")
		jsonFile.write(jsonString)
		jsonFile.close()



	### Game Functions

	def wakeUp(self, iPlayer, numberOfPlayers, gameConf):

		#print(self.episode)

		self.iPlayer = iPlayer
		self.playerId = chr(ord("A") + iPlayer - 1)
		self.game = game.GameRisky()
		self.game.update(gameConf)
		self.viewer = game.ViewerTerminal(self.game)

		self.lastState = self.state_to_string()
		self.lastAction = 'sleep'
		self.lastScore = 0

	def perceive(self, gameState):
		self.game.update(gameState)

		#Define a reward for last move
		newScore = self.score() 
		reward = newScore - self.lastScore 
		self.lastScore = newScore

		#Convert the game state to string
		newstate = self.state_to_string()

		if newstate not in self.qvalues.keys() :
			self.qvalues[newstate]= { 'sleep' : 0.0 }
		#print(self.qvalues.keys())

		if self.lastAction not in self.qvalues[self.lastState].keys() :
			self.qvalues[self.lastState][self.lastAction] = 0.0
		#print(self.qvalues)

		self.updateQ( self.lastState, self.lastAction, newstate, reward)

		self.lastState = newstate

	def decide(self):
		if self.episode < 100 or random.random() < self.epsilon :
			self.lastAction = MCTS(self.game, self.iPlayer).best_action(20)
		else :
			self.lastAction= self.bestAction( self.state_to_string() )
		print( f'Turn: { self.game.counter }, action: { self.lastAction }')
		return self.lastAction

	def sleep(self, result):
		self.dumpQTable()
		self.episode +=1
		#print(f'---\ngame end\nresult: {result}')

# script
if __name__ == '__main__':
	main()
