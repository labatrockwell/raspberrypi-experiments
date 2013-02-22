# Servo Driver
# -------------
# 
# library that controls the 16-Channel PWM Servo drivers from Adafruit 
# using the i2c bus on a Raspberry Pi. These drivers are based on the
# PCA9685 chip, so it can work on any other board that features these
# PWM chips. 
#  
# This library was designed to work with both normal and continuous 
# rotation servos. 
# 
# @author    	Julio Terra (LAB at Rockwell Group)
# @filename  	servodriver.py
# @version 		0.0.1
# @date 	 	Feb 21, 2013
# 

from Adafruit_Libs.Adafruit_PWM_Servo_Driver import PWM

class ServoDriver:

	##
	# Constructor method for ServoDriver class 
	# @param {integer} address	i2c address of the 16-channel PWM driver
	# @param {integer} begin	Default pulse length in nanosecs to set servo to beginning position 
	# @param {integer} end		Default pulse length in nanosecs to set servo to end position 
	# @param {integer} freq		number of pwn windows per second (frequency), determine max and min pulse length
	# @partm {boolean} debug	flag that turns on and off debug messages 
	def __init__ (self, address = 0x40, begin = 570, end = 2650, freq = 60, debug = False):
		self.debug = debug
		self.freq = freq

		# minimum pulse length in nanoseconds based on freq and 12-bit resolution of PWM driver
		self.nanosec_res = 1.0 / freq * 1000000.0 / 4096.0

		# make sure the begin and end pulse length in nanoseconds is supported with current frequency 
		if begin < self.nanosec_res: begin = self.nanosec_res
		if begin > (self.nanosec_res * 4096): begin = (self.nanosec_res * 4096)
		if end < self.nanosec_res: end = self.nanosec_res
		if end > (self.nanosec_res * 4096): end = (self.nanosec_res * 4096)

		# initialize the configuration array that holds config settings for all servos
		self.configurations = [{"begin": begin, "end": end, "range": (end - begin), "stop": 400, "continuous": False} for x in range(16)]

		# connect to PWM driver at specified i2c address
		self.connect(address)

	##
	# connect 	Method initializes that connects to PWM driver and sets the appropriate PWM frequency
	# @param {integer} address	i2c address of the 16-channel PWM driver
	def connect (self, address):
		if self.debug: print "[connect:ServoDriver] connecting to the servo driver at i2c address ", address
		self.pwm = PWM(address, debug = self.debug)
		self.pwm.setPWMFreq(self.freq)

	##
	# continuous	Method that configures specified servos as continous rotation servos
	# @param {integer} servo 		Number of the servo channel
	# @param {boolean} continuous 	Sets whether the servo at the specified channel should be set to continuous
	def continous (self, servo, continuous = True):
		if self.debug: print "[continuous:ServoDriver] setting servo ", servo, " continuous mode to ", continuous
		self.configurations[servo]["continuous"] = continuous

	##
	# calibrationTest	Method that runs a calibration test designed to enable user to figure out
	# 					the pulse length that sets a specific servo to its beginning and end positions.
	# 					The test consists of changing the pulse length at a specified interval, and 
	# 					printing the current pulse length to the terminal/console.
	# @param {integer} servo 		Number of the servo channel
	# @param {integer} start_pulse	Length in nanosecs of the pulse to start the calibration process. If
	# 								this is set to shorter value than the minimum supported pulse length
	# 								then it is adjusted appropriately.
	# @param {integer} inc_pulse 	Increase in pulse length in nanosec during each step in the 
	# 								calibration process
	# @param {integer} inc_inter 	Interval in seconds between each step in the calibration process. 
	# 
	def calibrationTest (self, servo, start_pulse = 1, inc_pulse = 25, inc_inter = 1):
		# adjust start_pulse if it is shorter than minimum pulse length
		if start_pulse < self.nanosec_res: start_pulse = self.nanosec_res

		# convert starting pulse length, and pulse increment to format required for setting PWM driver
		rel_cur_pulse = int(start_pulse / self.nanosec_res)
		rel_inc_pulse = int(inc_pulse / self.nanosec_res)

		# if the current pulse length is longer than supported by current frequency then abort
		if rel_cur_pulse > 4098: return

		print "*******************************************************************************"
		print "Calibration Test "
		print " - starting with pulse length (nanosecs): ", start_pulse
		print " - increment per step (nanosecs): ", inc_pulse
		print " - starting pulse length as 12-bit relative pos based on full window: ", rel_cur_pulse
		print "--------------------------------------------------------------------------------"

		# send pulse to take servo to starting position
		self.pwm.setPWM(servo, 0, rel_cur_pulse)
		time.sleep(3)

		# increase pulse length until we reach the maximum pulse length
		while rel_cur_pulse < 4098 :
			print " - updated pulse length, nanosecs: ", (rel_cur_pulse * self.nanosec_res), ", 12-bit rel pos: ", rel_cur_pulse
			self.pwm.setPWM(servo, 0, rel_cur_pulse)	# set pulse length
			rel_cur_pulse += rel_inc_pulse				# increase the pulse length				
			time.sleep(inc_inter)						# wait for interval time

	## 
	# calibratePos	Method used to calibrate a normal servo that is attached to the specified channel 
	# 				on the PWM driver
	# @param {integer} servo 	Number of the servo channel
	# @param {integer} begin	Pulse length in nanosecs to set specified servo to beginning position 
	# @param {integer} end		Pulse length in nanosecs to set specified servo to end position 
	def calibratePos (self, servo, begin, end):
		if self.debug: print "[calibratePos:ServoDriver] calibrating servo ", servo, " begin pulse to ", begin, ", and end ", end
		self.configurations[servo]["begin"] = begin
		self.configurations[servo]["end"] = end
		self.configurations[servo]["range"] = end - begin

	## 
	# calibrateCont	Method used to calibrate a continuous rotation servo that is attached to the specified 
	# 				channel on the PWM driver
	# @param {integer} servo 	Number of the servo channel
	# @param {integer} stop		Pulse length in nanosecs to stop the servo from rotating
	def calibrateCont (self, servo, stop):
		if self.debug: print "[calibrateCont:ServoDriver] calibrating continous servo ", servo, " to stop pulse ", stop
		self.configurations[servo]["stop"] = stop

	##
	# move 		Method that updates the position of the specified servo. For normal servos, this method
	# 			enables you to set a specific position; for continuous rotation serovs this method
	# 			enables you to set their rotation direction and speed.
	# @param {integer} servo 	Number of the servo channel
	# @param {integer} pos 		Values between 90 and -90 translate into a position for normal servos,
	# 							For continuous rotation servos 0 will stop their rotation, a higher value
	# 							will rotate it left, and a lower value will rotate it to the right. 
	def move (self, servo, pos):
		if pos < -90: degress = -90
		elif pos > 90: degree = 90
		pos += 90
		
		# handle normal servos
		if self.configurations[servo]["continuous"] == False:
			if self.debug: print "[move:ServoDriver] moving servo ", servo, " to pos ", pos

			range_mult = self.configurations[servo]["range"] / 180.0
			pos = self.configurations[servo]["begin"] + (pos * range_mult)
			pos_int = int(pos / self.nanosec_res)

			self.pwm.setPWM(servo, 0, pos_int)

		# handle continuous servos
		else:
			if self.debug: print "[move:ServoDriver] moving continous servo ", servo, " to ", pos
			pos = pos * (2048 / 90)
			self.pwm.setPWM( servo, 0, (self.configurations[servo]["stop"] + pos) )

if __name__ == "__main__":
	print """
			This is a library for controlling the PCA9685 PWM driver using a Raspberry Pi.
			In order to use this library you need to add the following Adafruit libraries
			to your project directory inside of a folder called Adafruit_Libs:
				* Adafruit_I2C.py 
				* Adafruit_PWM_Servo_Driver.py
		"""