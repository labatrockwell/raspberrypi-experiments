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

	def __init__(self, pixels = 32, spi = None):
		print '[__init__:LEDStrip] initializing strip with ', pixels, ' pixels.'

		self.pixels_count = pixels
		self.pixels = bytearray(self.pixels_count * 3 + 1)
		self.spi = spi

		if self.spi: print '[__init__:LEDStrip] LED Strip successuflly initialized.'
		else: print '[__init__:LEDStrip] ERROR unable to initialize LED Strip.'


	def updateLength(self, pixels):
		print '[updateLength:LEDStrip] pixels count updated to: ', pixels
		self.pixels_count = pixels
		self.pixels = bytearray(pixels * 3)

	def setPixelColor(self, pixel, color):
		if pixel > len(self.pixels) or pixel < 0: 
			print "[setPixelColor:LEDStrip] pixel number not valid "
			return

		rgb = [hex(color >> i & 0xff) for i in (16,8,0)]
		pixel_loc = pixel * 3
		self.pixels[pixel_loc] = int(rgb[1], 16)
		self.pixels[pixel_loc + 1] = int(rgb[0], 16)
		self.pixels[pixel_loc + 2] = int(rgb[2], 16)

	def setPixelColorRGB(self, pixel, red, green, blue):
		self.setPixelColor(pixel, self.color(red, green, blue))

	def color(self, red, green, blue):
                new_color = int((0x80 | red << 16) | (0x80 | blue << 8) | (0x80 | blue))
		return new_color

	def show(self):
		if self.spi:
			self.spi.write(self.pixels)
			self.spi.flush()
		else:
			print '[show:LEDStrip] ERROR unable to update leds'



if __name__ == "__main__":
	print """
This is a library for the Adafruit RGB LED strip (with 32 leds/meter). 
It was created for use on the Raspberry Pi. 
"""
	
