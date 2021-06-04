from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import exceptions
import math
import argparse

def connectMyCopter():
	parser=argparse.ArgumentParser(description='commands')
	parser.add_argument('--connect')
	args=parser.parse_args()
	
	connection_string=args.connect
	
	if not connection_string:
		import dronekit_sitl
		sitl=dronekit_sitl.start_default()
		connection_string=sitl.connection_string()
	
	vehicle=connect(connection_string,wait_ready=True)
	return vehicle

###python connection_template.py --connect 127.0.0.1:14550

########MAIN EXECUTABLE
vehicle=connectMyCopter()

vehicle.wait_ready('autopilot_version')
print('Autopilot version: %s'%vehicle.version)

print('Supports set altitude from companion: %s'%vehicle.capabilities.set_attitude_target_local_ned)

print('Position: %s'%vehicle.location.global_relative_frame)

print('Attitude: %s'%vehicle.attitude)

print('Velocity: %s'%vehicle.velocity)#North (X), East(Y), Down(Z)

print('Last Heartbeat: %s'%vehicle.last_heartbeat)

print('Is the vehicle armable: %s'%vehicle.is_armable)

print('Groundspeead: %s'%vehicle.groundspeed)#This is settable

print('Mode: %s'%vehicle.mode.name)#This is settable

print('Armed: %s'%vehicle.armed)#This is settable

print('EKF Ok: %s'%vehicle.ekf_ok)

vehicle.close()



