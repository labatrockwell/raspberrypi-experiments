#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)

#stopContinous = 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
inter = 0.3
pos_1 = 100
pos_2 = 150
while (True):
  # Change speed of continuous servo on channel O
  print "start"
  pwm.setPWM(2, 0, 1000)
  counter = 0

  while (counter < 20):
    counter += 1
    pwm.setPWM(1, 0, pos_1)
    time.sleep(inter)
    pwm.setPWM(1, 0, pos_2)
    time.sleep(inter)

  print "stop"
  pwm.setPWM(2, 0, 4096)
  time.sleep(10)



