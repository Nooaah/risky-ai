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

import json

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

	def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
		self.state = ""
		self.iPlayer = iPlayer
		self.playerId = chr(ord("A") + iPlayer - 1)
		self.game = game.GameRisky()
		self.game.update(gameConf)
		self.viewer = game.ViewerTerminal(self.game)

	def perceive(self, gameState):
		self.game.update(gameState)
		#print(gameState)
		if self.qvalue == None:
			self.qvalue = {self.state: {}}
		idcell = self.game.cellIds()
		state = []
		for i in idcell:
			res = self.game.armyOn(i)
			if res == False:
				state.append([])
			else:
				state.append([res.status(), res.attributes()[0], res.attributes()[1]])
		state.append(self.playerId)
		self.state = str(state)\
			.replace('[','_').\
				replace(']','').\
					replace(' ','').\
						replace('\'','').\
							replace(',','')
		#self.viewer.print(self.playerId)

	def decide(self):
		action = self.train()
		if self.state not in self.qvalue.keys():
			self.qvalue[self.state] = {}
		if self.qvalue[self.state] == {}:
			self.qvalue[self.state][action[0]] = action[1]
		if action not in self.qvalue[self.state].keys():
			self.qvalue[self.state][action[0]] = action[1]
		else:
			self.qvalue[
				self.state][action[0]] = (self.qvalue[self.state][action[0]] +
															 action[1]) / 2
		return action[0]

	def sleep(self, result):
		self.learnFromTraining()
		#print(f'---\ngame end\nresult: {result}')

	def jsonValue(self):
		fileObject = open("teamBlue/file.json", "r")
		jsonContent = fileObject.read()
		if jsonContent != "":
			obj_python = json.loads(jsonContent)
			fileObject.close()
			if (obj_python):
				return obj_python

	def learnFromTraining(self):
		jsonString = json.dumps(self.qvalue)
		jsonFile = open("teamBlue/file.json", "w")
		jsonFile.write(jsonString)
		jsonFile.close()


#learning fonction

	def train(self):
		if self.iPlayer == 1 :
			playerLeft = 2
		else:
			playerLeft = 1
		
		test = MCTSState(self.game, self.iPlayer, None, "self", playerLeft, self.game.counter)
		nodeTest = MCTSNode(test, None)
		action = self.best_action(nodeTest, 5)
		print(action[0])
		return action


class PlayerRandom(hg.AbsPlayer):

	# Player interface :
	def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
		#print(f'---\nwake-up player-{iPlayer} ({numberOfPlayers} players)')
		self.playerId = chr(ord("A") + iPlayer - 1)
		self.game = game.GameRisky()
		self.game.update(gameConf)
		self.viewer = game.ViewerTerminal(self.game)

	def perceive(self, gameState):
		self.game.update(gameState)
		#self.viewer.print(self.playerId)

	def decide(self):
		actions = self.game.searchActions(self.playerId)
		#print(f"Actions: { ', '.join( [ str(a) for a in actions ] ) }")
		action = random.choice(actions)
		if action[0] == 'move':
			action[3] = random.randint(1, action[3])
		action = ' '.join([str(x) for x in action])
		#print("Do: " + action)
		return action

	def sleep(self, result):
		True
		#print(f'---\ngame end\nresult: {result}')


# script
if __name__ == '__main__':
	main()
