import serial
import random
from struct import * 
import time
from spacebrew import SpaceBrew

ser = serial.Serial('/dev/ttyACM0', 9600)

brew1 = SpaceBrew("Pithon Example",server="sandbox.spacebrew.cc")
brew1.addPublisher("pub")
brew1.addSubscriber("light")

# Here's a simple example of a function that recieves a value.
def example(value):
    print "Got",value
    ser.write(pack('B',value/4))
    
# We call "subscribe" to associate a function with a subscriber.
brew1.subscribe("light",example)

brew1.start()

try:
    while True:
        time.sleep(3)
        # The publish method sends a value from the specified
        # publisher.
        brew1.publish('pub','rub')
except (KeyboardInterrupt, SystemExit) as e:
    # Calling stop on a brew disconnects it and waits for its
    # associated thread to finish.
    brew1.stop()


