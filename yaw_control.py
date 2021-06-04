from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil

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

def arm_and_takeoff(targetHeight):
	while vehicle.is_armable!=True:
		print("Waiting for the vehicle to become armable")
		time.sleep(1)

	print('Vehicle is now armable')
	vehicle.mode=VehicleMode('GUIDED')

	while vehicle.mode!='GUIDED':
		print("Waitig for drone to enter GUIDED fligt mode")
		time.sleep(1)

	print("Vehicle now in GUIDED MODE. Have fun!!")

	vehicle.armed=True

	while vehicle.armed==False:
		print("Waiting for vehicle to become armed")
		time.sleep(1)

	print("Look out! Virtual props are spinning!!")
	
	vehicle.simple_takeoff(targetHeight)#meters
	while True:
		print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt>=.95*targetHeight:
			break
		time.sleep(1)
	print("Target altitude reached!!")
	return None

def condition_yaw(degrees, relative):
	if relative:
		is_relative=1#yaw relative to direction of travel
	else:
		is_relative=0#yaw is an absolute angle
	#create the CONDITION_YAW command using command_long_encode()
	msg=vehicle.message_factory.command_long_encode(
		0,0,
		mavutil.mavlink.MAV_CMD_CONDITION_YAW,
		0,
		degrees,
		0,
		1,
		is_relative,
		0,0,0)
	vehicle.send_mavlink(msg)
	vehicle.flush()

def dummy_yaw_initializer():
	lat=vehicle.location.global_relative_frame.lat
	lon=vehicle.location.global_relative_frame.lon
	alt=vehicle.location.global_relative_frame.alt
	
	aLocation=LocationGlobalRelative(lat,lon,alt)
	msg=vehicle.message_factory.set_position_target_global_int_encode(
		0,
		0,0,
		mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
		0b0000111111111000,
		aLocation.lat*1e7,
		aLocation.lon*1e7,
		aLocation.alt,
		0,
		0,
		0,
		0,0,0,
		0,0)
	vehicle.send_mavlink(msg)
	vehicle.flush()
###python connection_template.py --connect 127.0.0.1:14550

vehicle=connectMyCopter()
arm_and_takeoff(10)
dummy_yaw_initializer()
time.sleep(2)

condition_yaw(30,1)#30 degrees relative to relative frame 
print("Yawing 30 degrees relative to current position")
time.sleep(7)

print("Yawing True North")
condition_yaw(0,0)#True north
time.sleep(7)

print("Yawing True West")
condition_yaw(270,0)

while True:
	time.sleep(1)
