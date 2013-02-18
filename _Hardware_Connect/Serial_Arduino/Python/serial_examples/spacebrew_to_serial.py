import serial
import random
from struct import * 
import time
from spacebrew import SpaceBrew

# open serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)

# create spacebrew object and add publish and subscription channels
brew1 = SpaceBrew("Pithon Example",server="sandbox.spacebrew.cc")
brew1.addPublisher("pub")
brew1.addSubscriber("light")

# Here's a simple example of a function that recieves a value.
def forwardToArduino(value):
	print "Got",value
	ser.write(pack('B',value/4))
	
# We call "subscribe" to associate a function with a subscriber
brew1.subscribe("light",forwardToArduino)

# Connect to spacbrew
brew1.start()

try:
	while True:
		# Send a test string to spacbrew every 10 seconds
		brew1.publish('pub','bang')
		time.sleep(10)

except (KeyboardInterrupt, SystemExit) as e:
	# Calling stop on a brew disconnects it and waits for associated thread to finish.
	brew1.stop()

