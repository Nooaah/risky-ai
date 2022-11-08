#!env python3
"""
HackaGame player interface
"""

import sys
import random
import math
import numpy as np
from time import time as clock

sys.path.insert(1, __file__.split('teamBlue')[0])
import gameRisky.gameEngine as game
import hackapy as hg


def main():
	player = Player()
	player.takeASeat()


class MCTSNode():
	def __init__(self, state, parent=None):
		self.n = 0
		self.w = 0
		self.state = state
		self.parent = parent
		
		self.terminal = self.state.isEnded()
		self.children = []

	def isExpanded(self):
		return len(self.children) == len(self.state.moves())

	def uct(self):
		
		if self.n == 0:
			return (float("inf"))
		return ((float(self.w)/self.n) + math.sqrt(2)*math.sqrt((np.log(self.parent.n))/self.n))

	def best_child(self, verbose=False):
		for child in self.children: 
			child.uct_score = child.uct()
			# if verbose:
			# 	print(f'n:{child.n} score: {child.uct_score} action:{child.state.action}')
		#print(max(node.uct_score for node in self.children))

		choices = [l for l in self.children if l.uct_score == max(node.uct_score for node in self.children)]
		return random.choice(choices)


class MCTSState():

	def __init__(self, state, player, move=None, playerToPlay="self", playerLeft=2, turn=0):
		self.players = {
			"self": (player, chr(ord("A")+player-1)),
			"opponant": (3-player, chr(ord("A")+3-player-1))
		}

		self.state = state
		self.action = move

		self.playerToPlay = self.players[playerToPlay]
		self.turn = turn
		self.players_left = playerLeft

	def result(self):
		if (self.state.playerScore(self.players["self"][0]) - self.state.playerScore(self.players["opponant"][0])) > 0:
			return 1
		else:
			return 0

	def isEnded(self):
		return self.turn >= 10

	def moves(self):
		moves = self.state.searchActions(self.playerToPlay[1])
		movesList = []
		

		for action in moves:
			#print(action)
			movesList.append(action)
			if action[0] == 'move':
				#print(action[3])
				for i in range(int(action[3])):
					action_to_add = [action[0], action[1], action[2], f'{i+1}']
					movesList.append(action_to_add)
		#print(movesList)
		return movesList

	def play(self, action):
		new_state = self.state.copy()
		action= ' '.join( [ str(x) for x in action ] )
		# print(action)
		turn_is_over = new_state.applyPlayerAction(self.playerToPlay[0], action)

		players_left = self.players_left
		turn = self.turn
		playerToPlay = "self"

		if turn_is_over:
			if self.playerToPlay is self.players["self"]:
				playerToPlay = "opponant"
			else:
				playerToPlay = "self"
			players_left = players_left - 1

		#print(f'Turn: {turn} - Player {self.playerToPlay[0]} - Action {action} - Turn Over {turn_is_over} - Left {players_left} ')

		if players_left <= 0:
			turn += 1
			players_left = 2

		return MCTSState(new_state, self.players["self"][0], action, playerToPlay, players_left, turn)


class Player(hg.AbsPlayer):

	# def simulate(self, state):
	# 	i = 0

	# 	while state.turn < 10:
	# 		actions = state.state.searchActions( state.playerToPlay[1] )
	# 		print( f"Actions: { ', '.join( [ str(a) for a in actions ] ) }" )
	# 		action= random.choice( actions )
	# 		if action[0] == 'move':
	# 			action[3]= random.randint(1, action[3])
	# 		action= ' '.join( [ str(x) for x in action ] )
	# 		#print(f'Action played: {action}')

	# 		state = state.play(action)
	# 		i +=1
	# 	print(i)

	def traverse(self, node):
		current_node = node
		while not current_node.terminal:

			if not current_node.isExpanded():
				return self.expand(current_node)

			else:
				current_node = current_node.best_child()
		return current_node

	def expand(self, node):

		for action in node.state.moves():
			next_state = node.state.play(action)
			child_node = MCTSNode(next_state, node)
			node.children.append(child_node)
			#print(node.children)
		return node

	def rollout_policy(self, state):
			current_state = state
			action = random.choice(current_state.moves())
			next_state = current_state.play(action)
			#print(f"Rollout Policy : Turn {next_state.turn}")
			#print(f"parent in rollout : {child_node.parent}")
			return next_state

	def rollout(self, state):
		while not state.isEnded():
			state = self.rollout_policy(state)
			#print(f"Rollout : Turn {state.turn}")
		return state

	def backpropagate(self, node, result):
		node.n += 1
		node.w += result
		#print(f'parent : {node.parent}')

		if node.parent is not None:
			self.backpropagate(node.parent, result)

	def best_action(self, node, time_budget):
		start_time = clock()
		num_rollouts = 0
		while clock() - start_time < time_budget:
			#print(i)
			v = self.traverse(node)
			#print(v)
			final_state = self.rollout(v.state)
			self.backpropagate(v, final_state.result())
			num_rollouts += 1
		best_child = node.best_child()
		#print(f'Number of experiments: {num_rollouts}')
		return (best_child.state.action, best_child.uct())

	#####

	# Player interface :
	def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
		#print( f'---\nwake-up player-{iPlayer} ({numberOfPlayers} players)')
		self.playerId= chr( ord("A")+iPlayer-1 )
		self.player = iPlayer
		self.game= game.GameRisky()
		self.game.update(gameConf)
		self.viewer= game.ViewerTerminal( self.game )

	def perceive(self, gameState):
		self.game.update( gameState )
		#self.viewer.print( self.playerId )
	
	def decide(self):
		# actions= self.game.searchActions( self.playerId )
		# print(actions)
		if self.player == 1 :
			playerLeft = 2
		else:
			playerLeft = 1
		test = MCTSState(self.game, self.player, None, "self", playerLeft, self.game.counter)
		nodeTest = MCTSNode(test, None)
		action = self.best_action(nodeTest, 0.5)

		#print(f'[Turn {self.game.counter}] AI Player - {action}')

		return action[0]
	
	def sleep(self, result):
		#print( f'---\ngame end\nresult: {result}')r
		return

# script
if __name__ == '__main__' :
	main()
