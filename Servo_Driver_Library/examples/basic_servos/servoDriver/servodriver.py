from Adafruit_Libs.Adafruit_PWM_Servo_Driver import PWM

class ServoDriver :

	def __init__ (self, address = 0x40, begin = 570, end = 2650, freq = 60, debug = False):
		self.debug = debug

		self.freq = freq
		self.nanosec_res = 1.0 / self.freq * 1000000.0 / 4096.0

		# make sure the begin and end pulse length in nanoseconds is supported with current frequency 
		if begin < self.nanosec_res: begin = self.nanosec_res
		if begin > (self.nanosec_res * 4096): begin = (self.nanosec_res * 4096)
		if end < self.nanosec_res: end = self.nanosec_res
		if end > (self.nanosec_res * 4096): end = (self.nanosec_res * 4096)

		# initialize the configuration array that holds config settings for all servos
		self.configurations = [{"begin": begin, "end": end, "range": (end - begin), "stop": 400, "continuous": False} for x in range(16)]

		self.connect(address)

	def connect (self, address):
		if self.debug: print "[connect:ServoDriver] connecting to the servo driver at i2c address ", address
		self.address = address		
		self.pwm = PWM(self.address, debug = self.debug)
		self.pwm.setPWMFreq(self.freq)

	def continous (self, servo, continuous = True):
		if self.debug: print "[continuous:ServoDriver] setting servo ", servo, " continuous mode to ", continuous
		self.configurations[servo]["continuous"] = continuous

	def calibrationTest (self, servo, start_pulse = 1, inc_pulse = 25, inc_inter = 1):
		if start_pulse < self.nanosec_res: start_pulse = self.nanosec_res
		rel_cur_pulse = start_pulse / self.nanosec_res
		rel_inc_pulse = inc_pulse / self.nanosec_res

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

	def calibratePos (self, servo, begin, end):
		if self.debug: print "[calibratePos:ServoDriver] calibrating servo ", servo, " begin pulse to ", begin, ", and end ", end
		self.configurations[servo]["begin"] = begin
		self.configurations[servo]["end"] = end
		self.configurations[servo]["range"] = end - begin

	def calibrateCont (self, servo, stop):
		if self.debug: print "[calibrateCont:ServoDriver] calibrating continous servo ", servo, " to stop pulse ", stop
		self.configurations[servo]["stop"] = stop

	def move (self, servo, pos):
		if pos < -90: degress = -90
		elif pos > 90: degree = 90
		pos += 90
		
		if self.configurations[servo]["continuous"] == False:
			if self.debug: print "[move:ServoDriver] moving servo ", servo, " to pos ", pos

			range_mult = self.configurations[servo]["range"] / 180.0
			pos = self.configurations[servo]["begin"] + (pos * range_mult)
			pos_int = int(pos / self.nanosec_res)

			self.pwm.setPWM(servo, 0, pos_int)

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