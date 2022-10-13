# HackaGames - An Hackable Games' Engine

![](resources/logo-128.png)

**HackaGames** aims to be an open game engine dedicated to the development of Artificial Intelligence (AI) based on Operational Research (OR) technic.
The philosophy of hackagames is to permit developers to easily work in any language of its choice.
For that, the project is based on a communication protocol relying on *ZeroMQ* and is developed accordingly to [KISS](https://fr.wikipedia.org/wiki/Principe_KISS) (Keep It Stupid Simple) principle.
The main feature of this project is to permit the game, players and AIs to works on their own process potentially distributed over different machines.
In other terms, **HackaGames** implement a simple client/server architecture to permit AI to take a seat on a game through a simple communication protocol.

**HackaGames** is seen as an API for game development.
Several games are proposed with the API for example:

- **421** (Python): A very simple one player dice game to get the concept of AI implementation (not a core HackaGames client/server game).
- **TicTacToe** (Python): Classic and Ultimate _TicTacToe_ game.
- **Risky** (Python): a simple turm based startegic game.

## Concurency:

**HackaGame** is not what you looking for ? Try those solutions:

- https://ludii.games/ "a general game system designed to play, evaluate and design a wide range of games" (JAVA)
- https://www.pommerman.com/ an hackable Bomberman game (Python)
- https://www.codingame.com web-based environment for *NPC* development (complete solution but not open).

## License

**HackaGame** is distributed under the [MIT license](./LICENCE.md).
This API comme with absolutly no guarantee.

## Installation

**HackaGames** is natively developed on and for Linux systems.
Commands are given regarding Ubuntu-like distribution.
However, **HackaGames** is packaged in several levels where the level one is only relaing to `python3` language.
This way level one will supported what ever our favorit operating system is.

### Level one (python)

Level one consist in making the **hakapy** `python3` module working.
The network protocol of **HackaGames** relies on `zmq` library and process-bar are implemented via `tqdm`
So first get those dependancies for instance via `pip`.

```sh
pip3 install zmq tqdm
```

Then get Hackagame by cloning our repository in your working directory:

```bash
mkdir hacka-workspace
cd hacka-workspace
git clone https://bitbucket.org/imt-mobisyst/hackagames.git
```

That it.
You can play to several of the games (the ones developped on top of `hackapy`), and implement some IAs (cf. **Get Started** section).

### Level two (C)

Level two consist in compaling the **C** **hakalib** and the games built on top of the **C** lib.

Actually the **Level two** is desactivated due to majors modification in the client/server protocol.

<!--
**HackaGames** is natively developed on and for Linux systems.
Commands are given regarding Ubuntu-like distribution.

The classical way to get **HackaGames** is to clone then buid the project.
So first, you can clone this repository (game engine plus games):

The short way: 

```bash
./bin/install-dependencies
./bin/build
```
For the detailled way, see [install documentation](./doc/hacka-01-install.md)
-->

## Getting started

The easiest way is to play to one of the proposed python3 games, **421** for instance.

Each python3 game commes with `local` script permiting to start the game with interactive interface in a shell.

```sh
python3 hackagames/game421/local
```

The **421** is a tree dice game the player can roll several times to get a combinaison.
The player can perform one and only one action at it turns, and the game stops automatically after 2 turns.

The actions consist in keeping or rolling each of the 3 dices. So there are 8 actions:

- `keep-keep-keep`,  `keep-keep-roll`,  `keep-roll-keep`,  `keep-roll-roll`, `roll-keep-keep`,  `roll-keep-roll`,  `roll-roll-keep` and `roll-roll-roll`

The goal is to optimize the combination of dices before the end of the 2 turns.
The best combination ever is **421**.
But you can explore other combinations.

You can then follow the tutorial of [421](doc/tuto-game-421.md) to learn how to implement a AI to the game.

## In this repository

Directories:

- *bin* : scripts for project management.
- *.git* : git directory (version manager).
- *doc* : some documentation of the project.
- *hackalib* : Librairy and tools like interfaces in different programing language to help connect a game.
- *hackapy* : Python version of the librairy and tools.
- *gameXyz** : game examples on the top of **HackaGames** API.
- *resources* : some resources, images of **HackaGames** project.

Root Files:

- *README.md* : Your servitor.
- *LICENCE.md* : The Applied MIT license.

### Going further

See the documentation [table of contents](./doc/toc.md)

### Contributors

- Permanent contributor:
  * **Guillaume LOZENGUEZ** - [guillaume.lozenguez@imt-nord-europe.fr](mailto:guillaume.lozenguez@imt-nord-europe.fr)
