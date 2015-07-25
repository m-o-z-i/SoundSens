#!/usr/bin/python
from wavebender import *

import pygame
import urllib
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from math import radians
from pygame.locals import *
import os

SCREEN_SIZE = (800, 600)
SCALAR = .5
SCALAR2 = 0.2

#for gyro calibration
gyro_calib_x = 0
gyro_calib_y = 0
gyro_calib_z = 0

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
    link = "http://10.42.0.27:8080" # Change this address to your settings
    f = urllib.urlopen(link)
    myfile = f.read()
    return myfile.split(" ")

def writeSound(x, y, length):
    soundlength = 0.4
    l1 = 44100 * 0.4
    l2 = l1
    amp = map(-90, 90, x, 0.1, 0.01)
    freq = map(-90, 90, y, 900, 50)

    if (length > 0.4):
        l1 = 8 * l1
        l2 = 2  * l2
        soundlength = 2.0


    channels = ((C(l1, l2),), (C(l1, l2),))
    if(freq < 250):
        print "C ---> (" , freq , ")"
    elif(freq < 360):
        channels = ((D(l1, l2),), (D(l1, l2),))
        print "D ---> (" , freq , ")"
    elif(freq < 470):
        channels = ((E(l1, l2),), (E(l1, l2),))
        print "E ---> (" , freq , ")"
    elif(freq < 580):
        channels = ((F(l1, l2),), (F(l1, l2),))
        print "F ---> (" , freq , ")"
    elif(freq < 690):
        channels = ((G(l1, l2),), (G(l1, l2),))
        print "G ---> (" , freq , ")"
    else:
        channels = ((A(l1, l2),), (A(l1, l2),))
        print "A ---> (" , freq , ")"

    samples = compute_samples(channels, 44100 * soundlength)

    write_wavefile('test.wav', samples, 44100 * soundlength, nchannels=2)
    command = 'aplay ./test.wav'
    os.system(command)

def writeSound1C(x, y, length):
    channels = (violinOrig(x,y, length),)
    samples = compute_samples(channels, 44100 * length)

    write_wavefile('test.wav', samples, 44100 * length, nchannels=1)
    command = 'aplay ./test.wav'
    os.system(command)


def writeSound2C(x, y, length):
    channels = (violinG(x,y, length), violinA(x,y, length),)
    samples = compute_samples(channels, 44100 * 1)

    write_wavefile('test.wav', samples, 44100 * 1, nchannels=2)
    command = 'aplay ./test.wav'
    os.system(command)


def C(length1, length2):
  return islice(damped_wave(frequency=260.0, amplitude=1, length=int(length1/4)), length2)

def D(length1, length2):
  return islice(damped_wave(frequency=300.0, amplitude=1, length=int(length1/4)), length2)

def E(length1, length2):
  return islice(damped_wave(frequency=340.0, amplitude=1, length=int(length1/4)), length2)

def F(length1, length2):
  return islice(damped_wave(frequency=380.0, amplitude=1, length=int(length1/4)), length2)

def G(length1, length2):
  return islice(damped_wave(frequency=420.0, amplitude=1, length=int(length1/4)), length2)

def A(length1, length2):
  return islice(damped_wave(frequency=460.0, amplitude=1, length=int(length1/4)), length2)

def violin2(x, y, length):
    l = 44100 * length
    amp = map(-90, 90, x, 0.1, 0.01)
    freq = map(-90, 90, y, 900, 50)

    amplitude = 0.1

    return (damped_wave(freq * 1,   amplitude=0.76*amplitude,   length=l),
            damped_wave(freq * 2,   amplitude=0.44*amplitude,   length=l),
            damped_wave(freq * 3,   amplitude=0.32*amplitude,   length=l),
            damped_wave(freq * 8.5, amplitude=0.16*amplitude,   length=l),
            damped_wave(freq * 1.5, amplitude=1.0 *amplitude,   length=l),
            damped_wave(freq * 2.5, amplitude=0.44*amplitude,   length=l),
            damped_wave(freq * 4,   amplitude=0.32*amplitude,   length=l))

def violinG(x, y, length):
    l = 44100 * length
    amp = map(-90, 90, x, 0.1, 0.01)
    freq = map(-90, 90, y, 900, 50)

    amplitude = 0.1

    return (damped_wave(400.0, amplitude=0.76*amplitude, length=l),
            damped_wave(800.0, amplitude=0.44*amplitude, length=l),
            damped_wave(1200.0, amplitude=0.32*amplitude, length=l),
            damped_wave(3400.0, amplitude=0.16*amplitude, length=l),
            damped_wave(600.0, amplitude=1.0*amplitude, length=l),
            damped_wave(1000.0, amplitude=0.44*amplitude, length=l),
            damped_wave(1600.0, amplitude=0.32*amplitude, length=l))


def violin1(x, y, length):
    l = int(44100*length) # each note lasts 0.4 second
    amp = map(-90, 90, x, 0.1, 0.02)
    freq = map(-90, 90, y, 800, 350)
    
    return (damped_wave(frequency=0.8 * freq, framerate=44100, amplitude=0.76*amp, length=l),
                  damped_wave(frequency=1.3 * freq, framerate=44100, amplitude=0.44*amp, length=l),
                  damped_wave(frequency=2.5 * freq, framerate=44100, amplitude=0.32*amp, length=l),
                  damped_wave(frequency=7.0 * freq, framerate=44100, amplitude=0.16*amp, length=l),
                  damped_wave(frequency=1.2 * freq, framerate=44100, amplitude=1.00*amp, length=l),
                  damped_wave(frequency=2.0 * freq, framerate=44100, amplitude=0.44*amp, length=l),
                  damped_wave(frequency=3.2 * freq, framerate=44100, amplitude=0.32*amp, length=l))

def damped(x, y):
    l = int(44100*0.4) # each note lasts 0.4 second

    amp = map(-90, 90, x, 2, 0.2)
    freq = map(-90, 90, y, 850, 320)
    
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

def visualisation(x_angle_filter, y_angle_filter, x_angle_accel, y_angle_accel, x_angle_gyro, y_angle_gyro, z_angle_gyro, cube, cube_accel, cube_gyro, color):
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

def calibrateGyro(rot_gyro_x, rot_gyro_y, rot_gyro_z):
    global gyro_calib_x, gyro_calib_y, gyro_calib_z

    gyro_calib_x += rot_gyro_x
    gyro_calib_y += rot_gyro_y
    gyro_calib_z += rot_gyro_z


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resize(*SCREEN_SIZE)
    init()
    #clock = pygame.time.Clock()
    cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))
    cube_accel = Cube((0.0, 0.0, 0.0), (.5, .5, .7))
    cube_gyro = Cube((0.0, 0.0, 0.0), (.5, .5, .7))

    x_good_angle = 0
    y_good_angle = 0

    x_old_accel = 0
    y_old_accel = 0
    z_old_accel = 0

    i = 0

    musicTimer = time.time()
    frameAcceleration = []
    playNextFrame = False

    while True:
        i += 1

        values = read_values()

        rot_filter_x = float(values[0])
        rot_filter_y = float(values[1])
        rot_accel_x  = float(values[2])
        rot_accel_y  = float(values[3])
        rot_gyro_x   = float(values[4])
        rot_gyro_y   = float(values[5])
        rot_gyro_z   = float(values[6])
        x_accel      = float(values[7])
        y_accel      = float(values[8])
        z_accel      = float(values[9])
        delta_gyro_x   = float(values[10])
        delta_gyro_y   = float(values[11])
        delta_gyro_z   = float(values[12])

        now = time.time()

        #calibrateGyro(delta_gyro_x, delta_gyro_y, delta_gyro_z)
        #print "gyro delta data [" , delta_gyro_x , ", " , delta_gyro_y , ", " , delta_gyro_z , "]"
        #print "average drift: " , i , "  --> [" , gyro_calib_x/i , ", " , rot_gyro_y/i , ", " , rot_gyro_z/i , "]"

        #print values

        #print "accel data [" , x_accel , ", " , y_accel , ", " , z_accel , "]" 
        #print "rotation accel [" , rot_accel_x , ", " , rot_accel_y , "]" 
        #print "rotation gyro [" , rot_gyro_x , ", " , rot_gyro_y , ", " , rot_gyro_z, "]" 
        #print "rotation filter [" , rot_filter_x , ", " , rot_filter_y , "]" 

            

        accelDelta = (abs(x_old_accel) - abs(x_accel)) + (abs(y_old_accel) - abs(y_accel)) + (abs(z_old_accel) - abs(z_accel))
        accelSum = abs(x_accel) + abs(y_accel) + abs(z_accel)
        #print accelSum

        if (playNextFrame):
            length = max(map(7 , 15, accelAccumulation, 0.5, 0.1), 0.1)
            print accelAccumulation , " and length:; ", length
            writeSound(rot_filter_x, rot_filter_y, length)

        playNextFrame = False
        
        if (len(frameAcceleration) < 5):
            frameAcceleration.append(accelSum)
        else:
            frameAcceleration.pop(0)
            frameAcceleration.append(accelSum)

        accelAccumulation = 0
        for accel in frameAcceleration:
            accelAccumulation += accel


        #print accelDelta
        if (accelDelta > 1.0 and accelAccumulation > 6.0): #and now - musicTimer > 0.5
            print "delta: " , accelDelta, "  accelAccumulation: " , accelAccumulation
            playNextFrame = True
            musicTimer = time.time()
        

        visualisation(rot_filter_x, rot_filter_y, rot_accel_x, rot_accel_y, rot_gyro_x, rot_gyro_y, rot_gyro_z, cube, cube_accel, cube_gyro, True)

        x_old_accel = x_accel
        y_old_accel = y_accel
        z_old_accel = z_accel


class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Cube information
    num_faces = 6

    vertices = [ (-0.3, -0.05, 0.5),
                 (0.3, -0.05, 0.5),
                 (0.3, 0.05, 0.5),
                 (-0.3, 0.05, 0.5),
                 (-0.3, -0.05, -0.5),
                 (0.3, -0.05, -0.5),
                 (0.3, 0.05, -0.5),
                 (-0.3, 0.05, -0.5) ]

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

    verticesStick = [ (-0.04, -0.5, 0.04),
                      (0.04, -0.5, 0.04),
                      (0.04, 0.0, 0.04),
                      (-0.04, 0.0, 0.04),
                      (-0.04, -0.5, -0.04),
                      (0.04, -0.5, -0.04),
                      (0.04, 0.0, -0.04),
                      (-0.04, 0.0, -0.04) ]

    def setColor(self, color):
        self.color = color

    def render(self):
        then = pygame.time.get_ticks()
        glColor(self.color)

        vertices = self.vertices
        verticesStick = self.verticesStick

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
        
        # draw cylinder
        glBegin(GL_QUADS)
        for face_no in xrange(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(verticesStick[v1])
            glVertex(verticesStick[v2])
            glVertex(verticesStick[v3])
            glVertex(verticesStick[v4])
        glEnd()

if __name__ == "__main__":
    #print("start GL visualisation")
    run()