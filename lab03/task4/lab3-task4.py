#!/usr/bin/env python

# Authors: Hunter Long (mia014) and Ryan Gill (jie134)
# Group 9
# CS-4833-001
# Lab 3 Task 4
# October 22nd, 2022

#!/usr/bin/python3
from __future__ import print_function
from __future__ import division

import serial
import random

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

try:
    BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
    BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

    color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
    current_color = "none"
    print("BrickPi3 connected and running")
except brickpi3.FirmwareVersionError as error:
    print(error)
except:
    print("Communication with BrickPi3 unsuccessful")

# test communication with Tetrix controller
print("Pi: set up serial port; this will *** RESET *** PRIZM board !!!!")
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# Dakai: init serial port will re-set PRIZM board !!!!
# Dakai: need to start python code on Pi first,
#       and then press GREEN button on PRIZM !!!!
time.sleep(2) # wait for 1 second for reset PRIZM

print ("***************************************************** ")
print("Please press the GREEN button to start PRIZM board !!!!")
print ("***************************************************** ")

#send out data to PRIZM until it reply
cmd = 1
while 1:
        cmdStr = str(cmd)
        cmdStr += '  100'
        print ("Sending out handshaking signal ::" + cmdStr + " to Arduino")
        cmdStr += ' \n'
        ser.write( cmdStr.encode() )
        ser.flush()
        input = ser.readline()
        if input == "":
            print ("Read NOTHING")
        else:
            ackResult = int(input)
            print ("Read input ::"+ str(ackResult) + " from Arduino")
            print (" ************************* \n\n\n\n")
            print (" Get Connected to PRIZM !! ")
            print (" ************************* ")
            input = ser.readline() # eat the extra newline char
            break  # once receive the handshake message, go to next loop           
        cmd= cmd+1
        if cmd == 5:
            cmd = 1
        time.sleep(0.01)

#send out command

# 6 -> move forward, param is power (000 is brake)
# 7 -> move backward, param is power
# 8 -> turn right, param is degrees
# 9 -> turn left, param is degrees
        
cmd = 6
para = 10
last_color = "none"
searching = False
base_time = .5
search_time = base_time
start_time = None
current_direction = 7
done_driving = False
while not done_driving:
        #cmd = random.randint(6,10)
        cmdStr = str(cmd) + ' '
        #para = random.randint(20,30)
        cmdStr += str(para) + ' '        
        print ("Sending out ::"+ cmdStr + " to Arduino")
        
        cmdStr += '\n'  # add newline char
        ser.write( cmdStr.encode() )
        ser.flush()

        #read ack from Arduino as one line
        input = ser.readline()
        ackResult = int(input)
        print ("Read input ::"+ str(ackResult) + " from Arduino")
        input = ser.readline() # eat the extra newline char

        if searching:
            try:
                value = BP.get_sensor(BP.PORT_2)
                current_color = color[value]
                current_time = time.time()
                if current_color != "White":
                    if start_time == None:
                        start_time = current_time
                        cmd = current_direction
                    else:
                        elapsed_time = current_time - start_time 
                        if elapsed_time > search_time:
                            if current_direction == 7:
                                current_direction = 8
                            else:
                                current_direction = 7
                            search_time += base_time
                            start_time = None

                    
                    
                else:
                    searching = False
                    current_time = None
                    cmd = 6
                    para = 0
                    current_direction = 7
                    search_time = base_time

            except brickpi3.SensorError as error:
                print(error)
                
        else:
            
            try:
                value = BP.get_sensor(BP.PORT_2)
                current_color = color[value]
                if current_color == "Red":
                    #first red or stop
                    if last_color == "White":
                        cmd = 6
                        para = 0
                        done_driving = True
                    cmd = 6
                    para = 10
                    last_color = "Red"
                elif current_color == "White":
                    cmd = 6
                    para = 10
                    last_color = "White"
                elif current_color == "Green":
                    cmd = 7
                    para = 0
                    last_color = "Green"
                else:
                    searching = True
                    cmd = 6
                    para = 0
                    last_color = "none"
                

            except brickpi3.SensorError as error:
                print(error)
            
        #cmd += 1
        #if cmd == 10:
        #    cmd = 6

        time.sleep(.25)
