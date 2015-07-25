#!/usr/bin/python

from wavebender import *

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