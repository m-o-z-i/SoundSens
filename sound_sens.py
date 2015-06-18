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
    channels = ((waves(x,y),), (waves(x,y),))
    samples = compute_samples(channels, None)
    #music = write_wavefile2('test.wav', samples, None)
    write_wavefile3('test.wav', samples, None)
    command = 'aplay ./test.wav'
    os.system(command)

def waves(x, y):
    l = int(44100*0.4) # each note lasts 0.4 second
    #x = float(x) + 90;
    freq_x = map2(-90, 90, x, 200, 600);
    amp_y = map2(-90, 90, y, 0.5, 1.5)
    print "freq: " , freq_x , "   amp: " , amp_y
    return damped_wave(frequency=freq_x, amplitude=amp_y, length=int(l/20))
    #return damped_wave(frequency = int(x/10), amplitude = int(y*0.1), length=int(l/4))


def map(val_min, val_max, val, in_min, in_max):
    total_in = float(in_max) - float(in_min)
    #print 'total in  ', total_in
    total_val = float(val_max) - float(val_min)
    #print 'total val  ', total_val
    if (val < 0):
        print abs(float(val) - float(val_min)) 
        return abs(float(val) - float(val_min)) * total_in/total_val
    else:
        print (float(val) - float(val_min))
        return (float(val) - float(val_min)) * total_in/total_val 

def map2(in_min, in_max, x, out_min, out_max):
    return (float(x) -float(in_min))*(float(out_max)-float(out_min)) / (float(in_max)-float(in_min) )+ float(out_min);
        

def mapFrequency(freq):
    test = -90 - freq
    test2 = test * test
    return test

def mapAccel(accel):
    return accel

def visualisation(x_angle, y_angle, cube):
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

    while True:
        values = read_values()
        print values
        x_angle = values[0]
        y_angle = values[1]

        #other data ...
        visualisation(x_angle, y_angle, cube)
        writeSound(x_angle, y_angle)




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