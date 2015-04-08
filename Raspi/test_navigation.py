import sensors
import time
from navigation import *# navigate
from drive import *

output = True # gives output if True

print_log_obj = open('print_log.txt', 'w')

def print_log(message):
	print message
	print_log_obj.write(message)

global current_status
global desired_status 

sens = sensors.sensors(mode=2, start=True)

current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
desired_status = current_status
driving(current_status,desired_status) #init Fahrtregler
time.sleep(2)

#obstacle distance
obstacle = 100 #cm
#direction to goal in degree
reference_direction = 0 #means straight, negative left, positive right!

#x = raw_input("Press enter to start")

#while([x[0] for x in sens.measurements[1]].min() == 0):
#	pass

if output: print_log ( 'While loop starts\n')
while True:
	if output: print_log ("beginn of loop\n__________________________________\n\n")
	if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle: #or sens.measurements[1][0][0] < obstacle/3.0 or sens.measurements[1][-1][0] < obstacle/3.0:
		if output: print_log ( 'potential obstacle found!\n\n')
		desired_status = ['break', 'slow', 'straight']
		driving(current_status,desired_status) #put this here to make reaction to obstacles faster
		time.sleep(1) 	#maybe wait for actual time needed to update all measurements
		if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle:
		#time.sleep(1)
			if output: print_log ( 'real obstacle found!\n\n')
			desired_status = ['break', 'slow', 'straight']
			if output: print_log ( 'steer left 90 after break!\n\n')
			left90(current_status,desired_status)
			time.sleep(.5)
		else:
			if output: print_log ( 'no real obstacle found!\n\n')
			desired_status = ['forward', 'slow', 'straight']
	else:
		steering_direction = navigate(sens.measurements[1],4*obstacle,reference_direction) #steering direction in degree.
		#if steering_direction == reference_direction: #do nothing?
		if output: print_log ( 'berechnete Lenkrichtung: ' + str(steering_direction) + '\n\n')
		if steering_direction == -1:
			desired_status = ['break', 'slow', 'straight']
			if output: print_log ( 'steer right 90, after no free corridor was recognized, after that: stand still for 1 second!\n\n')
			right90(current_status,desired_status)
			time.sleep(.5)
		elif steering_direction > reference_direction: #directons from -90 to 90 degree.
		#steer right
			if output: print_log ( 'steer right for 1 second\n')
			desired_status = ['forward','slow','right']
		elif steering_direction < reference_direction: #0 is on the left side while 10 is right.
		#steer left
			if output: print_log ( 'steer left for 1 second\n')
			desired_status = ['forward','slow','left']
		elif steering_direction == reference_direction:
			if output: print_log ( 'steer straight for 1 second\n')
			desired_status = ['forward', 'slow', 'straight']
		else:
			desired_status = ['break', 'slow', 'straight']
			if output: print_log ( 'deine Mutter hat ein Fehler gemacht, Junge!!! Bleibscht du stehen!\n')
	driving(current_status,desired_status)
	time.sleep(0.5)
	out = str(sens.running) + ": " + str(sens.measurements[0][0]) + ", ("
        for entry in sens.measurements[1]:
                out = out + str(entry[0]) + ", "
	out = out + "), "  + str(sens.measurements[2][0])
	if output: print_log ( out + "\n")
	if output: print_log ( "let it roll a bit, for 1 second.\n")
	desired_status = ['forward', 'null', 'straight']
	driving(current_status,desired_status) 
	time.sleep(0.5)

	



