# 421, an HackaGames game

- Return to the [Table Of Content](toc.md)

**421** is simple dice games where players try to optimize it dice combination after a maximum of 2 roll dice steps.


## Try the game:

The `local` script starts the game with interactive interface in a shell.

```sh
python3 hackagames/game421/local
```

The **421** is a tree dice game the player can roll several times to get a combinaison.
The player can perform one and only one action at it turns, and the game stops automatically after 2 turns.

The actions consist in keeping or rolling each of the 3 dices. So there are 8 actions:

- `keep-keep-keep`,  `keep-keep-roll`,  `keep-roll-keep`,  `keep-roll-roll`, `roll-keep-keep`,  `roll-keep-roll`,  `roll-roll-keep` and `roll-roll-roll`

The goal is to optimize the combination of dices before the end of the 2 turns.
The best combination ever is **421** for **800** points.
But you can explore other combinations.


## Let an AI play:

The file `./game421/firstAI.py` propose a first random AI with the required structure to play **421**.

From the script `local`, modify the imported player to get the first AI:

aside to `hackagames` directory, create your own launcher:

```sh
cp hackagamtest es/game421/local test421.py
```

Then Modify the import instructions to get the gameEngine considering the position of `test421.py` in the file tree
and to get the firstAI

```python
from hackagames.game421.gameEngine import GameSolo as Game
from hackagames.game421.firstAI import PlayerRandom as Player
```

The final `test421.py` is :

```python
#!env python3
from HackaGames.game421.gameEngine import GameSolo as Game
from HackaGames.game421.firstAI import PlayerRandom as Player

def main():
  game= Game()
  player1= Player()
  game.local( [player1], 1 )

# script
if __name__ == '__main__' :
    main()
```

That it, you can execute your script: `python3 test421.py`


## client/server game:

**421** is a standard **HackaGames** game, and it is designed to work in a client-server architecture.
The server is the game, the clients are the players.
**421** can be played in a _solo_ or a _duo_ mode. 

First start the game server (from **HackaGames** repository) in default _solo_ mode :

```sh
python3 hackagames/game421/start
```

Then, in a new terminal start the basic **HackaGames** terminal player:

```sh
python3 hackagames/play
```

or a 421 AI like firstAI: 

```sh
python3 hackagames/game421/firstAI.py
```


## Your first AI:

In a directory dedicated to your work aside to `hackagames`, you start an AI from the proposed random player:

```bash
mkdir teamOfMine
cp hackagames/game421/firstAI.py teamOfMine/my421IA.py
```

`my421AI.py` script must import hackagames elements. For that you have to correct the directory path where python sck for packages (the `sys.path`) by returning in the root directory of `teamOfMine` and adding `hackagames` directory ie: 

```python
# Local HackaGame:
sys.path.insert( 1, __file__.split('teamOfMine')[0] + "/hackagames" )
import hackapy as hg
```

An **HackaGames** player is composed by 4 main methods: `wakeUp`, `perceive`, `decide` and `sleep`

In python: 

```python
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConfigurationMsg):
        self.scores= [ 0 for i in range(numberOfPlayers+1) ]
        self.id= playerId
        print( '> ' + '\n'. join([ str(line) for line in gameConfigurationMsg ]) )

    def perceive(self, gameStatusMsg):
        gameStatus= gameStatusMsg[0].split(' ')
        self.horizon= int(gameStatus[1])
        self.dices= [ int(gameStatus[3]), int(gameStatus[4]), int(gameStatus[5]) ]
        print( '> ' + '\n'. join([ str(line) for line in gameStatusMsg ]) )
        print( f'H: {self.horizon} DICES: {self.dices}' )

    def decide(self):
        action= random.choice( actions )
        return action
    
    def sleep(self, result):
      print( f'--- Results: {str(result)}' )
```



## Play Battle:
