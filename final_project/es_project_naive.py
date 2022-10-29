#!/usr/bin/env python

# Authors: Hunter Long (mia014) and Ryan Gill (jie134)
# Group 9
# CS-4833-001
# Lab 4 Task 2
# November 12th, 2022

from __future__ import print_function
from __future__ import division

import serial
import random

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

import mySerialComm

cmd = mySerialComm.Commands()

cmd.setup_connection(9600)
cmd.handshake_prizm()

start_time = time.time()

cmd.drive_forward(15)

while True:
    if (time.time() - start_time) > 120:
        exit(0)
    cmd.execute_command()
    cmd.read_sonic_sensor()
    if cmd.sonic_distance < 10:
        cmd.brake()
        cmd.execute_command()
        cmd.drive_backward(15)
        while cmd.sonic_distance < 20:
            cmd.execute_command()
            cmd.read_sonic_sensor()
        cmd.brake()
        cmd.execute_command()
        if random.randint(0, 1) == 0:
            cmd.turn_left(random.randint(0, 360))
            cmd.execute_command()
        else:
            cmd.turn_right(random.randint(0, 360))
            cmd.execute_command()
        time.sleep(2)
        cmd.drive_forward(15)
        
    else:
        cmd.drive_forward(15)


# Naive Approach:
# 1. Drive forward until green -> until red -> until yellow
# 	a. if distance read by sonic sensor is less than minimum for collision avoidance:
# 		(retreat procedure)
# 		i. back up until read green -> back up a bit more
# 		ii. turn 90 degrees in one direction 
# 		iii. drive forward a certain distance
# 		iv. turn the inverse of the previous 90 degree turn (point toward the green circle again)
# 2. Once yellow is read in -> until blue, stop
# 	a. if distance read by sonic sensor is less than minimum for collision avoidance or yellow is read in again:
# 		(perform retreat procedure again)