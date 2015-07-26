#!/usr/bin/python
from wavebender import *
from sounds import *
from visualisation import *
from cube import *

import urllib
import time
from math import radians
import os

#for gyro calibration
gyro_calib_x = 0
gyro_calib_y = 0
gyro_calib_z = 0

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

    if (length < 8.0):
        l1 = 12 * l1
        l2 = 3  * l2
        soundlength = 2.0


    channels = ((C(l1, l2),), (C(l1, l2),))
    if(freq < 240):
        print "C ---> (freq: " , freq , ", l: " , length,  ")"
    elif(freq < 345):
        channels = ((D(l1, l2),), (D(l1, l2),))
        print "D ---> (freq: " , freq , ", l: " , length,  ")"
    elif(freq < 450):
        channels = ((E(l1, l2),), (E(l1, l2),))
        print "E ---> (freq: " , freq , ", l: " , length,  ")"
    elif(freq < 545):
        channels = ((F(l1, l2),), (F(l1, l2),))
        print "F ---> (freq: " , freq , ", l: " , length,  ")"
    elif(freq < 670):
        channels = ((G(l1, l2),), (G(l1, l2),))
        print "G ---> (freq: " , freq , ", l: " , length,  ")"
    else:
        channels = ((A(l1, l2),), (A(l1, l2),))
        print "A ---> (freq: " , freq , ", l: " , length,  ")"

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

def map(in_min, in_max, x, out_min, out_max):
    return (x - in_min) * (out_max - out_min ) / (in_max - in_min) + out_min;

def calibrateGyro(rot_gyro_x, rot_gyro_y, rot_gyro_z):
    global gyro_calib_x, gyro_calib_y, gyro_calib_z
    gyro_calib_x += rot_gyro_x
    gyro_calib_y += rot_gyro_y
    gyro_calib_z += rot_gyro_z


def run():
    init()

    x_old_accel = 0
    y_old_accel = 0
    z_old_accel = 0

    x_old_filter = 0 
    y_old_filter = 0

    x_old_gyro = 0
    y_old_gyro = 0
    z_old_gyro = 0

    oldAccelAccumulation = 0

    i = 0

    musicTimer = time.time()
    frameAcceleration = []
    playNextFrame = False
    noSoundFrames = 0

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

        #CALIBRATION
        #calibrateGyro(delta_gyro_x, delta_gyro_y, delta_gyro_z)
        #print "gyro delta data [" , delta_gyro_x , ", " , delta_gyro_y , ", " , delta_gyro_z , "]"
        #print "average drift: " , i , "  --> [" , gyro_calib_x/i , ", " , rot_gyro_y/i , ", " , rot_gyro_z/i , "]"


        #print values
        #print "accel data [" , x_accel , ", " , y_accel , ", " , z_accel , "]" 
        #print "rotation accel [" , rot_accel_x , ", " , rot_accel_y , "]" 
        #print "rotation gyro [" , rot_gyro_x , ", " , rot_gyro_y , ", " , rot_gyro_z, "]" 
        #print "rotation filter [" , rot_filter_x , ", " , rot_filter_y , "]" 
        visualisation(rot_filter_x, rot_filter_y, rot_accel_x, rot_accel_y, rot_gyro_x, rot_gyro_y, rot_gyro_z, True)

        rotDelta = abs(abs(x_old_filter) - abs(rot_filter_x)) + abs(abs(y_old_filter) - abs(rot_filter_y))
        accelDeltaTest = abs(abs(x_old_accel) - abs(x_accel)) + abs(abs(y_old_accel) - abs(y_accel)) + abs(abs(z_old_accel) - abs(z_accel))
        accelSum = abs(x_accel) + abs(y_accel) + abs(z_accel)
        gyroSum = abs(abs(x_old_gyro) - abs(rot_gyro_x)) + abs(abs(y_old_gyro) - abs(rot_gyro_y)) + abs(abs(z_old_gyro) - abs(rot_gyro_z))

        #print gyroSum , "  " , accelSum

        if (len(frameAcceleration) < 5):
            frameAcceleration.append(accelSum)
        else:
            frameAcceleration.pop(0)
            frameAcceleration.append(accelSum)

        accelAccumulation = 0
        for accel in frameAcceleration:
            accelAccumulation += accel

        #print oldAccelAccumulation
        if (playNextFrame):
            writeSound(rot_filter_x, rot_filter_y, accelAccumulation)
            noSoundFrames = 0
        else:
            noSoundFrames += 1
        
        playNextFrame = False

        #print noSoundFrames

        accelDelta = (abs(x_old_accel) - abs(x_accel)) + (abs(y_old_accel) - abs(y_accel)) + (abs(z_old_accel) - abs(z_accel))

        #print accelDelta
        #if (noSoundFrames > 1 and accelDelta > 2.10 and accelAccumulation > 2.0): #and now - musicTimer > 0.5
        if (noSoundFrames > 1 and accelDelta > 1.0 and now - musicTimer > 0.4):
            #print "delta: " , accelDelta, "  rotDelta: " , rotDelta
            playNextFrame = True
            musicTimer = time.time()
        

        x_old_accel = x_accel
        y_old_accel = y_accel
        z_old_accel = z_accel

        x_old_gyro = rot_gyro_x
        y_old_gyro = rot_gyro_y
        z_old_gyro = rot_gyro_z

        x_old_filter = rot_filter_x
        y_old_filter = rot_filter_y

        oldAccelAccumulation = accelAccumulation


if __name__ == "__main__":
    #print("start GL visualisation")
    run()