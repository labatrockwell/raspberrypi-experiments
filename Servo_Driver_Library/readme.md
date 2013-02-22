LAB Servo Driver Library 
========================

This python library was created to control servo motors using the 16-Channel 12-bit PWM/Servo Drivers from Adafruit. This is an early version of the library that has not been thoroughly tested. More documentation to come soon. In the meantime you can check out the code and example if you want to try out the library. 

References:  
* 16-Channel 12-bit PWM/Servo Driver Product Page on Adafruit - http://www.adafruit.com/products/815  
* Tutorial and Associated Libraries on Adafruit - http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi  
  
@author     Julio Terra (LAB at Rockwell Group)  
@credits    Based on code foundation created by Adafruit  
@date       February 19, 2013  
@version    0.0.1

Example Sketches
================

###Basic Servos
Simple sketch that moves a standard servo back and forward from its starting to end position. It is configured with PWM pulse length that should work with most standard servos.

###Spacebrew Servos
Sketch that enables you to control the movement of two servos via Spacebrew. This sketch registers two subscription inlets in Spacebrew. The first of these accepts a boolean message to control a continuous rotation servo, connected to channel 0. The second accepts a range message that controls a normal servo, connected to channel 2. 

Please note that continuous rotation servos usually require calibration since their stopping point varies considerably between model. I will create calibration example sketch soon to show how to use the calibration features of the Servo Driver Library.

Library Documentation
=====================

###__init__ (self, address = 0x40, begin = 570, end = 2650, freq = 60, debug = False) 
Constructor method for ServoDriver class.

Parameters
* `address` : integer : i2c address of the 16-channel PWM driver
* `begin` : integer : Default pulse length in nanosecs to set servo to beginning position 
* `end` : integer : Default pulse length in nanosecs to set servo to end position 
* `freq` : integer : number of pwn windows per second (frequency), determine max and min pulse length
* `debug` : boolean : flag that turns on and off debug messages 

###connect (self, address)
Method initializes that connects to PWM driver and sets the appropriate PWM frequency

Parameters
* `address` : integer : i2c address of the 16-channel PWM driver

###continous (self, servo, continuous = True):
Method that configures specified servos as continous rotation servos

Parameters
* `servo` : integer : Number of the servo channel
* `continuous` : boolean : Sets whether the servo at the specified channel should be set to continuous

###calibrationTest (self, servo, start_pulse = 1, inc_pulse = 25, inc_inter = 1)
Method that runs a calibration test designed to enable user to figure out the pulse length that sets a specific servo to its beginning and end positions. The test consists of changing the pulse length at a specified interval, and printing the current pulse length to the terminal/console.

Parameters
* `servo` : integer : Number of the servo channel
* `start_pulse` : integer : Length in nanosecs of the pulse to start the calibration process. If this is set to shorter value than the minimum supported pulse length then it is adjusted appropriately.
* `inc_pulse` : integer : Increase in pulse length in nanosec during each step in the calibration process
* `inc_inter` : integer : Interval in seconds between each step in the calibration process.

###calibratePos (self, servo, begin, end)
Method used to calibrate a normal servo that is attached to the specified channel on the PWM driver

Parameter
* `servo` : integer : Number of the servo channel
* `begin` : integer: Pulse length in nanosecs to set specified servo to beginning position 
* `end` : integer : Pulse length in nanosecs to set specified servo to end position 

###calibrateCont (self, servo, stop)
Method used to calibrate a continuous rotation servo that is attached to the specified channel on the PWM driver

Parameter
* `servo` : integer : Number of the servo channel
* `stop` : integer : Pulse length in nanosecs to stop the servo from rotating


###move (self, servo, pos):

Method that updates the position of the specified servo. For normal servos, this method enables you to set a specific position; for continuous rotation serovs this method enables you to set their rotation direction and speed.

Parameter
* `servo` : integer : Number of the servo channel
* `pos` : integer : Values between 90 and -90 translate into a position for normal servos, for continuous rotation servos 0 will stop their rotation, a higher value will rotate it left, and a lower value will rotate it to the right. 


