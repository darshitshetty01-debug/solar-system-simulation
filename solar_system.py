from qdraw import window, circle, draw
from numpy import sin, cos, pi, arange

window(xlim=[-3500, 3500], ylim=[-3500, 3500], bgcolor="black")

planets = list(range(7))

R1 = 610.589
R2 = 980.48915
R3 = 1496.5043
R4 = 2018.0703875
R5 = 2672.015
R6 = 3166.124


planets[0] = circle(color = "yellow",     size= 750, pos=[0,0])
planets[1] = circle(color = "gray",       size= 100.0,    pos=[R1, 0])
planets[2] = circle(color = "goldenrod",  size= 248.01,   pos=[R2, 0])
planets[3] = circle(color = "royalblue",  size= 261.08,   pos=[R3, 0])
planets[4] = circle(color = "orangered",  size= 138.75,    pos=[R4, 0])
planets[5] = circle(color = "peru",       size= 429.81,  pos=[R5, 0])
planets[6] = circle(color = "khaki",      size= 298.325,  pos=[R6, 0])

planets[1].trail(color="white")
planets[2].trail(color="white")
planets[3].trail(color="white")
planets[4].trail(color="white")
planets[5].trail(color="white")
planets[6].trail(color="white")


for theta in arange(0,3000*pi,0.009):
    planets[1].setpos(R1*cos(theta),R1*sin(theta))
    planets[2].setpos(R2*cos(0.391*theta),R2*sin(0.391*theta))
    planets[3].setpos(R3*cos(0.240*theta),R3*sin(0.240*theta))
    planets[4].setpos(R4*cos(0.128*theta),R4*sin(0.128*theta))
    planets[5].setpos(R5*cos(0.020*theta),R5*sin(0.020*theta))
    planets[6].setpos(R6*cos(0.008*theta),R6*sin(0.008*theta))
    draw(0.01)