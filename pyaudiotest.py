#!/usr/bin/env python3 

import pyaudio
import struct
import math

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

def data_for_freq(frequency: float, time: float = None):
	frame_count = int(RATE * time)

	remainder_frames = frame_count% RATE
	wavedata = []

	for i in range(frame_count):
		a = RATE / frequency
		b = i/a
		c = b*(2*math.pi)
		d = math.sin(c)*32767
		e = int(d)
		wavedata.append(e)

	for i in range(remainder_frames):
		wavedata.append(0)

	number_of_bytes = str(len(wavedata))
	wavedata = struct.pack(number_of_bytes + 'h', *wavedata)

	return wavedata

def play(frequency: float, time: float):

	frames = data_for_freq(frequency, time)
	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
	stream.write(frames)
	stream.stop_stream()
	stream.close()

if __name__ == "__main__":
	play(350, 4)
	play(440,4)
	play(480,4)
