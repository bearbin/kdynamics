#import time
import sys
import brickpi3

MAX_POINT_Y = 64 * 12
COORDINATE_FRAME_CM = 230
COORDINATE_FRAME_CM_X = 230
COORDINATE_FRAME_CM_Y = 230
COORDINATE_BIG_STEP = 50
COORDINATE_SMALL_STEP = 10
BIG_STEP_SIZE = 1
SMALL_STEP_SIZE = 0.5
SCALING_FACTOR_CM = MAX_POINT_Y / COORDINATE_FRAME_CM

DRAW_OFFSET_X = 10
DRAW_OFFSET_Y = 220

CROSS_SIZE = 10

state = []

def offsetCoordinatesTuple(coords):
    return (coords[0] + DRAW_OFFSET_X, -coords[1] + DRAW_OFFSET_Y)

def drawWalls():
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
    drawLineTuple((0,0,0,168))        # a
    drawLineTuple((0,168,84,168))     # b
    drawLineTuple((84,168,84,210))    # c
    drawLineTuple((84,210,168,210))   # d
    drawLineTuple((168,210,168,84))   # e
    drawLineTuple((168,84,210,84))    # f
    drawLineTuple((210,84,210,0))     # g
    drawLineTuple((210,0,0,0))        # h

def drawPath():
    drawLineTuple((84,30,180, 30))     
    drawLineTuple((180,30,180,54))     
    drawLineTuple((180, 54, 138, 54))  
    drawLineTuple((138, 54, 138, 168)) 
    drawLineTuple((138,168,114, 168))  
    drawLineTuple((114,168,114,84))    
    drawLineTuple((114,84,84, 84))     
    drawLineTuple((84,84,84,30))       


def drawWorld():
    #drawCoordinateFrame(1)
    drawWalls()
    # drawPath()


def drawCross(x, y):
    drawLineTuple((x - CROSS_SIZE, y + CROSS_SIZE, x + CROSS_SIZE, y - CROSS_SIZE))
    drawLineTuple((x + CROSS_SIZE, y + CROSS_SIZE, x - CROSS_SIZE, y - CROSS_SIZE))


def drawLineTupleRaw(line):
    print("drawLine:" + str(line))


def drawLineXYRaw(x0,y0,x1,y1):
    drawLineTuple((x0,y0,x1,y1), offset=False)


def drawLineTuple(line, offset=True):
    if offset:
        offsetStart = offsetCoordinatesTuple((line[0], line[1]))
        offsetEnd = offsetCoordinatesTuple((line[2], line[3]))
        line = (offsetStart[0], offsetStart[1], offsetEnd[0], offsetEnd[1])
    drawLineTupleRaw(tuple([x * SCALING_FACTOR_CM for x in line]))


def drawLineXY(x0,y0,x1,y1):
    drawLineTuple((x0,y0,x1,y1))


def drawParticlesRaw(particles):
    print("drawParticles:" + str(particles))


# [(x, y, theta, weight)]
def drawParticles(particles):
    drawParticlesRaw(list(map(lambda x: ((x[0]+DRAW_OFFSET_X) * SCALING_FACTOR_CM, (-x[1]+DRAW_OFFSET_Y) * SCALING_FACTOR_CM, x[2], x[3]), particles)))




def drawParticlesStateful(particles):
    global state
    state += particles
    drawParticles(state)

# Point is (x, y, theta, weight)
def drawPointStateful(x, y, theta=0, weight=1):
    global state
    point = (x, y, theta, weight)
    state.append(point)
    drawParticles(state)

def resetDrawingState():
    state = []

def drawCoordinateFrame(withGrid):
    return
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
