# LED Strip
# ---------
# 
# library that controls the LED strips from Adafruit using the 
# SPI bus on a Raspberry Pi.
# 
# The protocol for sending information to the light requires that we 
# send an array with three bytes for each LED on the strip, followed
# by a single latch byte. The latch byte activates the color settings. 
# 
# The LED strip is updated only when the show method is called. The 
# setPixelColor method updates the byte array that holds the state of 
# each led.
# 

class LEDStrip(object):

	# constructor method for the LEDStrip class
	# @param {integer} pixels 	Length of the LED strip in pixels
	# @param {spi} spi 			Link to spi connection
	def __init__(self, pixels = 32, spi = None):
		print '[__init__:LEDStrip] initializing strip with ', pixels, ' pixels.'

		self.pixels = bytearray(pixels * 3 + 1)
		# self.pixels[self.numPixels()] = 0x80
		self.spi = spi

		if self.spi: print '[__init__:LEDStrip] LED Strip successuflly initialized.'
		else: print '[__init__:LEDStrip] ERROR unable to initialize LED Strip.'

	##
	# updateLength 		Updates the length of the LED strip
	# @param {integer} pixels 	Length of the LED strip in pixels
	def updateLength(self, pixels):
		print '[updateLength:LEDStrip] pixels count updated to: ', pixels
		old_pixels = self.pixels
		self.pixels = bytearray(pixels * 3 + 1)

		for i in self.pixels:
			if i < (len(old_pixels) - 1): self.pixels[i] = old_pixels[i]

	##
	# setPixelColor 	Sets the color of a pixel from the LED strip. Note that pixel will not 
	# 					update to new color until `show` method is called.
	# @param {integer} pixel 	Pixel number whose color will be updated
	# @param {integer} color 	Integer that holds a 21-bit color value (MSB is always set to HIGH)
	def setPixelColor(self, pixel, color):
		if (pixel > self.numPixels()) or (pixel < 0): return

		rgb = [hex(color >> i & 0xff) for i in (16,8,0)]
		pixel_loc = pixel * 3
		self.pixels[pixel_loc] = int(rgb[1], 16)
		self.pixels[pixel_loc + 1] = int(rgb[0], 16)
		self.pixels[pixel_loc + 2] = int(rgb[2], 16)

	##
	# setPixelColorRGB 	Sets the color of a pixel from the LED strip. Note that pixel will 
	# 					not update to new color until `show` method is called.
	# @param {integer} pixel 	Pixel number whose color will be updated
	# @param {integer} red 		Integer that holds a 7-bit red color value 
	# @param {integer} green 	Integer that holds a 7-bit green color value 
	# @param {integer} blue 	Integer that holds a 7-bit blue color value 
	def setPixelColorRGB(self, pixel, red, green, blue):
		self.setPixelColor(pixel, self.color(red, green, blue))

	##
	# color 	Returns a 21-bit color value that corresponds to the RGB color
	# @param {integer} red 		Integer that holds a 7-bit red color value 
	# @param {integer} green 	Integer that holds a 7-bit green color value 
	# @param {integer} blue 	Integer that holds a 7-bit blue color value 
	# @returns {integer}		Integer that holds a 21-bit color value (MSB is always set to HIGH)
	def color(self, red, green, blue):
        new_color = int((0x80 | red << 16) | (0x80 | green << 8) | (0x80 | blue))
		return new_color

	##
	# getPixelColor 	Returns a 21-bit color value that corresponds to the specified 
	# 					pixel's RGB color
	# @param {integer} pixel 	Pixel number whose color will be returned
	# @returns {integer}		Integer that holds a 21-bit color value 
	# 							(MSB is always set to HIGH)
	def getPixelColor(self, pixel):
		if (pixel > self.numPixels()) or (pixel < 0): return

		pixel_loc = pixel * 3
		return self.color(self.pixels[pixel_loc], self.pixels[pixel_loc + 1], self.pixels[pixel_loc + 2])

	##
	# getPixelColorRGB 	Returns an array with 7-bit RGB color values that corresponds to 
	# 					this pixel's RGB color
	# @param {integer} pixel 	Pixel number whose color will be returned
	# @returns {array}			Array that holds 7-bit RGB color values
	def getPixelColorRGB(self, pixel):
		if (pixel > self.numPixels()) or (pixel < 0): return

		pixel_loc = pixel * 3
		return [self.pixels[pixel_loc], self.pixels[pixel_loc + 1], self.pixels[pixel_loc + 2]]

	##
	# numPixels 	Returns the length in pixels of the LED strip
	def numPixels(self):
		return ( (len(self.pixels) - 1) / 3 )

	##
	# show 		Updates all pixels on the LED strip to display new colors
	def show(self):
		if self.spi:
			self.spi.write(self.pixels)
			self.spi.flush()
		else:
			print '[show:LEDStrip] ERROR unable to update leds'


if __name__ == "__main__":
	print """
			This is a library for controlling the Adafruit RGB LED strip using the Raspberry Pi.
			Library only supports hardware SPI connections (no bit-bang connections), and only 
			works with the RGB LED String model LPD8806, with 32 leds/meter. 
		"""
	
