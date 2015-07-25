#!/usr/bin/python
from cube import *

import pygame

SCREEN_SIZE = (800, 600)
SCALAR = .5
SCALAR2 = 0.2
cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))
cube_accel = Cube((0.0, 0.0, 0.0), (.5, .5, .7))
cube_gyro = Cube((0.0, 0.0, 0.0), (.5, .5, .7))

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
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resize(*SCREEN_SIZE)
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

def visualisation(x_angle_filter, y_angle_filter, x_angle_accel, y_angle_accel, x_angle_gyro, y_angle_gyro, z_angle_gyro, color):
    #print "filter: [", x_angle_filter, ", ", y_angle_filter,"];  accel: [", x_angle_accel, ", ", y_angle_accel, "];  gyro" , x_angle_gyro, ", " , y_angle_gyro , "]"
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



    # accel cube
    glPushMatrix()
    glTranslate(1, 0, 0)

    glRotate(float(x_angle_accel), 1, 0, 0)
    glRotate(-float(y_angle_accel), 0, 0, 1)
    #glRotate(float(z_angle_gyro), 0, 1, 0)

    cube_accel.setColor((0., 1., 0.))

    cube_accel.render() 
    glTranslate(-1, 0, 0)  
    glPopMatrix()
    



    # gyro cube
    glPushMatrix()
    glRotate(float(x_angle_gyro), 1, 0, 0)
    glRotate(-float(y_angle_gyro), 0, 0, 1)
    #glRotate(float(z_angle_gyro), 0, 1, 0)

    cube_gyro.setColor((0., 0., 1.))

    cube_gyro.render()   
    glPopMatrix()



    # filter cube
    glPushMatrix()
    glTranslate(-1, 0, 0)
    glRotate(float(x_angle_filter), 1, 0, 0)
    glRotate(-float(y_angle_filter), 0, 0, 1)
    #glRotate(float(z_angle_gyro), 0, 1, 0)

    if (color):
        cube.setColor((1., 0., 0.))
    else:
        cube.setColor((1., 1., 1.))

    cube.render()
    glTranslate(1, 0, 0)
    glPopMatrix()

    pygame.display.flip()