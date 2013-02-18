from Adafruit_Libs.Adafruit_PWM_Servo_Driver import PWM

class ServoDriver :

	def __init__ (self, address = 0x40, begin = 570, end = 2650, debug = False):
		self.freq = 60
		self.freq_map = (1.0 / self.freq * 1000000.0) / 4096.0
		self.debug = debug

		if begin < 570: begin = 570
		if begin > 2650: begin = 2650
		if end < 570: end = 570
		if end > 2650: end = 2650
		self.begin = begin
		self.end = end
		self.range = self.end - self.begin

		self.calibrations = [{"begin": self.begin, "end": self.end, "range": self.range, "stop": 2048} for x in range(16)]
		self.continuous = [False for x in range(16)]

		self.connect(address)

	def connect (self, address):
		self.address = address
		self.pwm = PWM(self.address, debug = self.debug)
		self.pwm.setPWMFreq(self.freq)

	def continous (self, servo, continuous = True):
		self.continuous[servo] = continuous

	def calibrationTest (self, servo, inc_pos = 25, cur_pos = 1, inc_time = 1):

		print "****************************************************"
		print "Calibration Test "
		print " - starting with pulse length (nanosecs): ", (cur_pos * self.freq_map)
		print " - increment per step (nanosecs): ", (inc_pos * self.freq_map)
		print " - starting pulse length as 12-bit relative pos based on full window: ", cur_pos
		print " "

		self.pwm.setPWM(servo, 0, cur_pos)
		time.sleep(5)

		while cur_pos < 4098 :
			print " - pulse length in nanoseconds: ", (cur_pos * self.freq_map), " 12-bit relative pos: ", cur_pos
			self.pwm.setPWM(servo, 0, cur_pos)
			time.sleep(inc_time)
			cur_pos += inc_pos		

	def calibratePos (self, servo, begin, end):
		self.calibrations[servo]["begin"] = begin
		self.calibrations[servo]["end"] = end
		self.calibrations[servo]["range"] = end - begin

	def calibrateCont (self, servo, stop):
		self.calibrations[servo]["stop"] = stop

	def move (self, servo, pos):
		if self.continuous[servo] == False:
			if pos < 0: degress = 0
			elif pos > 180: degree = 180

			range_mult = self.calibrations[servo]["range"] / 180.0
			new_pos = self.calibrations[servo]["begin"] + (pos * range_mult)
			new_pos = int(new_pos / self.freq_map)

			self.pwm.setPWM(servo, 0, new_pos)

		else:
			self.pwm.setPWM( servo, 0, (self.calibrations[servo]["stop"] + pos) )

if __name__ == "__main__":
	print """
			This is a library for controlling the PCA9685 PWM driver using a Raspberry Pi.
			In order to use this library you need to add the following Adafruit libraries
			to your project directory inside of a folder called Adafruit_Libs:
				* Adafruit_I2C.py 
				* Adafruit_PWM_Servo_Driver.py
		"""