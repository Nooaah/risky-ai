# TicTacToe, an HackaGames game

- Return to the [Table Of Content](toc.md)


**TicTacToe** is simple two-player games where each player tries to align trees of their pieces.

It comes in two versions: _classic_ and _ultimate_.

## Installation

**TicTacToe** (as **HackaGames**) is natively developed on and for Linux systems.
Commands are given regarding Ubuntu-like distribution.

**TicTacToe** is included in the minimal **HackaGames** package (i.e. nothing to do here).

## Try the game:

**TicTacToe** is a standard **HackaGames** game, and it works with a client-server architecture.
The server is the game, the clients are the players.

First start the game server (from **HackaGames** repository) :

```sh
./gameTictactoe/start.py
```

This starts **TicTacToe** in classic mode for 2 games. Each player will take turns at starting. To start in ultimate mode with a different number of games: `./gameTictactoe/start.py ultimate -n 100`

Then, in a new terminal start the a **HackaGames** terminal player dedicated to **TicTacToe** (the basic **HackaGames** terminal player `./play.py` will work but with a less fancy interface):

```sh
./gameTictactoe/play.py
```

The player can perform one and only one action at it turns, and the game stops automatically with a winner or when no more pieces can be set on the tabletop.

The actions consist in set a player's piece on a position. 

- 3 times 3 actions in _classic_ mode: `A-1`, `A-2`, `A-3`, `B-1`, `B-2`, `B-3`, `C-1`, `C-2` and `C-3`
- 9 times 9 actions in _ultimate_ mode: `A-1`, `A-2`, ... , `A-9`, `B-1`, ... , `I-9` (most of the time, only a sub-number of actions are available).

In _classic_ **TicTacToe** the first player aligning 3 of its pieces win the game.
The _ultimate_ mode is a hierarchical 2-levels **TicTacToe**. The players have to win 3 aligned _classic_ grids to win an _ultimate_ **TicTacToe**. 
The particularity in hierarchical **TicTacToe** is that, the took position by a player in the _classic_ grid indicates the next grid to play for the next player turn.

## Let an AI play:

The file `./gameTictactoe/firstAI.py` propose a first random-safe AI with the required structure to play **TicTacToe**.
The **firstAI** will win if possible, prevent the oponent to win if possible or play in a random manner.

to test the player, start the server and 2 players in 3 different terminals:

```sh
./gameTictactoe/start.py
```

then :
```sh
./gameTictactoe/firstAI.py
```

You have to launch `firstAI.py` 2 times or with `play.py` if you wana fight the AI.

To notice that, you can increase the numbers of games with the `-n` attribute:

```sh
./gameTictactoe/start.py -n 1000
```

### Your first AI:

In a directory dedicated to your work, you start an Ia from the proposed random player:

```bash
mkdir draft
cp gameTictactoe/firstAI.py draft/myTictactoeAI.py
```

If it is your first time with **HackaGames** AI, try the **421** game first.

The goal is to generate an AI beating the `firstAI.py` in _classic_ mode, then in _ultimate_ mode.
