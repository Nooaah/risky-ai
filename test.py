#!env python3
"""
HackaGame - Game - TicTacToe 
"""
import time

from gameRisky.gameEngine import GameRisky
from gameRisky.firstAI import PlayerRandom as playerTest
from teamBlue.ourPlayer import Player as PlayerBlue


def playerId(aPlayer):
  return str(type(aPlayer).__module__).split('.')[0]


def main():
  players = [
    PlayerBlue(),
  ]
  nboGames = 10
  resultFile = open('result.csv', 'w')
  refTime = time.time()
  for player in players:
    game = GameRisky(
      2, "board-10")  # the number of players and the tabletop to load.
    result = game.local(
      [player, playerTest()],
      nboGames)  # A list of players and the number of games to plays.
    t = time.time()
    resultFile.write(
      f"{playerId(player)}, playerTest, {round( (t-refTime)/nboGames, 4 )}, {sum(result[0])/nboGames}, {sum(result[1])/nboGames}\n"
    )
    refTime = t
  resultFile.close()


# script
if __name__ == '__main__':
  main()
