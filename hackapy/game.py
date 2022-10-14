
# Local HackaGame:
from . import interprocess
from tqdm import tqdm

class AbsGame():

    # Constructor
    def __init__(self, numerOfPlayers= 1 ):
        self.numberOfPlayers= numerOfPlayers

    # Game interface :
    def initialize(self):
        # Initialize a new game (not returning anyhing)
        # Return the game configuration (a AbsGamel)
        pass

    def playerHand( self, iPlayer ):
        # Return the game elements in the player vision (an AbsGamel)
        pass

    def applyPlayerAction( self, iPlayer, action ):
        # Apply the action choosen by the player iPlayer. return a boolean at True if the player terminate its actions for the current turn.
        pass

    def tic( self ):
        # called function at turn end, after all player played its actions. 
        pass

    def isEnded( self ):
        # must return True when the game end, and False the rest of the time.
        pass

    def playerScore( self, iPlayer ):
        # return the player score for the current game (usefull at game ending)
        pass
    
    # Process :
    def start(self, numberOfGames= 1, port=1400 ):
        dealer= interprocess.Dealer(port)
        self.startWithDealer(dealer, numberOfGames)

    def local(self, players, numberOfGames= 1 ):
        print( f" local games: {players} - {numberOfGames} " )
        assert( len(players) == self.numberOfPlayers )
        dealer= interprocess.Local(players)
        self.startWithDealer(dealer, numberOfGames)

    def startWithDealer(self, dealer, numberOfGames):
        print( f'HackaGame: wait for {self.numberOfPlayers} players' )
        dealer.waitForPlayers( self.numberOfPlayers )
        print( f'HackaGame: process {numberOfGames} games' )
        for i in tqdm(range(numberOfGames)) :
            self.play(dealer)
            dealer.changePlayerOrder()
        print( f'HackaGame: stop player-clients' )
        for i in range(1, self.numberOfPlayers+1) :
            dealer.stopPlayer( i )
    
    def play(self, aDealer):
        # Depend on how the players are handled: cf. AbsSequentialGame and AbsSimultaneousGame
        pass


class AbsSequentialGame(AbsGame):

    def play(self, aDealer):
        gameConf= self.initialize()
        aDealer.wakeUpPlayers( gameConf )
        iPlayer= 1
        # player take turns :
        while not self.isEnded() :
            action= aDealer.activatePlayer( iPlayer, self.playerHand(iPlayer) )
            # give a chance to propose a better action :
            while not self.applyPlayerAction( iPlayer, action ) :
                action= aDealer.activatePlayer( iPlayer, self.playerHand(iPlayer) )
            # switch player :
            iPlayer+= 1
            if iPlayer > self.numberOfPlayers :
                self.tic()
                iPlayer= 1
        # conclude the game :
        iPlayer= 1
        while iPlayer <= self.numberOfPlayers :
            aDealer.sleepPlayer( iPlayer, self.playerHand(iPlayer), self.playerScore(iPlayer) )
            iPlayer+= 1

class AbsSimultaneousGame(AbsGame):
    pass
