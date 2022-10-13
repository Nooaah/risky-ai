from gameEngine import GameRisky
import random

# Army Attributes
ACTION= 1
FORCE=  2

# ------------------------------------------------------------------------ #
#                   T E S T   R I S K Y   G A M E
# ------------------------------------------------------------------------ #

def verbose(aString):
  print(aString)

# Test move action ...
def test_risky_Fight01():
  game= GameRisky()
  assert game.map == "board-4"
  assert game.numberOfPlayers == 2
  game.initialize()
  assert game.playerHand(1).dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 12
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""
  random.seed(4)
  game.actionFight( 1, 1, 10, 2 )
  verbose( game.playerHand(1).dump() )
  assert game.playerHand(1).dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 4
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

def test_risky_fight02():
  game= GameRisky()
  game.initialize()
  random.seed(4)
  game.actionFight( 1, 1, 15, 2 )
  verbose( game.playerHand(1).dump() )
  assert game.playerHand(1).dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : A 0 4
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

def test_risky_grow():
  game= GameRisky()
  game.initialize()
  game.actionGrow( 1, 1 )
  army= game.armyOn(1)
  verbose( army.dump() )
  assert army.dump() == "Army 1 2 0 0 : A 0 16"
  game.actionGrow( 1, 1 )
  assert army.dump() == "Army 1 2 0 0 : A 0 16"
  army.setAttribute(ACTION, 2)
  assert army.dump() == "Army 1 2 0 0 : A 2 16"
  game.actionGrow( 1, 1 )
  assert army.dump() == "Army 1 2 0 0 : A 1 22"
  game.actionGrow( 1, 1 )
  assert army.dump() == "Army 1 2 0 0 : A 0 24"
  army.setAttribute(ACTION, 2)
  game.actionGrow( 1, 1 )
  assert army.dump() == "Army 1 2 0 0 : A 1 24"

def test_risky_wrongAction():
  game= GameRisky()
  game.initialize()
  assert game.wrongAction == [0, 0, 0]
  game.applyPlayerAction( 1, "move 1 2 10" )
  assert game.wrongAction == [0, 0, 0]
  game.initialize()
  game.applyPlayerAction( 1, "move 2 1 10" )
  assert game.wrongAction == [0, 1, 0]
  game.applyPlayerAction( 1, "move" )
  game.applyPlayerAction( 1, "grow 4" )
  game.applyPlayerAction( 2, "truc" )
  assert game.wrongAction == [0, 3, 1]


def test_risky_copy():
  game= GameRisky()
  game.initialize()
  game2= game.copy()
  assert game2.playerHand(1).dump() ==  game.playerHand(1).dump()
  game2.applyPlayerAction( 1, "move 1 3 10" )
  
  assert game.playerHand(1).dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 12
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

  print(game2.playerHand(1).dump())
  assert game2.playerHand(1).dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 2
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 12
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 1 : 3 1 9
  - Army 1 2 0 0 : A 0 10
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""