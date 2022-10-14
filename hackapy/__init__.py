#!env python3

from . import pieceOfData, component, game, player, command
#from . import element, interprocess, game, player, cmd

# HackaGames Elements
Pod= pieceOfData.Pod
Board= component.Board
AbsGame= game.AbsGame
AbsSequentialGame= game.AbsSequentialGame
AbsSimultaneousGame= game.AbsSimultaneousGame
AbsPlayer= player.AbsPlayer
PlayerIHM= player.PlayerIHM

#Piece= game.Piece
#Cell= game.Cell
#Tabletop= game.Tabletop

# Command tools
StartCmd= command.StartCmd
