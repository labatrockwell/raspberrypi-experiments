LAB LED Strip Library 
=====================

This python library was created to drive the LED Strips from Adafruit with 32 pixels per meter using the Raspberry Pi (this LED strip uses LPD8806 LED drivers). We structured this library to mimic Adafruit's existing Arduino library, so that it would be easy for anyone to get up and running with it quickly. 

In order to use this library with your Raspberry Pi we recommend that you install Adafruit's Linux distribution, called Occidentalis. This flavor of Linux includes that drivers and configurations you need to use the hardware SPI on your Raspberry Pi - if you are using the standard Linux distribution you will have to get hardware SPI working first.
  
References:    
* LED Strip Product Page on Adafruit - http://adafruit.com/products/306    
* LED Strip Tutorial and Arduino Library on Adafruit - http://learn.adafruit.com/digital-led-strip/  
  
@author     Julio Terra at the LAB at Rockwell Group  
@credits    Based on Library foundation created by Adafruit  
@date       February 19, 2013    
@version    0.0.2  

Library Documentation
=====================

###__init__(self, pixels = 32, spi = None, debug = False)
Constructor for the LED Strip Library that initializes the `self.pixels` byte array, which holds the current state of each RGB led, and assigns the `self.spi` variable a reference to the spi connection. The `self.pixels` array holds three bytes for each led, and an extra latch byte.

Parameters:
* `pixels`: integer : length of the strip in pixels
* `spi`: object : spi connection reference
* `debug`: boolean : turns on info/debug messages

###updateLength(self, pixels)
Updates the length of the LED strip.

Parameters: 
* `pixels`: integer : length of the strip in pixels

###setPixelColor(self, pixel, color)
Sets the color of a pixel from the LED strip. Note that pixel will not update to new color until `show` method is called.

Parameters:
* `pixel`: integer : Pixel number whose color will be updated
* `color`: integer : 21-bit RGB color value. MSB is always set to HIGH.

###setPixelColorRGB(self, pixel, red, green, blue)
Sets the color of the specified pixel. Note that pixel will not update to new color until `show` method is called.

Parameters:
* `pixel`: integer : Pixel number whose color will be updated
* `red` : integer : 7-bit red color value 
* `green` : integer : 7-bit green color value 
* `blue` : integer : 7-bit blue color value 

###color(self, red, green, blue):
Returns a 21-bit color value that corresponds to the specified RGB color

Parameters:
* `red` : integer : 7-bit red color value 
* `green` : integer : 7-bit green color value 
* `blue` : integer : 7-bit blue color value 

###getPixelColor(self, pixel)
Returns a 21-bit color value that corresponds to the specified pixel's RGB color

Parameters
* `pixel`: integer : Pixel number whose color will be returned

###getPixelColorRGB(self, pixel)
Returns an array with 7-bit RGB color values that correspond to the specified pixel's RGB color

Parameters
* `pixel`: integer : Pixel number whose color will be returned

###numPixels(self) 	
Returns the length of the LED strip in pixels/leds

Parameters
* n/a

###show(self)
Updates all pixels on the LED strip to display new colors. Note that the state of all leds are only updated when the show method is called.

Parameters
* n/a


