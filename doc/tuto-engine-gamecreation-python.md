# Game Creation in Python 

The ideas here is to present step by step the game creation in python with `hackapy`.

Reminder, `hackapy` is the HackaGames python librairy helping for the game and players to communicate together.

## Directory structure 

In your `HackaGame` directory create a subdirectory `gameXyz` where `Xyz` identify your new game (`gameHelo` for instance).
This new subdirectory (your working directory) will also include another subdirectory `gameEngine` regrouping the source code making your game working.

Directory squeletom: 

```
HackaGames                 # Master directory
- ...
- hackapy                  # Python version of HackaGames lib.
- ...
- gameHelo                # your game folder
  - gameEngine              # sourcecode of the game
- ...
```

Then we start with 3 files:

- `README.md` : a Markdown readme first file presenting the game and how to handdle it.
- `gameEngine/__init__.py` : a classical python files marking the entrance of your gameEngine package.
- `start` : a start script, lauching the game server.

## Game Engine

At minima `gameEngine` python package derivate `hackapy.Game` class in the  `__init__.py` file. 
First, initialize python file and import the `hackapy` package.

```python 
#!env python3
"""
HackaGame - Game - Hello 
"""
import sys

sys.path.insert( 1, __file__.split('gameXyz')[0] )
import hackapy as hg
```

Then implement a simple Game as an abstract sequential game for instance (a game where each player play at turn).
The Game class must implement some methode: `initialize`, `playerHand`, `applyPlayerAction`, `isEnded` and `playerScore`.

```python
class GameHello( hg.AbsSequentialGame ) :
    
    # Game interface :
    def initialize(self):
        # Initialize a new game (returning the game setting as a Gamel, a game ellement shared with player wake-up)
        self.counter= 0
        return hg.Pod( 'hello' )
        
    def playerHand( self, iPlayer ):
        # Return the game elements in the player vision (an AbsGamel)
        return hg.Pod( 'hi', attributs=[ self.counter ] )  

    def applyPlayerAction( self, iPlayer, action ):
        # Apply the action choosen by the player iPlayer. return a boolean at True if the player terminate its actions for the current turn.
        print( f"Player-{iPlayer} say < {action} >" )
        return True
    s
    def tic( self ):
        # called function at turn end, after all player played its actions. 
        self.counter= min( self.counter+1, 3 )

    def isEnded( self ):
        # must return True when the game end, and False the rest of the time.
        return self.counter == 3

    def playerScore( self, iPlayer ):
        # return the player score for the current game (usefull at game ending)
        return 1
```

Here the Hello game simply echo the player action in a terminal $3$ times (method `applyPlayerAction`).
A counter initialized in `initialize` method, count $3$ game turn (i.e. after each player play at-turn) in `tic` method. 
Then the `isEnded` method will return true.
The method `playerHand` simplely informs the player about the counter status.
Finaly, there is no winner and all player will end with a result at $1$ (method `playerScore`).

## Lets play 

The `start` script will permit to lauch the game server.
It only instancate a Game with a determined number of players then call the `AbsGame` `start` method.

```python
#!env python3
"""
HackaGame - Game - Hello 
"""
from gameEngine import GameHello

game= GameHello( numerOfPlayers= 1 )
game.start()
```

That it. 

You can set your script executable (`chmod +x ./gameXyz/start`) and play with your new game (in tree different terminals): `./gameXyz/start`, `./play` and `./play`


## Going futher: Command Interpreter:

```python
import sys, os
from gameEngine import GameHello

# Local HackaGame:
sys.path.insert( 1, __file__.split('gameXyz')[0] )
import hackapy as hg

# Commands:
class StartCmd( hg.StartCmd ) :
    def __init__(self) :
        super().__init__(
            "Hello",
            ["classic"],
            parameters= { 
                "n": ["number of games", 2],
                "p": ["server port", 1400]
            }
        )

cmd= StartCmd()
print( cmd )

if cmd.mode in ["classic"] :
    game= GameHello( cmd.mode )
else :
    print("/!\ Unreconized mode")
    exit()

game.start( (int)(cmd.parameter("n")), (int)(cmd.parameter("p")) )
```
