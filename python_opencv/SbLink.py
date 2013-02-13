import sys
sys.path.append("spacebrew-python")
from spacebrew import SpaceBrew

class SbLink:

	def __updateThreshold(self, value):
		self.thresholdCutoff = int(value)
		print "Changing threshold cutoff to: ", self.thresholdCutoff

	def __updateLearnRate(self, value):
		self.learnRate = float(value)
		print "Changing learning rate to: ", self.learnRate

	def __changeConstantUpdates(self, value):
		self.constantMessaging = bool(value)
		print "Changing constant update to: ", self.constantMessaging

	def __updatePercentageFillTest(self, value):
		self.percentageFill = float(value)
		print "Changing percentage fill test to: ", self.percentageFill

	def __updateROI(self, value):
		self.ROI = value
		print "Changing percentage fill test to: ", self.ROI


	def __init__(self,
		 	 	 thresholdCutoff = 20, 
				 learnRate = 0.1, 
				 constantMessaging = False,
				 percentageFill = 0.2,
				):


		# variables IN
		self.thresholdCutoff = thresholdCutoff
		self.learnRate = learnRate
		self.constantMessaging = constantMessaging
		self.percentageFill = percentageFill

		self.ROI = None


		self.__brew = SpaceBrew("AreaDetector", server="localhost")
		# just expose easier variable
		brew = self.__brew

		############ PUBLISHERS
		# we publish the percentage of an area that changed
		brew.addPublisher("PercentFill")
		# send out a frame upon request
		brew.addPublisher("Frames")


		############ SUBSCRIBERS
		# grayscale difference before we consider a pixel changed
		brew.addSubscriber("setThresholdCutoff", "range", self.thresholdCutoff)
		brew.subscribe("setThresholdCutoff", self.__updateThreshold)

		# rate at which the background is learned
		brew.addSubscriber("setBackgroundLearnRate", "string", str(self.learnRate))
		brew.subscribe("setBackgroundLearnRate", self.__updateLearnRate)

		# True default, should we constantly broadcast (True), 
		#  or only broadcast when above percentage (False)
		brew.addSubscriber("setConstantUpdates", "bool", self.constantMessaging)
		brew.subscribe("setConstantUpdates", self.__changeConstantUpdates)

		# If we are not constant broadcast, after what % change in box do we report
		brew.addSubscriber("setPercentageFillTest", "string", str(self.percentageFill))
		brew.subscribe("setPercentageFillTest", self.__updatePercentageFillTest)

		# Receive the updated ROI coordinates
		brew.addSubscriber("setROI", "string")
		brew.subscribe("setROI", self.__updateROI)

		brew.start()

	def stop(self):
		print "Stopping spacebrew link"
		self.__brew.stop()

	def publishPercentFill(self):
		pass

	def publishFrames(self, frames):
		self.__brew.publish("Frames", frames)


