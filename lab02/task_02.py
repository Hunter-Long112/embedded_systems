#!/usr/bin/env python

# Authors: Hunter Long (mia014) and Ryan Gill (jie134)
# Group 9
# CS-4833-001
# Lab 2 Task 1
# September 24th, 2022

import time
import brickpi3

def listen_for_release():
    while True:
        try:
            value = BP.get_sensor(BP.PORT_1)
            if value == 0:
                break
        except brickpi3.SensorError as error:
            print(error)

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_COLOR_COLOR)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
current_color = "none"
MOTOR_STOP = 0
MOTOR_HALF = 360
MOTOR_FULL = 720
motor_on = False
previous_click_time = 0 
current_click_time = 0

try:
    while True:
        try:
            value = BP.get_sensor(BP.PORT_1)
            print(value)
            if value == 1:
                previous_click_time = current_click_time
                current_click_time = time.time()
                listen_for_release()
                if (current_click_time - previous_click_time) < 0.5:
                    motor_on = False
                else:
                    motor_on = True

            if motor_on:
                try:
                    value = BP.get_sensor(BP.PORT_2)
                    current_color = color[value]
                    if current_color == "Red":
                        BP.set_motor_dps(BP.PORT_A, MOTOR_STOP)
                    elif current_color == "Yellow":
                        BP.set_motor_dps(BP.PORT_A, MOTOR_HALF)
                    else:
                        BP.set_motor_dps(BP.PORT_A, MOTOR_FULL)

                except brickpi3.SensorError as error:
                    print(error)
                    
            else:
                BP.set_motor_dps(BP.PORT_A, 0)
        	
        except brickpi3.SensorError as error:
            print(error)
            
except KeyboardInterrupt: 
    BP.reset_all()        
