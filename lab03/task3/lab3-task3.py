#!/usr/bin/env python

# Authors: Hunter Long (mia014) and Ryan Gill (jie134)
# Group 9
# CS-4833-001
# Lab 3 Task 3
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
para = 30
while 1:
        cmdStr = str(cmd) + ' '
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

        if ackResult < 10:
            cmd = 7
            para = 30
        elif ackResult >= 10 and ackResult < 20:
            cmd = 6
            para = 0
        else:
            cmd = 6
            para = 30

        time.sleep(0.01)
