import sys
sys.path.append("spacebrew-python")
from spacebrew import SpaceBrew
import time

class SbObject:

	def __init__(self, name, varType, value, direction):
		self.varType = varType
		self.value = value
		self.name = name
		self.direction = direction
		self.update = False



class SbLink:

	def __init__(self, clientName, server="localhost"):
		self.__objects = {}
		self.clientName = clientName
		self.server = server

	def start(self):
		print self.clientName, self.server
		self.__brew = SpaceBrew(self.clientName, server=self.server)
		# just expose easier variable
		brew = self.__brew

		for key,obj in self.__objects.iteritems():

			if obj.direction.lower() == "dir_out":
				brew.addPublisher(obj.name, obj.varType)
			elif obj.direction.lower() == "dir_in":
				brew.addSubscriber(obj.name, obj.varType)
				brew.subscribe(obj.name, obj.setter)
			else:
				print "Unknown direction of " , obj.direction

		brew.start()
		# give brew time to connect
		time.sleep(3)

	def add(self, name, varType, value, direction):
		
		obj = SbObject(name, varType, value, direction)
		self.__objects[name] = obj

		def getter():
			#print "calling getter on ", name
			return self.__objects[name].value

		def setter(x):
			#print "calling setter on ", name, " and val ", x
			self.__objects[name].value = x
			if direction.lower() == "dir_out" and self.__brew is not None:
				self.__brew.publish(name, x)
			else:
				self.__objects[name].update = True

		def updateQuery():
			#print "calling update query on ", name
			return self.__objects[name].update

		def updateMarker():
			self.__objects[name].update = False

		getter.__name__ = name
		setter.__name__ = "set" + name[0:1].upper() + name[1:]
		updateQuery.__name__ = name + "Refreshed"
		updateMarker.__name__ = name + "Read"

		setattr(self, getter.__name__, getter)
		setattr(self, setter.__name__, setter)
		setattr(self, updateQuery.__name__, updateQuery)
		setattr(self, updateMarker.__name__, updateMarker)

		obj.setter = setter
		obj.getter = getter
		obj.updateQuery = updateQuery
		obj.updateMarker = updateMarker



	def printAll(self):
		for obj in self.__objects:
			print obj.name
			print getattr(self, obj.name)
			print obj.value


	def stop(self):
		print "Stopping spacebrew link"
		self.__brew.stop()

