#!env python3
"""
HackaGame - Game - Risky 
"""
import os, sys, random

sys.path.insert(1, __file__.split('gameRisky')[0])
import hackapy as hg

gamePath= __file__.split('gameRisky')[0] + "/gameRisky"

# Army Attributes
ACTION= 1
FORCE=  2

class GameRisky( hg.AbsSequentialGame ) :

    # Constructor :
    #--------------
    def __init__(self, numerOfPlayers= 2, map="board-4"):
        super().__init__(numerOfPlayers)
        # Attributes
        self.map= map
        self.counter= 0
        self.duration= 0
        self.maximalArmyForce= 24
        self.board= hg.Board()
        self.wrongAction= [ 0 for i in range(0, numerOfPlayers+1) ]
        # Configuration
        self.degatMethod= self.degatStochastic
        self.verbose= print

    def copy(self):
        cpy= GameRisky( self.numberOfPlayers, self.map )
        cpy.duration= self.duration
        cpy.maximalArmyForce= self.maximalArmyForce
        cpy.board= self.board.copy()
        cpy.wrongAction= [ x for x in self.wrongAction ]
        cpy.counter= self.counter
        return cpy

    # Game interface :
    #-----------------
    def initialize(self):
        # Initialize a new game (returning the game setting as a Gamel, a game ellement shared with player wake-up)
        f= open(f"{gamePath}/resources/map-{self.map}.gml")
        self.board.load( f.read() )
        f.close()
        for i in range(1, self.numberOfPlayers+1) :
            self.appendArmy( i, i, 12, 1 )
            #self.board.cell( i ).append-Child( hg.Gamel( "Army", self.playerLetter(i), [1, 12] ) )
        self.counter= 1
        if self.duration == 0 :
            self.duration= self.board.numberOfCells()
        self.board.setAttributes( [ self.counter, self.duration ] )
        return self.board

    def playerHand( self, iPlayer ):
        # Return the game elements in the player vision (an AbsGamel)
        self.board.setAttributes( [ self.counter, self.duration ] )
        return self.board

    def applyPlayerAction( self, iPlayer, action ):
        # Apply the action choosen by the player iPlayer. return a boolean at True if the player terminate its actions for the current turn.
        action= action.split(' ')
        cellIds= range( 1, self.board.numberOfCells()+1 )
        if action[0] == "move" and len( action ) == 4 :
            cellFrom= int(action[1])
            cellTo= int(action[2])
            force= int(action[3])
            army= self.armyOn(cellFrom)
            if cellFrom in cellIds and cellTo in cellIds and army and army.status() == self.playerLetter(iPlayer) and army.attribute(FORCE) >= force :
                return self.actionMove( iPlayer, cellFrom, cellTo, force )
        if action[0] == "grow" and len( action ) == 2 :
            cellId= int(action[1])
            army= self.armyOn(cellId)
            if cellId in cellIds and army and army.status() == self.playerLetter(iPlayer) :
                return self.actionGrow( iPlayer, cellId)
        if action[0] == "sleep" :
            return self.actionSleep( iPlayer )

        self.wrongAction[iPlayer]+= 1
        print( f"!!! Wrong action: {action} !!!" )
        if self.wrongAction[iPlayer] >= 8 :
            return self.actionSleep( iPlayer )
        return False

    def tic( self ):
        # called function at turn end, after all player played its actions. 
        self.counter= min( self.counter+1, self.duration )

    def isEnded( self ):
        # must return True when the game end, and False the rest of the time.
        return len( self.activePlayers() ) == 1 or self.counter >= self.duration 

    # Player access :
    #----------------
    def update( self, board ):
        self.board.setFrom( board )
        self.counter= self.board.attribute(1)
        self.duration= self.board.attribute(2)
    
    def searchActions(self, playerId):
        acts= [ ["sleep"] ]
        for i in range( 1, self.board.numberOfCells()+1) :
            cell= self.board.cell(i)
            if cell.children() and cell.child(1).status() == playerId and cell.child(1).attribute(ACTION) > 0 :
                acts.append( ["grow", i] )
                acts+= self.searchMoveAction(i)
        return acts
    
    def searchMoveAction( self, iCell ):
        force= self.armyOn(iCell).attribute(FORCE)
        return [ [ "move", iCell, target, force ] for target in self.edgesFrom( iCell ) ]

    def cellIds(self):
        return range(1, self.board.numberOfCells()+1)

    def edgesFrom(self, iCell):
        return self.board.edgesFrom(iCell)

    def armyOn(self, iCell) :
        if self.board.cell(iCell).children() :
            return self.board.cell(iCell).child()
        return False

    # Actions :
    #----------
    def actionMove( self, iPlayer, iFrom, iTo, force ):
        target= self.board.cell(iTo)
        army= self.armyOn(iFrom)
        if army :
            actCounter= army.attribute(ACTION)
            playerLetter= self.playerLetter(iPlayer)
            if playerLetter == army.status() and actCounter > 0 :
                # All the army ?
                if force >= army.attribute(FORCE) :
                    force= army.attribute(FORCE)
                    self.board.cell(iFrom).pop(1)
                else :
                    army.setAttribute(FORCE, army.attribute(FORCE)-force)
                # free target:
                if len( target.children() ) == 0 :
                    self.appendArmy( iPlayer, iTo, force, action= actCounter-1 )
                # friend target:
                elif target.child().status() == playerLetter :
                    targetArmy= target.child()
                    targetArmy.setAttribute(FORCE, targetArmy.attribute(FORCE)+force)
                    targetArmy.setAttribute( ACTION, min( targetArmy.attribute(ACTION), actCounter-1) )
                else: 
                    self.actionFight( iPlayer, actCounter, force, iTo )
            else :
                print( f"!!! Wrong move: unvalid army on {iFrom}!!!" )
        else :
            print( f"!!! Wrong move: no army on {iFrom} !!!" )
        return False
        
    def actionFight( self, iPlayer, actCounter, attack, iTo ):
        # Initialize:
        defence= self.armyOn(iTo).attribute(FORCE)
        # while fighters:
        while attack > 0 and defence > 0 :
            degatAtt, degatDef= self.degatMethod(attack, defence)
            self.verbose( f"Fight-{iTo}: {attack}({degatAtt}) vs {defence}({degatDef})" )
            attack= max( 0, attack - degatDef )
            defence= max( 0, defence - degatAtt )
        # Update cell: defence
        self.verbose( f"Fight-{iTo}: {attack} vs {defence}" )
        if defence == 0 :
            self.board.cell(iTo).pop()
        else :
            self.armyOn(iTo).setAttribute(FORCE, defence)
        # Update cell: attack
        if attack > 0 :
            self.appendArmy( iPlayer, iTo, attack, actCounter-1 )

    def degatDeterministic( self, attack, defence ):
        attackForce= attack + max(0, attack - defence)
        return (1+attackForce)//2, (2+defence*2)//3

    def degatStochastic( self, attack, defence ):
        attackForce= attack + max(0, attack-defence)
        degatAtt= 0
        for i in range( attackForce ):
            if random.randrange(12) < 6 :
                degatAtt+= 1
        degatDeff= 0
        for i in range( defence ):
            if random.randrange(12) < 8 :
                degatDeff+= 1
        return degatAtt, degatDeff

    def actionSleep( self, iPlayer ):
        playerLetter= self.playerLetter(iPlayer) 
        for cell in self.board.cells() :
            for army in cell.children() :
                if army.status() == playerLetter :
                    army.setAttribute( ACTION, min( 2, army.attribute(ACTION)+1) )
        return True

    def actionGrow( self, iPlayer, iCell ):
        playerLetter= self.playerLetter(iPlayer)
        army= self.armyOn(iCell)
        recrut= (2+army.attribute(FORCE))//3
        if army and army.status() == playerLetter and army.attribute(ACTION) > 0 :
            for iNeighbour in self.edgesFrom( iCell) :
                neighbourArmy= self.armyOn(iNeighbour)
                if neighbourArmy and neighbourArmy.status() == playerLetter :
                    recrut+= 1
            army.setAttribute( FORCE, min(army.attribute(FORCE)+recrut, self.maximalArmyForce) )
            army.setAttribute( ACTION, army.attribute(ACTION)-1 )
        return False

    def activePlayers(self):
        active= []
        for cell in self.board.cells() :
            for army in cell.children() :
                iPlayer= self.playerNum( army.status() )
                if iPlayer not in active :
                    active.append( iPlayer )
                    active.sort()
        return active
    
    def playerArmies(self):
        armies= [ 0 for i in range( self.numberOfPlayers+1 ) ]
        for cell in self.board.cells() :
            for army in cell.children() :
                iPlayer= self.playerNum( army.status() )
                armies[ iPlayer ]+= army.attribute(FORCE)
        return armies
    
    def playerScore( self, iPlayer ):
        # return the player score for the current game (usefull at game ending)
        armies= self.playerArmies()
        bestArmy= armies[0]
        winners= 0
        for i in range(1, self.numberOfPlayers+1) :
            if armies[i] > bestArmy :
                bestArmy= armies[i]
                winners= 1
            elif armies[i] == bestArmy :
                winners+= 1
        if winners == 1 and armies[iPlayer] == bestArmy :
            return 1
        return armies[iPlayer] - bestArmy
    
    # Risky tools :
    def appendArmy( self, iPLayer, position, force, action= 0 ):
        army= hg.Pod( "Army", self.playerLetter(iPLayer), [action, force] )
        self.board.cell(position).append( army )

    def playerLetter(self, iPlayer):
        return chr( ord("A")+iPlayer-1 )

    def playerNum(self, playerLetter):
        return 1 + ord(playerLetter) - ord("A")
