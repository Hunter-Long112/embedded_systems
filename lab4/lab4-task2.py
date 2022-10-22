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

cmd.drive_forward(15)

while True:
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
        
