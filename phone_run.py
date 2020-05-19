#!/usr/bin/env python3

import math
import numpy
import pyaudio
import sys
import time

def sine_wave(frequency, length, rate):
        length = int(length*rate)
        factor = float(frequency) * (math.pi * 2) /rate
        return numpy.sin(numpy.arange(length) * factor)

def sine_sine_wave(f1, f2, length, rate):
        s1=sine_wave(f1,length,rate)
        s2=sine_wave(f2,length,rate)
        ss=s1+s2
        sa=numpy.divide(ss, 2.0)
        return sa

def play_tone(stream, frequency=440, length = 0.20, rate=44100):
        frames = []
        frames.append(sine_wave(frequency, length, rate))
        chunk = numpy.concatenate(frames)* 0.25

        stream.write(chunk.astype(numpy.float32).tostring())

def play_dial_tone(stream, length=1):
        print('got here')
        frames = []
        frames.append(sine_sine_wave(440, 350, length, 44100))
        chunk = numpy.concatenate(frames)*0.25
        stream.write(chunk.astype(numpy.float32).tostring())


def play_dtmf_tone(stream, digits, length=0.20, rate=44100):
        dtmf_freqs = {'1': (1209,697), '2':(1336,697), '3': (1477,697), 'A': (1633,697), 
                '4': (1209, 770), '5': (1336, 770), '6':(1477,770), 'B':(1633,770),
                '7': (1209,852),'8':(1336,852),'9':(1477,852), 'C': (1633,852),
                '*': (1209,941), '0':(1336,941), '#':(1477,941), 'D':(1633,941)}

        dtmf_digits = ['1', '2', '3', '4','5','6','7','8','9','*','0','#','A','B','C','D']

        if type(digits) is not type(''):
                digits=str(digits)[0]
        digits = ''.join([dd for dd in digits if dd in dtmf_digits])

        for digit in digits:
                digit=digit.upper()
                frames=[]
                frames.append(sine_sine_wave(dtmf_freqs[digit][0], dtmf_freqs[digit][1], length, rate))
                chunk = numpy.concatenate(frames) * 0.25
                stream.write(chunk.astype(numpy.float32).tostring())
                time.sleep(0.2)


if __name__ == '__main__':
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output = 1)
        # play_dtmf_tone(stream, "8675309")
        #play_tone(stream);
        play_dial_tone(stream, 10)
        stream.close()
        p.terminate()
