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

#    Define any runtime errors we'll need
#    class ConfigurationError(Exception):

	def __init__(self, p_count = 32, spi = None):
		self.pixels_count = p_count
		self.pixels = bytearray(self.pixels_count * 3 + 1)
		self.spi = {}
		print '[__init__:LEDStrip] creating strip with: ', p_count
		if spi:
#			self.pixels_count = p_count
#			self.pixels = bytearray(self.pixels_count * 3 + 1)		
			self.spi = spi
			print '[__init__:LEDStrip] LED Strip successuflly initialized'
		else:
			print '[__init__:LEDStrip] ERROR unable to initialize LED Strip'


	def updateLength(self, p_count):
		print '[updateLength:LEDStrip] pixels count updated to: ', p_count
		self.pixels_count = p_count
		self.pixels = bytearray(pixels * 3)

	def setPixelColor(self, pixel, color):
		print '[setPixelColor:LEDStrip] updating pixel: ', pixel, " to ", color
		rgb = [hex(color >> i & 0xff) for i in (16,8,0)]
                print '[setPixelColor:LEDStrip] RGB Vals -  r: ', rgb[0], " g: ", rgb[1], " b: ", rgb[2]
		pixel_loc = pixel * 3
		if (pixel_loc + 2) < (self.pixels_count * 3):
			self.pixels[pixel_loc] = int(rgb[1], 16)
			self.pixels[pixel_loc + 1] = int(rgb[0], 16)
			self.pixels[pixel_loc + 2] = int(rgb[2], 16)
			print '[setPixelColor:LEDStrip] update valid starting at pos ', pixel_loc

	def setPixelColorRGB(self, pixel, red, green, blue):
		self.setPixelColor(pixel, self.color(red, green, blue))

	def color(self, red, green, blue):
		new_color = int((0x80 | red << 16) | (0x80 | blue << 8) | (0x80 | blue >> 16))
		print '[color:LEDStrip] color as int: ', new_color
		return new_color

	def show(self):
		print '[show:LEDStrip] show colors'
		self.spi.write(self.pixels)
		self.spi.flush()

		if 'write' in self.spi:
			print '[show:LEDStrip] refreshing the led colors'
			self.spi.write(self.pixels)
			self.spi.flush()
		else:
			print '[show:LEDStrip] ERROR unable to update leds'



if __name__ == "__main__":
    print """
This is a library for the Adafruit RGB LED strip (with 32 leds/meter). 
It was created for use on the Raspberry Pi. 
"""
    
