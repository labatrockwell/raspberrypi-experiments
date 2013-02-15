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

pwm.setPWMFreq(250)                        # Set frequency to 60 Hz
inter = 12
pos_1 = 1024
pos_2 = 2048
cur_actuator = 0
move_to = pos_2

while (True):
  # Change speed of continuous servo on channel O
  print "moving ", cur_actuator, " to ", move_to
  pwm.setPWM(cur_actuator, 0, move_to)
  time.sleep(inter)
  cur_actuator += 1
  cur_actuator %= 5
  if cur_actuator == 0:
    if move_to == pos_2: move_to = pos_1
    else: move_to = pos_2


