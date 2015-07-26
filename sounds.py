#!/usr/bin/python

from wavebender import *

def precomputeSound():
    #precompute sound
    soundlength = 0.4
    soundlength_L = 2
    l1 = 44100 * 0.4
    l2 = l1

    toneC   = C(l1, l2)
    channelsC = ((toneC,), (toneC,))
    samplesC = compute_samples(channelsC, 44100 * soundlength)
    write_wavefile('tones/C.wav', samplesC, 44100 * soundlength, nchannels=2)

    toneC_L   = C(12 * l1, 3 * l2)
    channelsC_L = ((toneC_L,), (toneC_L,))
    samplesC_L = compute_samples(channelsC_L, 44100 * soundlength_L)
    write_wavefile('tones/C_L.wav', samplesC_L, 44100 * soundlength_L, nchannels=2)

    toneD   = D(l1, l2)
    channelsD = ((toneD,), (toneD,))
    samplesD = compute_samples(channelsD, 44100 * soundlength)
    write_wavefile('tones/D.wav', samplesD, 44100 * soundlength, nchannels=2)

    toneD_L   = D(12 * l1, 3 * l2)
    channelsD_L = ((toneD_L,), (toneD_L,))
    samplesD_L = compute_samples(channelsD_L, 44100 * soundlength_L)
    write_wavefile('tones/D_L.wav', samplesD_L, 44100 * soundlength_L, nchannels=2)

    toneE   = E(l1, l2)
    channelsE = ((toneE,), (toneE,))
    samplesE = compute_samples(channelsE, 44100 * soundlength)
    write_wavefile('tones/E.wav', samplesE, 44100 * soundlength, nchannels=2)

    toneE_L   = E(12 * l1, 3 * l2)
    channelsE_L = ((toneE_L,), (toneE_L,))
    samplesE_L = compute_samples(channelsE_L, 44100 * soundlength_L)
    write_wavefile('tones/E_L.wav', samplesE_L, 44100 * soundlength_L, nchannels=2)

    toneF   = F(l1, l2)
    channelsF = ((toneF,), (toneF,))
    samplesF = compute_samples(channelsF, 44100 * soundlength)
    write_wavefile('tones/F.wav', samplesF, 44100 * soundlength, nchannels=2)

    toneF_L   = F(12 * l1, 3 * l2)
    channelsF_L = ((toneF_L,), (toneF_L,))
    samplesF_L = compute_samples(channelsF_L, 44100 * soundlength_L)
    write_wavefile('tones/F_L.wav', samplesF_L, 44100 * soundlength_L, nchannels=2)

    toneG   = G(l1, l2)
    channelsG = ((toneG,), (toneG,))
    samplesG = compute_samples(channelsG, 44100 * soundlength)
    write_wavefile('tones/G.wav', samplesG, 44100 * soundlength, nchannels=2)

    toneG_L   = G(12 * l1, 3 * l2)
    channelsG_L = ((toneG_L,), (toneG_L,))
    samplesG_L = compute_samples(channelsG_L, 44100 * soundlength_L)
    write_wavefile('tones/G_L.wav', samplesG_L, 44100 * soundlength_L, nchannels=2)

    toneA   = A(l1, l2)
    channelsA = ((toneA,), (toneA,))
    samplesA = compute_samples(channelsA, 44100 * soundlength)
    write_wavefile('tones/A.wav', samplesA, 44100 * soundlength, nchannels=2)

    toneA_L   = A(12 * l1, 3 * l2)
    channelsA_L = ((toneA_L,), (toneA_L,))
    samplesA_L = compute_samples(channelsA_L, 44100 * soundlength_L)
    write_wavefile('tones/A_L.wav', samplesA_L, 44100 * soundlength_L, nchannels=2)


def C(length1, length2):
  return islice(damped_wave(frequency=180.0, amplitude=1, length=int(length1/4)), length2)

def D(length1, length2):
  return islice(damped_wave(frequency=210.0, amplitude=1, length=int(length1/4)), length2)

def E(length1, length2):
  return islice(damped_wave(frequency=240.0, amplitude=1, length=int(length1/4)), length2)

def F(length1, length2):
  return islice(damped_wave(frequency=270.0, amplitude=1, length=int(length1/4)), length2)

def G(length1, length2):
  return islice(damped_wave(frequency=300.0, amplitude=1, length=int(length1/4)), length2)

def A(length1, length2):
  return islice(damped_wave(frequency=330.0, amplitude=1, length=int(length1/4)), length2)

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