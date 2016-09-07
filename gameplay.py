# gameplay.py
# Michael Wang (mgw55)
# 12/10/2014
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Gameplay represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Gameplay.

The subcontroller Gameplay manages the paddle, ball, and bricks.  These are model
objects.  The ball and the bricks are represented by classes stored in models.py.
The paddle does not need a new class (unless you want one), as it is an instance
of GRectangle provided by game2d.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Gameplay can only access attributes in models.py via getters/setters
# Gameplay is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Gameplay(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is
    won, it stops animating.  You should create a NEW instance of 
    Gameplay (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.
    
    INSTANCE ATTRIBUTES:
        _wall   [BrickWall]:  the bricks still remaining 
        _paddle [GRectangle]: the paddle to play with 
        _ball [Ball]: 
            the ball to animate
        _last [GPoint, or None if mouse button is not pressed]:  
            last mouse position (if Button pressed)
        _tries  [int >= 0]:   the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    might want to make a Paddle class for your paddle.  If you make changes,
    please change the invariants above.  Also, if you add more attributes,
    put them and their invariants below.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTries(self):
        """returns attribute _tries"""
        return self._tries
    def setTries(self, tries):
        """sets attribute _tries"""
        self._tries = tries
    
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """initializes an instance of Gameplay.
        
            sets wall, paddle, tries, and ball to their initial states"""
        self._wall = BrickWall()
        self._paddle = GRectangle(x = GAME_WIDTH/2,
                                  y = PADDLE_OFFSET,
                                  width = PADDLE_WIDTH,
                                  height = PADDLE_HEIGHT)
        self._last = None
        self.setTries(NUMBER_TURNS)
        self._ball = Ball()


    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self, view):
        """draws bricks, ball, paddle
        
            Parameters: view"""
        self._wall.draw(view)
        self._paddle.draw(view)
        self._ball.draw(view)
        

    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, touch, last):
        """updates _paddles position to follow that of the change in mouse position
        Parameters: touch, last"""
        if not last is None and not touch is None:
            self._paddle.x += touch.x - last.x
        if min(self._paddle.x, 0) < 0:
            self._paddle.x = 0
        if max(self._paddle.x + PADDLE_WIDTH, GAME_WIDTH) > GAME_WIDTH:
            self._paddle.x = GAME_WIDTH - PADDLE_WIDTH

    
    def updateBall(self):
        """makes use of move and detectWallCollision methods of _ball, and
        _getCollidingObject method to check for any collisions and move the ball
        """
   
        self._ball.move()
        self._ball.detectWallCollision()
        self._getCollidingObject()   
    
    
    def _getCollidingObject(self):
        """Returns: GObject that has collided with the ball
    
        This method checks the four corners of the ball, one at a 
        time. If one of these points collides with either the paddle 
        or a brick, it stops the checking immediately and returns the 
        object involved in the collision. It returns None if no 
        collision occurred."""
        self._wall.brickCollision(self._ball)
        self._ball.detectPaddleCollision(self._paddle)


    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    
    def detectFail(self):
        """This function detects whether or not the ball is above the bottom of the screen
        Returns True if ball below bottom, False otherwise"""
        
        if self._ball.bottom <= 0:
            return True
        else:
            return False
        
    def newBall(self):
        """Creates a new ball"""
        self._ball = Ball()
    
    def checkBricks(self):
        """Returns list of Bricks"""
        return self._wall.getBrickList()
    
    def refreshBricks(self, view):
        """Creates new set of bricks"""
        self._wall.newBricks(view)
    