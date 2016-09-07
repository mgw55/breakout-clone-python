# models.py
# Michael Wang (mgw55)
# 12/10/2014
"""Models module for Breakout

This module contains the model classes for the Breakout game. Anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, both paddle
and individual bricks can just be instances of GRectangle.  There is no need for a
new class in the case of these objects.

We only need a new class when we have to add extra features to our objects.  That
is why we have classes for Ball and BrickWall.  Ball is usually a subclass of GEllipse,
but it needs extra methods for movement and bouncing.  Similarly, BrickWall needs
methods for accessing and removing individual bricks.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *

def create_brick_row(i):
        """A helper function that creates a row of bricks i rows from the top"""
        brick_row = []
        for j in range(BRICKS_IN_ROW):
            brick_row.append(GRectangle(x = BRICK_SEP_H/2 + j*BRICK_SEP_H + j*BRICK_WIDTH,
                       y = GAME_WIDTH - BRICK_Y_OFFSET - i*BRICK_SEP_V - i*BRICK_HEIGHT,
                       width = BRICK_WIDTH,
                       height = BRICK_HEIGHT,
                       linecolor = ROW_COLORS[i%10],
                       fillcolor = ROW_COLORS[i%10]))
        return brick_row
# PRIMARY RULE: Models are not allowed to access anything in any module other than
# constants.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Gameplay should pass it as a argument when it
# calls the method.


class BrickWall(object):
    """An instance represents the layer of bricks in the game.  When the wall is
    empty, the game is over and the player has won. This model class keeps track of
    all of the bricks in the game, allowing them to be added or removed.
    
    INSTANCE ATTRIBUTES:
        _bricks [list of GRectangle, can be empty]:
            This is the list of currently active bricks in the game.  When a brick
            is destroyed, it is removed from the list.
    
    As you can see, this attribute is hidden.  You may find that you want to access 
    a brick from class Gameplay. It is okay if you do that,  but you MAY NOT 
    ACCESS THE ATTRIBUTE DIRECTLY. You must use a getter and/or setter for any 
    attribute that you need to access in GameController.  Only add the getters and 
    setters that you need.
    
    We highly recommend a getter called getBrickAt(x,y).  This method returns the first
    brick it finds for which the point (x,y) is INSIDE the brick.  This is useful for
    collision detection (e.g. it is a helper for _getCollidingObject).
    
    You will probably want a draw method too.  Otherwise, you need getters in Gameplay
    to draw the individual bricks.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    def __init__(self):
        self._bricks = []
        self.breaking = Sound('explosion.wav')
        for i in range(BRICK_ROWS):
            self._bricks.extend(create_brick_row(i))
        
    def draw(self, view):
        for brick in self._bricks:
            brick.draw(view)
    
    def brickCollision(self, ball):
        """loops through _bricks and checks each corner of the GEllipse ball
            for a collision. if there is a collision, pops brick from _bricks"""
        for brick in self._bricks:
            if brick.contains(ball.right,ball.bottom) and brick in self._bricks:
                self.breaking.play()
                self._bricks.remove(brick)
                #print 'bottom right'
                ball.verticalBounce()
            if brick.contains(ball.left,ball.bottom) and brick in self._bricks:
                self.breaking.play()
                self._bricks.remove(brick)
                #print 'bottom left'
                ball.verticalBounce()
            if brick.contains(ball.right,ball.top) and brick in self._bricks:
                self.breaking.play()
                self._bricks.remove(brick)
                #print 'top right'
                ball.verticalBounce()
            if brick.contains(ball.left,ball.top) and brick in self._bricks:
                self.breaking.play()
                self._bricks.remove(brick)
                #print 'top left'
                ball.verticalBounce()
    
    
    def getBrickList(self):
        """getter for _bricks attribute"""
        return self._bricks
    
    
    def newBricks(self, view):
        """re-initializes and re-draws the bricks"""
        self.__init__()
        for i in range(BRICK_ROWS):
            self._bricks.extend(create_brick_row(i))
        for brick in self._bricks:
            brick.draw(view)
        self.draw(view)    

class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction
        bouncsound [wavefile sound object]: 
    
    The class Gameplay will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    In addition you must add the following methods in this class: an __init__
    method to set the starting velocity and a method to "move" the ball.  The
    __init__ method will need to use the __init__ from GEllipse as a helper.
    The move method should adjust the ball position according to  the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getXVelocity(self):
        """gets _vx attribute of Ball"""
        return self._vx
    def getYVelocity(self):
        """gets _vy attribute of Ball"""
        return self._vy
    def getYpos(self):
        """getter for y pos of ball"""
        return self.y
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        GEllipse.__init__(self)
        #used general idea from CS1110 documentation for assignment 7
        self.gamemusic = Sound('gamemusic.wav')
        self.gamemusic.play()
        self._vx = 0
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -3.0
        self._width = BALL_DIAMETER
        self._height = BALL_DIAMETER
        self.center_x = (GAME_WIDTH)/2
        self.center_y = GAME_HEIGHT/3
        self.fillcolor = colormodel.BLACK
        self.bouncesound = Sound('bounce.wav')
        
        
        
    def move(self):
        """moves ball by _vx and _vy with each call"""
        self.center_x += self._vx
        self.center_y += self._vy
        
    
    def detectWallCollision(self):
        """detects when ball collides with a game wall. Negates _vx when side
        wall is hit, negates _vy when top wall is hit"""
        if self.right >= GAME_WIDTH or self.left <= 0:
            self._vx = -1.0 * self._vx
        if self.top >= GAME_HEIGHT:
            self._vy = -1.0 * self._vy
    
    def detectPaddleCollision(self, paddle):
        """loops through 4 corners of ball and checks if paddle contains any corners.
        if paddle contains a corner, verticalBounce method called"""
        if paddle.contains(self.left,self.top) and self._vy < 0:
            self.bouncesound.play()
            self.verticalBounce()
            self._vx = random.uniform(5.0, 15.0)
            #print 'topright paddle collision'
        if paddle.contains(self.left,self.bottom) and self._vy < 0:
            self.bouncesound.play()
            self.verticalBounce()
            self._vx = random.uniform(5.0, 13.0)
            #print 'bottomright paddle collision'
        if paddle.contains(self.right,self.top) and self._vy < 0:
            self.bouncesound.play()
            self.verticalBounce()
            self._vx = random.uniform(5.0, 13.0)
            #print 'topleft paddle collision'
        if paddle.contains(self.right,self.bottom) and self._vy < 0:
            self.bouncesound.play()
            self.verticalBounce()
            self._vx = random.uniform(-15.0,-5.0)
            #print 'bottomleft paddle collision'

    def verticalBounce(self):
        """helper method to minimize repetition. Negates Y velocity with a .2 range of randomization"""
        self._vy = random.uniform(-1.1,-.9) * self._vy

