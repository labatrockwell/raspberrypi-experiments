#!/usr/bin/env python
import time

from SbLink import SbLink


try:
	link = SbLink()

	link.add("out", "int", 5, "dir_out")
	link.add("out2", "int", 10, "dir_out")

	link.start()
	time.sleep(3)

	counter = 0
	while True:
		link.setOut(counter)
		counter += 1
		time.sleep(3)
		link.setOut2(counter)
		counter += 1
		time.sleep(3)
		print "looped"

except (KeyboardInterrupt, SystemExit) as e:
	print "Got keyboard interrupt"
	link.stop()
except Exception as e:
	link.stop()
	raise
