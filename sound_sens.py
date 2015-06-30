#!/usr/bin/python
from wavebender import *

import pygame
import urllib
from OpenGL.GL import *
from OpenGL.GLU import *
from math import radians
from pygame.locals import *
import os

SCREEN_SIZE = (800, 600)
SCALAR = .5
SCALAR2 = 0.2

def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.001, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 1.0, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)
    
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0));

def read_values():
    link = "http://10.42.0.32:8080" # Change this address to your settings
    f = urllib.urlopen(link)
    myfile = f.read()
    return myfile.split(" ")

def writeSound(x, y):
    channels = ((damped(x,y),), (damped(x,y),))
    samples = compute_samples(channels, 44100 * 0.1)

    write_wavefile('test.wav', samples, 44100 * 0.1, nchannels=2)
    command = 'aplay ./test.wav'
    os.system(command)

def violin(x, y):
    l = int(44100*0.4) # each note lasts 0.4 second
    amp = map(-90, 90, x, 2, 0.2)
    freq = map(-90, 90, y, 800, 350)
    
    return (chain(damped_wave(frequency=0.8 * freq, framerate=44100, amplitude=0.76*amp, length=l * 0.1),
                  damped_wave(frequency=1.3 * freq, framerate=44100, amplitude=0.44*amp, length=l * 0.1),
                  damped_wave(frequency=2.5 * freq, framerate=44100, amplitude=0.32*amp, length=l * 0.1),
                  damped_wave(frequency=7.0 * freq, framerate=44100, amplitude=0.16*amp, length=l * 0.1),
                  damped_wave(frequency=1.2 * freq, framerate=44100, amplitude=1.00*amp, length=l * 0.1),
                  damped_wave(frequency=2.0 * freq, framerate=44100, amplitude=0.44*amp, length=l * 0.1),
                  damped_wave(frequency=3.2 * freq, framerate=44100, amplitude=0.32*amp, length=l * 0.1)))

def damped(x, y):
    l = int(44100*0.4) # each note lasts 0.4 second

    amp = map(-90, 90, x, 2, 0.2)
    freq = map(-90, 90, y, 750, 320)
    
    return islice( damped_wave(frequency=freq, framerate=44100, amplitude=amp, length=int(l/4)), l )
    
def damped2(x, y):
    l = int(44100*0.4) # each note lasts 0.4 second

    amp = map(-90, 90, x, 1, 0.01)
    freq = map(-90, 90, y, 450, 250)
    
    return islice( damped_wave(frequency=freq, framerate=44100, amplitude=amp, length=int(l/4)), l )

    
def waves(x, y):
    l = int(44100*0.4) # each note lasts 0.4 second
    amp = map(-90, 90, x, 2, 0.2)
    freq = map(-90, 90, y, 650, 300)
    
    return damped_wave(frequency=freq, framerate=44100, amplitude=amp, length=int(l/4))
    #return sine_wave(frequency=freq, framerate=44100, amplitude=amp)
    #return damped_wave(frequency = int(x/10), amplitude = int(y*0.1), length=int(l/4))

def map(in_min, in_max, x, out_min, out_max):
    return (x - in_min) * (out_max - out_min ) / (in_max - in_min) + out_min;

def visualisation(x_angle, y_angle, cube, color):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glColor((1.,1.,1.))

    glLineWidth(1)
    glBegin(GL_LINES)

    for x in range(-20, 22, 2):
        glVertex3f(x/10.,-1,-1)
        glVertex3f(x/10.,-1,1)
    
    for x in range(-20, 22, 2):
        glVertex3f(x/10.,-1, 1)
        glVertex3f(x/10., 1, 1)
    
    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z/10.)
        glVertex3f( 2, -1, z/10.)

    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z/10.)
        glVertex3f(-2,  1, z/10.)

    for z in range(-10, 12, 2):
        glVertex3f( 2, -1, z/10.)
        glVertex3f( 2,  1, z/10.)

    for y in range(-10, 12, 2):
        glVertex3f(-2, y/10., 1)
        glVertex3f( 2, y/10., 1)
    
    for y in range(-10, 12, 2):
        glVertex3f(-2, y/10., 1)
        glVertex3f(-2, y/10., -1)
    
    for y in range(-10, 12, 2):
        glVertex3f(2, y/10., 1)
        glVertex3f(2, y/10., -1)
    
    glEnd()
    glPushMatrix()
    glRotate(float(x_angle), 1, 0, 0)
    glRotate(-float(y_angle), 0, 0, 1)

    if (color):
        cube.setColor((1., 0., 0.))
    else:
        cube.setColor((1., 1., 1.))

    cube.render()
    glPopMatrix()
    pygame.display.flip()


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resize(*SCREEN_SIZE)
    init()
    #clock = pygame.time.Clock()
    cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))

    x_good_angle = 0
    y_good_angle = 0

    x_old_accel = 0
    y_old_accel = 0

    while True:
        values = read_values()

        x_angle = float(values[0])
        y_angle = float(values[1])
        x_accel = float(values[2])
        y_accel = float(values[3])
        z_accel = float(values[4])
        x_gyro  = float(values[5])
        y_gyro  = float(values[6])
        z_gyro  = float(values[7])

        #print values
        #print "x: " , x_angles[-1] , ";  y: " , y_angles[-1]
        #print "x: " , x_accel , ";  y: " , y_accel ,  ";  z: " , z_accel


        if (abs(x_accel) < 1.5 and abs(y_accel) < 1.5 and abs(z_accel) < 1.5 ):
            x_good_angle = x_angle
            y_good_angle = y_angle
            visualisation(x_angle, y_angle, cube, True)
        else:
            visualisation(x_angle, y_angle, cube, False)
            if (((abs(x_accel) - abs(x_old_accel)) + ((abs(y_accel) - abs(y_old_accel))) / 2) > 0.5 ):
                #print "x: " , x_accel , ";  y: " , y_accel , ";   x rot: " , x_angle , "  ;   y rot: " , y_angle
                writeSound(x_good_angle, y_good_angle)
                #pass
        x_old_accel = x_accel
        y_old_accel = y_accel


class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Cube information
    num_faces = 6

    vertices = [ (-1.0, -0.05, 0.5),
                 (1.0, -0.05, 0.5),
                 (1.0, 0.05, 0.5),
                 (-1.0, 0.05, 0.5),
                 (-1.0, -0.05, -0.5),
                 (1.0, -0.05, -0.5),
                 (1.0, 0.05, -0.5),
                 (-1.0, 0.05, -0.5) ]

    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ]  # bottom

    vertex_indices = [ (0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4) ]  # bottom

    def setColor(self, color):
        self.color = color

    def render(self):
        then = pygame.time.get_ticks()
        glColor(self.color)

        vertices = self.vertices

        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)

        for face_no in xrange(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])
        glEnd()

if __name__ == "__main__":
    #print("start GL visualisation")
    run()