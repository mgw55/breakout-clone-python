# breakout.py
# Michael Wang (mgw55)
# 12/10/2014
"""Primary module for Breakout application

This module contains the App controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in either the gameplay
module or the models module. If you are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from gameplay import *
from game2d import *


# PRIMARY RULE: Breakout can only access attributes in gameplay.py via getters/setters
# Breakout is NOT allowed to access anything in models.py
STATE_COMPLETE = 4
class Breakout(GameApp):
    """Instance is a Breakout App
    
    This class extends GameApp and implements the various methods necessary 
    for processing the player inputs and starting/running a game.
    
        Method init starts up the game.
        
        Method update either changes the state or updates the Gameplay object
        
        Method draw displays the Gameplay object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the init method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Gameplay.
    Gameplay should have a minimum of two methods: updatePaddle(touch) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView, it is inherited from GameApp]:
            the game view, used in drawing (see examples from class)
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
            the current state of the game represented a value from constants.py
        _last   [GPoint, or None if mouse button is not pressed]:
            the last mouse position (if Button was pressed)
        _game   [GModel, or None if there is no game currently active]: 
            the game controller, which manages the paddle, ball, and bricks
        
    ADDITIONAL INVARIANTS: Attribute _game is only None if _state is STATE_INACTIVE.
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _mssg [GLabel or None if gamestate is not STATE_INACTIVE]
            GLabel message to be displayed on screen
        _countdown [0<int<180]:
            counts number of frames elapsed since _state changed to STATE_COUNTDOWN
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # GAMEAPP METHODS
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message (in attribute _mssg) saying that the user should 
        press to play a game."""
        
        
        self._last = None
        self._game = None
        self._state = STATE_INACTIVE
        self._mssg = GLabel(x = GAME_WIDTH/2.25, y = GAME_HEIGHT/2, text='Press to Play')
        self._countdown = 0
        self.victory = Sound('victory.wav')


    
    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, but most
        of the others belong in class Gameplay.
        
        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse (_last is None, but view.touch is not None). If so, it 
        (re)starts the game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        Paddle movement should be handled by class Gameplay (NOT in this class).
        This state should delay at least one second.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Gameplay (NOT in this class).
        Gameplay should have methods named updatePaddle and updateBall.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_INACTIVE.  All of these checks
        should be in Gameplay, NOT in this class.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly. If dt > 0.5, you have a 
        framerate problem because you are trying to do something too complex."""

        self.inactiveToCountdown()
        self.startGame()
        self.startCountdown()
        self.countdownToActive()
        self.giveCredits()
        self.updateGame()
        self.pauseToCountdown()
        self.startNewGame()
        self._last = self.view.touch
        
        
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Gameplay. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Gameplay.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        if self._state == STATE_INACTIVE:
            self._mssg.draw(self.view)
        elif self._state == STATE_COMPLETE:
            self._mssg.draw(self.view)
        elif self._state == STATE_PAUSED:
            self._mssg.draw(self.view)
        else:
            self._game.draw(self.view)
            

    # HELPER METHODS FOR THE STATES GO HERE
    def inactiveToCountdown(self):
        """Changes state from inactive to countdown when screen is clicked"""
        if self._state == STATE_INACTIVE:
                if self.view.touch == None and self._last != None:
                    self._state = STATE_COUNTDOWN
    
    def startGame(self):
        """Checks if state is not inactive and no game created, starts game and paddle if so"""
        if self._state != STATE_INACTIVE and self._game == None:
            self._game = Gameplay()
        if self._state != STATE_INACTIVE:
            self._game.updatePaddle(self.view.touch, self._last)

    def startCountdown(self):
        """starts countdown to start of game""" 
        if self._state == STATE_COUNTDOWN:
            while self._countdown < 1000:
                self._countdown += 1



    def countdownToActive(self):
        """checks if countdown is over, starts game, changes state to active"""
        if self._state == STATE_COUNTDOWN and self._countdown == 1000:
            self._state = STATE_ACTIVE
            self._countdown = 0
    
    
    def giveCredits(self):
        """Gives lives if game is starting up"""
        if self._state == STATE_ACTIVE and self._game.getTries == 0:
            self._state = STATE_INACTIVE    
            self._game = None
            self._game.setTries(NUMBER_TURNS)
            
    def checkLives(self):
        """Checks if any lives are left. If not, changes state to complete and displays Game Over Glabel"""
        if self._game.getTries() <= 0:
            self._state = STATE_COMPLETE
            #make a label that says game over, click to restart
            self._mssg = GLabel(x = GAME_WIDTH/3, y = GAME_HEIGHT/2.0, text='Lol, noob. Click to Start Again')
            self.draw()
    
    
    def checkWin(self):
        """Checks if all bricks are cleared, draws a win Glabel and changes state to Complete if so"""
        if self._game.checkBricks() == []:
            self._state = STATE_COMPLETE
            self.victory.play()
            self._game.refreshBricks(self.view)
            self._mssg = GLabel(x = GAME_WIDTH/4.5, y = GAME_HEIGHT/2.0, text='Congrats, you win! Click to Play Again')
            self.draw()
            self._last = None
            self._game = None
            self._state = STATE_INACTIVE
            self.update(0.4)
            self._countdown = 0

    
    def updateGame(self):
        """Updates movement of ball, also checks if all bricks are cleared and pauses game when ball hits bottom
            Changes state to pause and puts lives left on screen"""
        if self._state == STATE_ACTIVE:
            if self._game.detectFail():
                self._game.newBall()
                self._state = STATE_PAUSED
                self._game.setTries(self._game.getTries() - 1)
                self._mssg = GLabel(x = GAME_WIDTH/3.5, y = GAME_HEIGHT/2.0, text= str(self._game.getTries()) + (' Lives Left. Click to Continue'))
                self.draw()
                self.checkLives()
                
            else:
                self._game.updateBall()
                self.checkWin()
    
    def pauseToCountdown(self):
        """Allows the user to click and restart game after losing a life"""
        if self.view.touch == None and self._last != None:
            self._state = STATE_COUNTDOWN
    
    def startNewGame(self):
        """Checks if game is complete, then allows a click to restart the game, refreshes bricks, lives, etc."""
        if self._state == STATE_COMPLETE and self._game.checkBricks() != []:
            self.lose = Sound('lose.wav')
            self.lose.play()
            self._game.refreshBricks(self.view)
            self._last = None
            self._game = None
            self._state = STATE_INACTIVE
            self.update(0.4)
            self._mssg = GLabel(x = GAME_WIDTH/5, y = GAME_HEIGHT/2, text='Lol, noob. Tap the Mouse to Play Again.')
            self._countdown = 0

    
    