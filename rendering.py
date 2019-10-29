import time
import sys
import brickpi3

def drawLineTuple(line):
    print("drawLine:" + str(line))

def drawLineXY(x0,y0,x1,y1):
    drawLineTuple((x0,y0,x1,y1))

def drawParticlesRaw(particles):
    print("drawParticles:" + str(particles))

def drawParticles(particles):
    drawParticlesRaw(map(lambda x: x, particles))
