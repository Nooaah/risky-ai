#!env python3
"""
HackaGame player interface
"""

import gameRisky.gameEngine as game
import hackapy as hg
import sys
import random
import math
import numpy as np
from time import time as clock

sys.path.insert(1, __file__.split('teamBlue')[0])

class MCTSNode():
	def __init__(self, state, player, move=None, parent=None):
		self.n = 0
		self.w = 0
		self.move = move
		self.parent = parent
		self.player = player
		self.state = state
		self.children = []

	### HELPER FUNCTIONS

	def isExpanded(self):
		return len(self.children) > 0 

	def moves(self):
		moves = self.state.searchActions(self.state.playerLetter(self.player))
		movesList = []
		
		for action in moves:
			#print(action)
			if action[0] == 'move':
				#print(action[3])
				for i in range(int(action[3])):
					action_to_add = [action[0], action[1], action[2], f'{i+1}']
					movesList.append(action_to_add)
			else:
				movesList.append(action)
		return movesList

	def uct(self):
		if self.n == 0:
			return (float("inf"))
		return ((float(self.w)/self.n) + math.sqrt(2)*math.sqrt((np.log(self.parent.n))/self.n))

	def best_child(self):
		
		for child in self.children: 
			child.uct_score = child.uct()

		choices = [l for l in self.children if l.uct_score == max(node.uct_score for node in self.children)]
		#print(f'{self.children}, {choices}')
		return random.choice(choices)

class MCTS:

	def __init__(self, state, playerToPlay):
		self.root = MCTSNode(state, player=playerToPlay)

	def randomAction( self, aListOfactions ):
		action= random.choice( aListOfactions )
		if action[0] == 'move':
			#print(action[3])
			action[3]= random.randint(1, action[3])
		action= ' '.join( [ str(x) for x in action ] )
		return action
	
	def traverse(self, node):
		current_node = node
		while not current_node.state.isEnded():

			if not current_node.isExpanded():
				return self.expand(current_node)

			else:
				current_node = current_node.best_child()
		return current_node

	def expand(self, node):

		for action in node.moves():
			action= ' '.join( [ str(x) for x in action ] )
			#print(action)
			play = node.player
			next_state = node.state.copy()
			endTurn = next_state.applyPlayerAction( node.player, action )

			if endTurn:
				play+= 1
				if play > next_state.numberOfPlayers :
					next_state.tic()
					play= 1

			child_node = MCTSNode(state=next_state, player=play, move=action ,parent=node)
			node.children.append(child_node)
		#print(node.children)
		return random.choice(node.children)

	def rollout(self, node):
		simulator= node.state.copy()
		iPlayer= node.player
		#print(node.move)
		# action= ' '.join( [ str(x) for x in node.move ] )
		# endTurn= simulator.applyPlayerAction( iPlayer, action )
		# tanque le jeu n'est pas terminé:
		endTurn = False
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
		return (simulator.playerScore( iPlayer ) , iPlayer)

	def backpropagate(self, node, result):
		if node.player == result[1]:
			node.w += 1
		node.n +=1

		#print(f'parent : {node.parent}')

		if node.parent is not None:
			self.backpropagate(node.parent, result)

	def best_action(self, nbsims):
		num_rollouts = 0
		for _ in range(nbsims):
			v = self.traverse(self.root)
			#print(v.move)
			result = self.rollout(v)
			self.backpropagate(v, result)
			num_rollouts += 1
		if len(self.root.children):
			best_child = self.root.best_child()
			return best_child.move
		else: 
			return 'sleep'
