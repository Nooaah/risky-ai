#!env python3
"""
HackaGame risky interface 
"""

import sys, os


sys.path.insert( 1, __file__.split('gameRisky')[0] )
import hackapy as hg

gamePath= __file__.split('gameRisky')[0] + "/gameRisky"

class ViewerTerminal:

    # Player interface :
    def __init__( self, aGame ):
        self.game= aGame
        self.generateGrid()
        mapFile= f"{gamePath}/resources/map-{self.game.board.status()}.txt"
        if os.path.exists( mapFile ) :
            self.loadGridBackground( mapFile )

    # grid: 
    def generateGrid(self):
        maxLine= 4
        maxLenght= 1
        for i in range( self.game.board.numberOfCells() ) :
            if self.game.board.cell(i).attribute(1) > maxLine :
                maxLine= self.game.board.cell(i).attribute(1)
            if self.game.board.cell(i).attribute(2) > maxLenght :
                maxLenght= self.game.board.cell(i).attribute(2)
            
        print( f"Grid size: ({maxLine}, {maxLenght})" )
        self.grid= [ [' ' for i in range(maxLenght+4) ] for line in range(maxLine+2) ]

    def loadGridBackground( self, mapFile ):
        f= open(mapFile)
        iLine= 0
        for line in f.readlines() :
            for iCol in range( len(line)-1 ) :
                self.grid[iLine][iCol]= line[iCol]
            iLine+= 1
    
    # Print: 
    def print(self, playerId):
        print( f'---\ngame state { self.game.board.status() }: player-{playerId} (turn { self.game.counter } over { self.game.duration })' )
        grid= [ [ x for x in line ] for line in self.grid ]
        for cell in self.game.board.cells() :
            cellId= str(cell.type().split('-')[1])
            line, col = cell.attribute(1), cell.attribute(2)
            if len( cell.children() ) > 0 :
                self.printArmyOnGrid( cell.child(1), grid, line, col )
            
            l= len(cellId)
            for i in range(l) :
                grid[line+1][col+3-l+i]=  cellId[i]

        for line in grid :
            print( '| '+ ''.join( line ) + ' |' )

    def printArmyOnGrid(self, army, grid, line, col):
        grid[line-1][col]= army.status()
        grid[line][col-2]= str(army.attribute(1))
        grid[line][col-1]= '-'
        force= str(army.attribute(2))
        while len( force ) < 3 :
            force= ' '+force
        grid[line][col]= force[0]
        grid[line][col+1]= force[1]
        grid[line][col+2]= force[2]
                
                