# Play with HackaGames on Replit

[Replit](https://replit.com) is a kind off web-base IDE that allows developers to share and collaborate on the code edition.

After creating an account, create a replit (a replit working repository) on python for instance and clone **HackaGames** project.

In the 'shell' box:

```
git clone https://GuillaumeLozenguez@bitbucket.org/imt-mobisyst/hackagames.git
```

**HackaGames** is only dependent on ZeroMQ library and tqdm to permit multi-processes to communicate together and process-bar.
In the shell:

```
pip install zmq tqdm
```

However, _replit_ will not allow us to work on _client-server_ mode, so only _./local_ scripts will be used on replit environment.

## Try a game:

It is possible to execute python script in the Shell with the commands `python`...

```
python  hackagames/game421/local
```

## Set up the main.py file:

From the `local` script of a game (`game421/local` for instance).

```python
#!env python3
"""
HackaGame - Game - 421 
"""
import sys, os

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

import gameEngine as g421
from hackapy.player import PlayerIHM as Player

def main():
    game= g421.GameSolo()
    game.local( [Player()], 1 )

# script
if __name__ == '__main__' :
    main()
```

Then configure correctly, the path  where to find the appropriate packages.
Concretely, change:

```python
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
```

to:

```python
sys.path.insert(1, os.path.join(sys.path[0], 'hackagames'))
sys.path.insert(1, os.path.join(sys.path[0], 'hackagames/game421'))
```

## A first IA in local mode.

Following the same idea, you can start from `game421/firstIA.py` script to generate a repllit compliante `main.py` script.

1. Set the appropriate `sys.path` references
2. start a local game rather than connect a server via `takeAseat`.
3. record locally les results to generate the graph and compute an average

In other terms, configure your `main.py` as follow: 

```python
#!env python3
"""
HackaGame - Game - 421 
"""
import sys, os
import matplotlib.pyplot as plt

sys.path.insert(1, os.path.join(sys.path[0], 'hackagames'))
sys.path.insert(1, os.path.join(sys.path[0], 'hackagames/game421'))

import gameEngine as g421
import random
from hackapy.player import PlayerIHM as Player
import hackapy as hg

def main():
  actions = []
  for a1 in ['keep', 'roll']:
    for a2 in ['keep', 'roll']:
      for a3 in ['keep', 'roll']:
        actions.append(a1 + '-' + a2 + '-' + a3)
  game = g421.GameSolo()
  player = PlayerRandom(actions)
  game.local([player], 100)
  print("# Average:")
  print(sum(player.results) / len(player.results))
  plotResults(player.results)


class PlayerRandom(hg.AbsPlayer):

  def __init__(self, actions):
    super().__init__()
    self.actions = actions
    self.results = []

  # Player interface :
  def wakeUp(self, playerId, numberOfPlayers, gameConf):
    print(f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
    print(gameConf)

  def perceive(self, gameState):
    elements = gameState.children()
    self.horizon = elements[0].attribute(1)
    self.dices = elements[1].attributes()
    if len(elements) == 3:  # ie in duo mode
      self.reference = elements[2].attribute(1)
      print(f'H: {self.horizon} DICES: {self.dices} REF: {self.reference}')
    else:
      print(f'H: {self.horizon} DICES: {self.dices}')

  def decide(self):
    action = random.choice(self.actions)
    print(f'Action: {action}')
    return action

  def sleep(self, result):
    self.results.append(result)
    print(f'--- Results: {str(result)}')


def plotResults(results, scope=100):
  # Calibrate the scope:
  if len(results) <= scope:
    scope = 1
  # Compute averages avery scope results:
  averageScores = []
  for i in range(scope, len(results) + 1):
    averageScores.append(sum(results[i - scope:i]) / scope)
  # And plot it:
  plt.plot(averageScores)
  plt.ylabel("scores")
  plt.show()


if __name__ == '__main__':
  main()
```
