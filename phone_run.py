#!/usr/bin/env python3

import math
import numpy
import pyaudio
import sys
import digitalio
import board
import adafruit_matrixkeypad
import time

sys.path.append("./toneGenerator.py")

from toneGenerator import ToneGenerator

# Membrane 3x4 matrix keypad on Raspberry Pi -
# https://www.adafruit.com/product/419
cols = [digitalio.DigitalInOut(x) for x in (board.D4, board.D17, board.D27)]
rows = [digitalio.DigitalInOut(x) for x in (board.D5, board.D6, board.D13, board.D25)]
hook = digitalio.DigitalInOut(board.D12)

hook.pull = digitalio.Pull.UP
print(hook.value);

keys = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
lastKeysPressed = []
offHook = True
exitapp = False

phoneNumber = []

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

def play_dial_tone(in_data, frame_count, time_info, status):
        print('dialtone start')
        frames = []
        frames.append(sine_sine_wave(440, 350, 10, 44100))
        chunk = numpy.concatenate(frames)*0.25
        return (chunk.astype(numpy.float32).tostring(), pyaudio.paContinue)


def play_dtmf_tone(stream, digits, length=0.20, rate=44100):
        print("Pressed: *", digits, "*");
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
                # time.sleep(0.2)

def areEqual(arr1, arr2):
	#print("array 1");
	#print("array 2");
	#print(arr1);
	#print(arr2);
	if(len(arr1) != len(arr2)):
		return False;

	arr1.sort();
	arr2.sort();

	for i in range(0, len(arr1)-1):
		if(arr1[i] != arr2[i]):
			return False;


def stopPhone():
        return True

def jenny():
        print("Jenny who can I turn to.")
        return False

def doNothing():
        return False

def numberLookup(phoneNumber):
        number = ''.join([str(elem) for elem in phoneNumber])

        switcher = {
                "1111111": stopPhone,
                "8675309": jenny
        } 

        print("Number", number)
        return switcher.get(number, doNothing)

if __name__ == '__main__':
        generator = ToneGenerator()

        p = pyaudio.PyAudio()
        streamDialtone = generator.play(0, 100.00, 0.50)
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output = 1)

        try:
                while not exitapp:
                        if (len(phoneNumber)==0 and hook.value):
                                streamDialtone.start_stream()
                                # streamDialtone.write(play_dial_tone(stream,1))

                        keys = keypad.pressed_keys
                        if (not areEqual(keys, lastKeysPressed) and len(keys) > 0):
                                try:
                                        streamDialtone.stop_stream()
                                        stream.write(play_dtmf_tone(stream, ''.join([str(elem) for elem in keys])));
                                except:
                                        pass
                                phoneNumber.append(''.join([str(elem) for elem in keys]))
                                print("PhoneNumber", phoneNumber);
                                lastKeysPressed = keys;
                        elif not hook.value:
                                offHook = False;
                                streamDialtone.stop_stream()
                                phoneNumber = []

                        elif (len(keys) == 0):
                                lastKeysPressed = [];

                        if (len(phoneNumber) == 7):
                                play_dtmf_tone(stream, ''.join([str(elem) for elem in phoneNumber]))
                                doThing = numberLookup(phoneNumber)
                                exitapp = doThing()
                                phoneNumber = []
                        time.sleep(0.10)


                        # if(''.join([str(elem) for elem in phoneNumber]) == "1111111"):
                        #         exitapp = True

                # play_dtmf_tone(stream, ''.join([str(elem) for elem in phoneNumber]))
                
                #play_tone(stream);
                # stream.write(play_dial_tone(stream, 5))
        except Exception as error:
                print(error)
        finally:
                streamDialtone.stop_stream()
                streamDialtone.close()
                stream.stop_stream()
                stream.close()
                p.terminate()


