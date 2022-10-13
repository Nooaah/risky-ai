from gameEngine import GameRisky

# Army Attributes
ACTION= 1
FORCE=  2

# ------------------------------------------------------------------------ #
#                   T E S T   R I S K Y   G A M E
# ------------------------------------------------------------------------ #

def verbose(aString):
  pass

# Test move action ...
def test_risky_init():
    game= GameRisky(1)
    assert game.map == "board-4"
    assert game.numberOfPlayers == 1
    game.initialize()
    assert game.playerHand(1).dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 0 : 2 5 15
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

# Test move action ...
def test_risky_action():
    game= GameRisky(1)
    game.initialize()
    assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 0 : 2 5 15
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

    print( game.board.dump() )
    assert not game.applyPlayerAction(1, "move 1 3 6")
    print( game.board.dump() )
    assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 6
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 0 : 2 5 15
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 1 : 3 1 9
  - Army 1 2 0 0 : A 0 6
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

    assert not game.applyPlayerAction(1, "move 1 2 6")
    print( game.board.dump() )
    assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 0 : 1 5 3
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : A 0 6
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 1 : 3 1 9
  - Army 1 2 0 0 : A 0 6
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

    assert game.applyPlayerAction(1, "sleep")
    print( game.board.dump() )
    assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 0 : 1 5 3
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : A 1 6
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 1 : 3 1 9
  - Army 1 2 0 0 : A 1 6
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

    assert not game.applyPlayerAction(1, "move 2 3 3")
    print( game.board.dump() )
    assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 0 : 1 5 3
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : A 1 3
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 1 : 3 1 9
  - Army 1 2 0 0 : A 0 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

# Test end ...
def test_risky_end():
  game= GameRisky(2, "board-4")
  assert game.map == "board-4"
  assert game.numberOfPlayers == 2
  game.initialize()
  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
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

  assert game.playerArmies() == [0, 12, 12]
  assert game.playerScore( 1 ) == 0
  assert game.playerScore( 2 ) == 0

  game.appendArmy( 1, 4, 6 )

  print(game.board.dump())

  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 12
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 1 : 4 9 9
  - Army 1 2 0 0 : A 0 6
- Edge-4 1 2 0 0 : 4 1 2"""

  assert not game.isEnded()

  assert game.playerArmies() == [0, 18, 12]
  assert game.playerScore( 1 ) == 1
  assert game.playerScore( 2 ) == -6

  for i in range( game.duration ) :
    game.tic()

  assert game.isEnded()

  game.board.cell(2).children().pop()
  
  # Test winners...
  assert game.activePlayers() == [1]
  assert game.playerArmies() == [0, 18, 0]
  assert game.playerScore( 1 ) == 1
  assert game.playerScore( 2 ) == -18
  assert game.isEnded()

# Test fight ...
samples= 10000
def test_risky_fight1(): # Failled attack
  game= GameRisky(2, "board-4")
  assert game.map == "board-4"
  assert game.numberOfPlayers == 2
  game.initialize()

  # Test winners...
  assert not game.isEnded()

  # get possible defences results for `samples` fight samples
  defences= [0 for i in range(13)]
  game.verbose= verbose
  for i in range(samples):
    game.board.cell(2).child(1).setAttribute(FORCE, 12)
    game.board.cell(1).child(1).setAttribute(FORCE, 12)
    assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
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
    assert not game.applyPlayerAction(2, "move 2 1 4")
    assert game.board.cell(2).dump() == """Cell-2 1 2 0 1 : 2 5 15
- Army 1 2 0 0 : B 1 8"""

    defences[ game.board.cell(1).child(1).attribute(FORCE) ] += 1

  # Compare percentages: 
  print( [ (obs*100)/samples for obs in defences ] )
  for obs, ref in zip( defences, [ 0, 0, 0, 0, 0, 0, 0, 0, 6, 25, 37, 25, 6 ] ) :
    assert (obs*100)//samples in [ref-2, ref-1, ref, ref+1, ref+2]

  # Test winners...
  assert not game.isEnded()

# Test fight ...
def test_risky_fight2(): # Successive attack
  game= GameRisky(2, "board-4")
  assert game.map == "board-4"
  assert game.numberOfPlayers == 2
  game.initialize()

  # Test winners...
  assert not game.isEnded()

  # get possible defences results for `samples` fight samples on
  attack= [0 for i in range(15)]
  game.verbose= verbose
  for i in range(samples):
    game.initialize()
    game.board.cell(1).child(1).setAttribute(FORCE, 15)
    game.board.cell(2).child(1).setAttribute(FORCE, 8)
    assert not game.applyPlayerAction(1, "move 1 2 14")
    assert game.board.cell(1).dump() == """Cell-1 1 2 0 1 : 1 5 3
- Army 1 2 0 0 : A 1 1"""

    if  game.board.cell(2).children() and game.board.cell(2).child(1).status() == 'A' :
      attack[ game.board.cell(2).child(1).attribute(FORCE) ] += 1
    else :
      attack[0] += 1

  # Compare percentages: 
  print( [ (obs*100)/samples for obs in attack ] )
  for obs, ref in zip( attack, [ 0, 0, 0, 0, 0, 2, 6, 17, 27, 25, 15, 6, 1, 0, 0 ] ) :
    assert (obs*100)//samples in [ref-2, ref-1, ref, ref+1, ref+2]

  # Test winners...
  assert game.isEnded()

# Test end ...
def test_risky_grow():
  game= GameRisky(2, "board-4")
  assert game.map == "board-4"
  assert game.numberOfPlayers == 2
  game.initialize()
  print( game.board.dump() )
  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
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

  game.actionGrow(1, 1)

  assert game.board.cell(1).dump() == """Cell-1 1 2 0 1 : 1 5 3
- Army 1 2 0 0 : A 0 16"""

  game.applyPlayerAction(1, "grow 1")

  assert game.board.cell(1).dump() == """Cell-1 1 2 0 1 : 1 5 3
- Army 1 2 0 0 : A 0 16"""

  game.applyPlayerAction(1, "sleep")
  game.applyPlayerAction(1, "move 1 3 6")
  game.applyPlayerAction(1, "grow 1")

  assert game.board.cell(1).dump() == """Cell-1 1 2 0 1 : 1 5 3
- Army 1 2 0 0 : A 0 15"""

def test_risky_sleep2():
  game= GameRisky(2, "board-4")
  assert game.map == "board-4"
  assert game.numberOfPlayers == 2
  game.initialize()
  print( game.board.dump() )
  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
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

  game.applyPlayerAction(1, "sleep")
  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 2 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 12
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

  game.applyPlayerAction(1, "sleep")
  game.applyPlayerAction(1, "sleep")
  game.applyPlayerAction(1, "sleep")
  game.applyPlayerAction(1, "sleep")
  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 2 12
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 12
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 0 : 3 1 9
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

def test_risky_growNmove():
  game= GameRisky(2, "board-4")
  assert game.map == "board-4"
  assert game.numberOfPlayers == 2
  game.initialize()
  print( game.board.dump() )
  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
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

  game.applyPlayerAction(1, "move 1 3 1")
  game.applyPlayerAction(1, "grow 1")
  game.applyPlayerAction(1, "sleep")
  game.applyPlayerAction(1, "grow 3")
  game.applyPlayerAction(1, "move 1 3 1")

  assert game.board.dump() == """Board 1 2 0 8 : board-4 1 4
- Cell-1 1 2 0 1 : 1 5 3
  - Army 1 2 0 0 : A 1 15
- Edge-1 1 3 0 0 : 1 2 3 4
- Cell-2 1 2 0 1 : 2 5 15
  - Army 1 2 0 0 : B 1 12
- Edge-2 1 3 0 0 : 2 1 3 4
- Cell-3 1 2 0 1 : 3 1 9
  - Army 1 2 0 0 : A 0 4
- Edge-3 1 2 0 0 : 3 1 2
- Cell-4 1 2 0 0 : 4 9 9
- Edge-4 1 2 0 0 : 4 1 2"""

if __name__ == "__main__" :
  pass #test_risky_end()