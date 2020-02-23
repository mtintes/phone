import time
import digitalio
import board
import adafruit_matrixkeypad
import pyaudiotest2
import pyaudio

# Membrane 3x4 matrix keypad on Raspberry Pi -
# https://www.adafruit.com/product/419
cols = [digitalio.DigitalInOut(x) for x in (board.D16, board.D20, board.D21)]
rows = [digitalio.DigitalInOut(x) for x in (board.D5, board.D6, board.D13, board.D19)]
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

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output = 1)
pyaudiotest2.play_dial_tone(stream,2);
stream.close()
p.terminate()

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

	return True;

while offHook:
	keys = keypad.pressed_keys
	if (not areEqual(keys, lastKeysPressed) and len(keys) > 0):
		print("Pressed: ", keys)
		lastKeysPressed = keys
	elif not hook.value:
		offHook = False;
	elif (len(keys) == 0):
		lastKeysPressed = []
	time.sleep(0.1)
