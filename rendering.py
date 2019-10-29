import time
import sys
import brickpi3

MAX_POINT_Y = 64 * 12
COORDINATE_FRAME_CM = 60
COORDINATE_FRAME_CM_X = 120
COORDINATE_FRAME_CM_Y = 60
COORDINATE_BIG_STEP = 10
COORDINATE_SMALL_STEP = 2
BIG_STEP_SIZE = 1
SMALL_STEP_SIZE = 0.5
SCALING_FACTOR_CM = MAX_POINT_Y / COORDINATE_FRAME_CM

def drawLineTupleRaw(line):
    print("drawLine:" + str(line))

def drawLineXYRaw(x0,y0,x1,y1):
    drawLineTuple((x0,y0,x1,y1))

def drawLineTuple(line):
    drawLineTupleRaw(tuple([x * SCALING_FACTOR_CM for x in line]))

def drawLineXY(x0,y0,x1,y1):
    drawLineTuple((x0,y0,x1,y1))

def drawParticlesRaw(particles):
    print("drawParticles:" + str(particles))

def drawParticles(particles):
    drawParticlesRaw(map(lambda x: x, particles))

def drawCoordinateFrame(withGrid):
    drawLineXY(0,0,0,COORDINATE_FRAME_CM_Y)
    drawLineXY(0,0,COORDINATE_FRAME_CM_X,0)
    for stepData in [[COORDINATE_BIG_STEP, BIG_STEP_SIZE], [COORDINATE_SMALL_STEP, SMALL_STEP_SIZE]]:
        step = stepData[0]
        sizeX = COORDINATE_FRAME_CM_X if withGrid else stepData[1]
        sizeY = COORDINATE_FRAME_CM_Y if withGrid else stepData[1]
        for x in range(step, COORDINATE_FRAME_CM_Y + 1, step):
            drawLineXY(0, x, sizeX, x)
        for x in range(step, COORDINATE_FRAME_CM_X + 1, step):
            drawLineXY(x, 0, x, sizeY)