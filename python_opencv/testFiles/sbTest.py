#!/usr/bin/env python

import time
import sys
# project specific spacebrew path
sys.path.append("spacebrew-python")
from spacebrew import SpaceBrew


def updateThreshold(value):
	print "Changing threshold cutoff to: ", int(value)

def updateLearnRate(value):
	print "Changing learning rate to: ", float(value)

def changeConstantUpdates(value):
	print "Changing constant update to: ", bool(value)

def updatePercentageFillTest(value):
	print "Changing percentage fill test to: ", float(value)


brew = SpaceBrew("AreaDetector", server="localhost")

# we publish the percentage of an area that changed
brew.addPublisher("PercentFill")

# we subscribe to all sorts of configuration settings
# 20 default, grayscale difference before we consider a pixel changed
brew.addSubscriber("ThresholdCutoff", "range", 20)
brew.subscribe("ThresholdCutoff", updateThreshold)
# 0.1 default, rate at which the background is learned
brew.addSubscriber("BackgroundLearnRate", "string", "0.1")
brew.subscribe("BackgroundLearnRate", updateLearnRate)
# True default, should we constantly broadcast (True), 
#  or only broadcast when above percentage (False)
brew.addSubscriber("ConstantUpdates", "bool", True)
brew.subscribe("ConstantUpdates", changeConstantUpdates)
# if we are not constant broadcast, after what % change in box do we report
brew.addSubscriber("PercentageFillTest", "string", "0.2")
brew.subscribe("PercentageFillTest", updatePercentageFillTest)


brew.start()

try:
	while True:
		time.sleep(1)
except (KeyboardInterrupt, SystemExit) as e:
	brew.stop()