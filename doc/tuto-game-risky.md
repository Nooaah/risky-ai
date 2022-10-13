# Risky, an HackaGames Game

- Return to the [Table of Content](toc.md)

**Risky** is a strategic turn-based game where two armies (or more) fights for a territory.


## Try the game:

The `local` script starts the game with an interactive interface in a shell playing against a `firstAI`.

```sh
python3 hackagames/gameRisky/local
```

The world is composed by interconnected nodes forming a tabletop as, for instance:

```
       .' '.
      |     |
       '. .3
      /     \
 .' '.       .' '.
|     |-----|     |
 '. .1       '. .2 
      \     /
       .' '.
      |     |
       '. .4
```

The 2 players are referenced as a player _A_ and player _B_ ; starting respectively in positions 1 and 2.
When an army is on a node, the information is presented as below:

```
 .'A'.    # Player ID
|1- 12|   # army action and force 
 '. .1    # node ID
```

Each army has 2 main attributes:

- its action counter (the number of action it can perform - max 2)
- its force (the size of the army - max 24)

At its turn the player can make several actions (in the limite of action counters):

- Moving: `move X Y FORCE` to move `FORCE` units from cell `X` to cell `Y`
- Growing: `grow X` to grow the army on nodes `X`. The increase of the army is depending on the initial army size and the connections to occupied friend nodes.
- Sleeping: `sleep` to increase the action counter by one for all the armies.

To notice that a moving action that will move an army toward an adversarial node trigger a fight.
Iteratively, each force point of the attack and the defense has a chance to deal one damage.
Defenses have an increased chance than attack.
However if the attack is greater than the defense than each extra point count double.
The fight is running until one of the army is destroyed.

For instance, with a `move 1 2 10` with a defense of `8` on the node `2`, the fight will start by considering an attack force of `12` ($10+10-8$) times 1 chance over 2 against a defense of `8` times 2 chances over 3.
The exact amount of damages at the end of the fight remains uncertain.


## Let an AI play:

As for [421](tuto-game-421.md) game, we consider that you organize your repository to develop your AI aside of hackagames.
Your repository contains at least :

- **hackagames** : a clone of hackagames repository, as it is, with no modification.
- **draftAI** : a directory regrouping your AIs.
- **testRisky.py** : a script to launch a configuration of risky with one of your AI.

Then **draftAI** will contain at least one AI script as, for instance **myRiskyAI.py**.\
Potentially, **draftAI** and **testRisky.py** are shared in your own repository.

Considering this architecture, a first **myRiskyAI.py** look like: 

```python
#!env python3
"""
HackaGame player interface 
"""
import sys, os, random

sys.path.insert(1, __file__.split('draftAI')[0] + "/hackagames")
import hackapy as hg
import gameRisky.gameEngine as game

def main():
    player= myPlayer()
    player.takeASeat()

class myPlayer(hg.AbsPlayer) :
    
    # Player interface :
    def wakeUp(self, iPlayer, numberOfPlayers, gameConf):
        print( f'---\nwake-up player-{iPlayer} ({numberOfPlayers} players)')
        self.playerId= chr( ord("A")+iPlayer-1 )
        self.game= game.GameRisky()
        self.game.update(gameConf)
        self.viewer= game.ViewerTerminal( self.game )

    def perceive(self, gameState):
        self.game.update( gameState )
        self.viewer.print( self.playerId )
    
    def decide(self):
        actions= self.game.searchActions( self.playerId )
        print( f"Actions: { ', '.join( [ str(a) for a in actions ] ) }" )
        action= random.choice( actions )
        if action[0] == 'move':
            action[3]= random.randint(1, action[3])
        action= ' '.join( [ str(x) for x in action ] )
        print( "Do: "+ action )
        return action
    
    def sleep(self, result):
        print( f'---\ngame end\nresult: {result}')

# script
if __name__ == '__main__' :
    main()
```

You can notice that the `wakeUp` and `perceive` methods load and maintain a copy of the Risky game engine in an instance attribute `game`.
The `decide` method uses the game engine to get a destription of all possible actions before to choose one of them at random.

On this basis, the `testRisky.py` is an adapted copy of the `gameRisky/local` script:

```python
#!env python3
"""
HackaGame - Game - TicTacToe 
"""

from HackaGames.gameRisky.gameEngine import GameRisky
from HackaGames.game421.firstAI import PlayerRandom as Player1
from draftAI.myRiskyAI import myPlayer as player2

def main():
    game= GameRisky( 2, "board-10" )
    player1= Player1()
    player2= Player2()
    game.local( [player1, player1], 1 )

# script
if __name__ == '__main__' :
    main()
```

## Customaize your AI: 

To customize your AI you can use the game engine copy (cf. [risky.py](../gameRisky/gameEngine/risky.py))

Somme of the available methods:

```python
def update( self, board ): # Update the board from the perception.

def searchActions(self, playerId): # List all the current possible actions from the configuration of the armies

def cellIds(self): # return the list of cell identifiers

def edgesFrom(self, iCell): # return the list of connected cell identifiers from the iCell cell.
     
def armyOn(self, iCell) : # return an army as a Pod object, if an army is on the iCell cell (and False otherwise).

def playerLetter(self, iPlayer): # return the player letter (A or B) of the ith player (1 or 2)
```

An army is a Pod object where the owner is recorded in the status and the 2 attributes is for action counter and force :

```python
army= self.game.armyOn(1) # The army on the cell 1
owner= army.status()
action= army.attribute(1)
force= army.attribute(2)
```

And that it... 




