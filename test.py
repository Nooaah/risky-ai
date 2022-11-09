#!env python3
"""
HackaGame - Game - TicTacToe 
"""
import time

from gameRisky.gameEngine import GameRisky
from teamBlue.QLearn import QPlayer as playerBlue
from gameRisky.firstAI import PlayerRandom as playerTest
from teamProf.bestRandomSim import Player as playerProf

def playerId(aPlayer):
  return str(type(aPlayer).__module__).split('.')[0]


def main():
  players = [
    playerBlue(),
  ]
  nboGames = 100
  resultFile = open('result.csv', 'w')
  refTime = time.time()
  for player in players:
    game = GameRisky(
      2, "board-10")  # the number of players and the tabletop to load.
    result = game.local(
      [player, playerTest()],
      nboGames)  # A list of players and the number of games to plays.
    print(result)
    t = time.time()
    resultFile.write(
      f"{playerId(player)}, playerTest, {round( (t-refTime)/nboGames, 4 )}, {sum(result[0])/nboGames}, {sum(result[1])/nboGames}\n"
    )
    refTime = t
  resultFile.close()


# script
if __name__ == '__main__':
  main()
