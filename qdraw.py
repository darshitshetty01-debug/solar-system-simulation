###########################################################################
#
# Functions for simple animated graphics, built on top of the turtle
# graphics capabilities of basic Python
#
# Written by Mark Newman <mejn@umich.edu>
# Version 0.92: 8 MAR 2025
# This software is released under the Revised BSD License.  You may use,
# share, or modify this file freely subject to the license terms below.
#
# Copyright 2025, Mark Newman
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###########################################################################

# Imports
from math import pi
from numpy import ones,linspace,sin,cos,column_stack
from time import sleep
from matplotlib import colormaps
from matplotlib.colors import Normalize
from turtle import Screen,Turtle,register_shape,update,bye,exitonclick

# Defaults
DEFAULT_SCREENWIDTH = 1000
DEFAULT_SCREENHEIGHT = 1000
DEFAULT_STARTX = 0
DEFAULT_STARTY = 0
DEFAULT_XMIN = 0.0
DEFAULT_XMAX = 1.0
DEFAULT_YMIN = 0.0
DEFAULT_YMAX = 1.0
DEFAULT_GRIDSIZE = 1
DEFAULT_SIZE = 1.0
DEFAULT_POS = (0,0)
DEFAULT_LINEWIDTH = 1
DEFAULT_OLWIDTH = 1
DEFAULT_TRAILWIDTH = 4
DEFAULT_FG = "black"
DEFAULT_BG = "white"
DEFAULT_TITLE = "Python Graphics"
DEFAULT_CMAP = "viridis"
DEFAULT_VMIN = 0.0
DEFAULT_VMAX = 1.0
CIRCLE_POINTS = 64

# Globals
__qdwindow__ = None

# Classes

# Window class
class window():

    def __init__(self,width=None,height=None,xlim=None,ylim=None,
                 position=(DEFAULT_STARTX,DEFAULT_STARTY),
                 bgcolor=DEFAULT_BG,title=DEFAULT_TITLE):

        # Create the window
        self.screen = Screen()
        self.screen.title(title)

        # Set the axes
        widthv,heightv,xlimv,ylimv = limits(width,height,xlim,ylim)
        self.screen.setup(widthv,heightv,position[0],position[1])
        self.screen.setworldcoordinates(xlimv[0],ylimv[0],xlimv[1],ylimv[1])
        self.xfactor = widthv/(xlimv[1]-xlimv[0])
        self.yfactor = heightv/(ylimv[1]-ylimv[0])
        self.center = (0.5*(xlimv[0]+xlimv[1]),0.5*(ylimv[0]+ylimv[1]))

        # Set the color, mode, and colormap
        self.cmap = colormaps[DEFAULT_CMAP]
        self.norm = Normalize(DEFAULT_VMIN,DEFAULT_VMAX)
        self.screen.colormode(1)
        self.screen.bgcolor(mapcolor(bgcolor))
        self.screen.tracer(False)

        # Trap user window-close events
        toplevel = self.screen.getcanvas().winfo_toplevel()
        toplevel.protocol("WM_DELETE_WINDOW",wclose)

        # Register shapes
        makeshapes()

        # Store the window object for later use
        global __qdwindow__
        __qdwindow__ = self

# Line
class line(Turtle):

    # Constructor
    def __init__(self,width=DEFAULT_LINEWIDTH,color=DEFAULT_FG):

        # Check if window exists
        if __qdwindow__ is None: raise RuntimeError("No graphics window")

        # Call the Turtle constructor
        super().__init__()

        # Default behaviors
        self.width(width)
        self.pencolor(mapcolor(color))
        self.penup()
        self.radians()
        self.setheading(0)
        self.hideturtle()
        self.visibleon = True

    # Set the points along the line
    def setline(self,x,y):
        if self.visibleon:
            n = min(len(x),len(y))
            if n<1: return
            self.clear()
            self.setpos(x[0],y[0])
            self.pendown()
            for k in range(1,n): self.setpos(x[k],y[k])
            self.penup()

    # Set color
    def setcolor(self,color):
        self.color(mapcolor(color))

    # Turn on and off
    def visible(self,b=True):
        if b: self.visibleon = True
        else:
            self.clear()
            self.visibleon = False

# General shape class
class shape(Turtle):

    # Constructor
    def __init__(self):

        # Check if window exists
        if __qdwindow__ is None: raise RuntimeError("No graphics window")

        # Call the Turtle constructor
        super().__init__()

        # Default behaviors
        self.penup()
        self.radians()
        self.setheading(0)
        self.trailon = self.streamon = False

    # Set position
    def setpos(self,x,y=None):
        super().setpos(x,y)
        if self.streamon:
            self.streamx[1:] = self.streamx[:-1]
            self.streamy[1:] = self.streamy[:-1]
            if y is None: self.streamx[0],self.streamy[0] = x
            else: self.streamx[0],self.streamy[0] = x,y
            self.streamer.setline(self.streamx,self.streamy)

    # Set angle
    def setangle(self,angle):
        self.setheading(angle)

    # Set color and outline color
    def setcolor(self,color=None,olcolor=None):
        if color is None:
            pencolor,fillcolor = self.color()
            if olcolor is None: return fillcolor,pencolor
            self.color(mapcolor(olcolor),fillcolor)
        else:
            if olcolor is None: self.color(mapcolor(color))
            else: self.color(mapcolor(olcolor),mapcolor(color))

    # Turn on and off
    def visible(self,b=True):
        if b:
            self.showturtle()
            if self.streamon: self.streamer.visible(True)
            elif self.trailon: self.pendown()
        else:
            self.hideturtle()
            if self.streamon:
                self.streamer.visible(False)
            elif self.trailon:
                self.clear()
                self.penup()

    # Turn trail on or off and set length, width, and color
    def trail(self,activate=True,length=None,width=DEFAULT_TRAILWIDTH,
              color=DEFAULT_FG):
        self.trailon = activate
        if activate:
            if length:
                # Streamer
                self.streamer = line(width,color)
                x,y = self.pos()
                self.streamx = x*ones(length,float)
                self.streamy = y*ones(length,float)
                self.streamon = True
                self.streamlength = length
            else:
                # Trail
                self.width(width)
                self.pencolor(mapcolor(color))
                self.pendown()
        else:
            if self.streamon:
                self.streamon = False
            else:
                self.penup()

# Ellipse
class ellipse(shape):

    def __init__(self,width=DEFAULT_SIZE,height=None,pos=None,
                 color=DEFAULT_FG,olcolor=None,olwidth=DEFAULT_OLWIDTH,
                 pixelsize=False):
        super().__init__()
        w = __qdwindow__
        self.shape("__qdcircle__")
        if height is None: height = width
        if pixelsize:
            self.turtlesize(width,height,outline=olwidth)
        else:
            self.turtlesize(width*w.xfactor,height*w.yfactor,outline=olwidth)
        if pos is None: self.setpos(w.center)
        else: self.setpos(pos)
        if olcolor is None: self.color(mapcolor(color))
        else: self.color(mapcolor(olcolor),mapcolor(color))

# Circle
class circle(ellipse):
    def __init__(self,size=DEFAULT_SIZE,pos=None,color=DEFAULT_FG,
                 olcolor=None,olwidth=DEFAULT_OLWIDTH,pixelsize=False):
        super().__init__(width=size,height=size,pos=pos,color=color,
                         olwidth=olwidth,olcolor=olcolor,pixelsize=pixelsize)

# Square
class square(shape):

    def __init__(self,size=DEFAULT_SIZE,pos=None,color=DEFAULT_FG,
                 olcolor=None,olwidth=DEFAULT_OLWIDTH,pixelsize=False):
        super().__init__()
        w = __qdwindow__
        self.shape("__qdsquare__")
        if pixelsize:
            self.turtlesize(size,size,outline=olwidth)
        else:
            self.turtlesize(size*w.yfactor,size*w.xfactor,outline=olwidth)
        if pos is None: self.setpos(w.center)
        else: self.setpos(pos)
        if olcolor is None: self.color(mapcolor(color))
        else: self.color(mapcolor(olcolor),mapcolor(color))

# Rectangle
class rectangle(shape):

    def __init__(self,left=-DEFAULT_SIZE,right=DEFAULT_SIZE,
                 bottom=-DEFAULT_SIZE,top=DEFAULT_SIZE,
                 pos=None,color=DEFAULT_FG,
                 olcolor=None,olwidth=DEFAULT_OLWIDTH,pixelsize=False):
        super().__init__()
        w = __qdwindow__
        if pixelsize:
            ls,rs = left,right
            bs,ts = bottom,top
        else:
            ls,rs = w.xfactor*left,w.xfactor*right
            bs,ts = w.yfactor*bottom,w.yfactor*top
        h = hash((left,right,bottom,top))
        name = "qdrectangle" + str(h)
        register_shape(name,((-ls,-bs),(-ls,-ts),(-rs,-ts),(-rs,-bs)))
        self.shape(name)
        self.turtlesize(outline=olwidth)
        if pos is None: self.setpos(w.center)
        else: self.setpos(pos)
        if olcolor is None: self.color(mapcolor(color))
        else: self.color(mapcolor(olcolor),mapcolor(color))

# Polygon
class polygon(shape):

    def __init__(self,path,pos=None,color=DEFAULT_FG,
                 olcolor=None,olwidth=DEFAULT_OLWIDTH,pixelsize=False):
        super().__init__()
        w = __qdwindow__
        if pixelsize:
            pathtuple = tuple((-x,-y) for (x,y) in path)
        else:
            pathtuple = tuple((-w.xfactor*x,-w.yfactor*y) for (x,y) in path)
        h = hash(pathtuple)
        name = "qdpoly" + str(h)
        register_shape(name,pathtuple)
        self.shape(name)
        self.turtlesize(outline=olwidth)
        if pos is None: self.setpos(w.center)
        else: self.setpos(pos)
        if olcolor is None: self.color(mapcolor(color))
        else: self.color(mapcolor(olcolor),mapcolor(color))

# Grid
class grid():

    # Constructor
    def __init__(self,size=(DEFAULT_GRIDSIZE,DEFAULT_GRIDSIZE),pos=DEFAULT_POS,
                 olcolor=None,olwidth=None):

        # Check if window exists
        if __qdwindow__ is None: raise RuntimeError("No graphics window")

        # Parameters
        self.xsize,self.ysize = size
        self.olcolor = olcolor

        # Make the grid
        self.grid = list()
        for i in range(self.xsize):
            row = list()
            for j in range(self.ysize):
                row.append(square(size=1,pos=(pos[0]+i+0.5,pos[1]+j+0.5),
                                  color=0.0,olcolor=olcolor,olwidth=olwidth))
            self.grid.append(row)

    # Update complete grid
    def setgrid(self,value):
        for i in range(self.xsize):
            for j in range(self.ysize):
                self.grid[i][j].setcolor(color=value[i,j],olcolor=self.olcolor)

    # Update a single grid point
    def setpoint(self,i,j,value):
        self.grid[i][j].setcolor(color=value,olcolor=self.olcolor)

# Functions

# Register new shapes
def makeshapes():

    # Circle with diameter 1
    theta = linspace(0,2*pi,CIRCLE_POINTS,endpoint=False)
    c = column_stack((0.5*cos(theta),0.5*sin(theta)))
    register_shape("__qdcircle__",tuple(c))

    # Square with side length 1
    register_shape("__qdsquare__",((0.5,0.5),(0.5,-0.5),(-0.5,-0.5),(-0.5,0.5)))

# Helper function to fill in missing dimensions for window size
def limits(w,h,x,y):

    # Count number of parameters of each type
    nwh = nxy = 0
    if w is not None: nwh += 1
    if h is not None: nwh += 1
    if x is not None: nxy += 1
    if y is not None: nxy += 1
    ntotal = nwh + nxy

    # Zero parameters are given
    if ntotal==0:
        w,h = DEFAULT_SCREENWIDTH,DEFAULT_SCREENHEIGHT
        x,y = (DEFAULT_XMIN,DEFAULT_XMAX),(DEFAULT_YMIN,DEFAULT_YMAX)

    # One parameter is given
    elif ntotal==1:
        if w is not None:
            h = w
            x,y = (DEFAULT_XMIN,DEFAULT_XMAX),(DEFAULT_YMIN,DEFAULT_YMAX)
        elif h is not None:
            w = h
            x,y = (DEFAULT_XMIN,DEFAULT_XMAX),(DEFAULT_YMIN,DEFAULT_YMAX)
        elif x is not None:
            y = x
            w,h = DEFAULT_SCREENWIDTH,DEFAULT_SCREENHEIGHT
        else:
            x = y
            w,h = DEFAULT_SCREENWIDTH,DEFAULT_SCREENHEIGHT

    # Two parameters are given
    elif ntotal==2:
        if nwh==2:
            x = (DEFAULT_XMIN,DEFAULT_XMAX)
            y = (DEFAULT_YMIN*h/w,DEFAULT_YMAX*h/w)
        elif nxy==2:
            dx = x[1]-x[0]
            dy = y[1]-y[0]
            if dx<dy:
                w = int(DEFAULT_SCREENWIDTH*dx/dy+0.5)
                h = DEFAULT_SCREENHEIGHT
            else:
                w = DEFAULT_SCREENWIDTH
                h = int(DEFAULT_SCREENHEIGHT*dy/dx+0.5)
        else:
            if w is None: w = h
            if h is None: h = w
            if x is None: x = y
            if y is None: y = x

    # Three parameters given
    elif ntotal==3:
        if w is None:
            dx = x[1]-x[0]
            dy = y[1]-y[0]
            w = int(h*dx/dy+0.5)
        elif h is None:
            dx = x[1]-x[0]
            dy = y[1]-y[0]
            h = int(w*dy/dx+0.5)
        elif x is None:
            x = (y[0]*w/h,y[1]*w/h)
        else:
            y = (x[0]*h/w,x[1]*h/w)

    # Four parameters given
    else:
        dx = x[1]-x[0]
        dy = y[1]-y[0]
        if dx<dy:
            w = int(h*dx/dy+0.5)
        else:
            h = int(w*dy/dx+0.5)

    return w,h,x,y


# Helper function that adds matplotlib-style colormaps and 1-character colors
def mapcolor(color):
    if isinstance(color,str):
        if len(color)==1:
            if   color=="k": return "black"
            elif color=="r": return "red"
            elif color=="g": return "green"
            elif color=="b": return "blue"
            elif color=="c": return "cyan"
            elif color=="m": return "magenta"
            elif color=="y": return "yellow"
            elif color=="w": return "white"
        return color
    try:
        if len(color)>1: return color
    except:
        pass
    w = __qdwindow__
    return w.cmap(w.norm(float(color)))[:3]

# Set color map
def setcmap(cmap=DEFAULT_CMAP,vmin=None,vmax=None):
    w = __qdwindow__
    w.cmap = colormaps[cmap]
    if vmin is not None and vmax is not None:
        w.norm = Normalize(vmin,vmax)

# Helper function for catching close-window events
def wclose():
    bye()
    global __qdwindow__
    __qdwindow__ = None

# Draw frame and wait the specified number of seconds
def draw(wait=0):
    if __qdwindow__ is None: raise RuntimeError("No graphics window")
    update()
    sleep(wait)

# Draw frame and hold, then delete the window
def show():
    global __qdwindow__
    if __qdwindow__ is None: raise RuntimeError("No graphics window")
    update()
    exitonclick()
    __qdwindow__ = None

# Alternate name for draw frame and hold
def hold():
    show()