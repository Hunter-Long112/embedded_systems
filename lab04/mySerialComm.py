#!/usr/bin/env python

# Authors: Hunter Long (mia014) and Ryan Gill (jie134)
# Group 9
# CS-4833-001
# Lab 4 Task 1
# November 12th, 2022

from __future__ import print_function
from __future__ import division

import serial
import random

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers


class Commands():


    def __init__(self):

        self.sonic_distance = None
        self.current_command = None
        self.current_param = None
        self.ser = None
        self.BP = None

    def setup_connection(self, baudrate):
        try:
            self.BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
            self.BP.set_sensor_type(self.BP.PORT_2, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)
            print("BrickPi3 connected and running")
        except brickpi3.FirmwareVersionError as error:
            print(error)
        except:
            print("Communication with BrickPi3 unsuccessful")

        # test communication with Tetrix controller
        print("Pi: set up serial port; this will *** RESET *** PRIZM board !!!!")
        self.ser = serial.Serial('/dev/ttyUSB0', baudrate, timeout=1)
        # Dakai: init serial port will re-set PRIZM board !!!!
        # Dakai: need to start python code on Pi first,
        #       and then press GREEN button on PRIZM !!!!
        time.sleep(2) # wait for 1 second for reset PRIZM

    def handshake_prizm(self):
        self.current_command = 1
        while 1:
                cmdStr = str(self.current_command)
                cmdStr += '  100'
                print ("Sending out handshaking signal ::" + cmdStr + " to Arduino")
                cmdStr += ' \n'
                self.ser.write( cmdStr.encode() )
                self.ser.flush()
                input = self.ser.readline()
                if input == "":
                    print ("Read NOTHING")
                else:
                    ackResult = int(input)
                    print ("Read input ::"+ str(ackResult) + " from Arduino")
                    print (" ************************* \n\n\n\n")
                    print (" Get Connected to PRIZM !! ")
                    print (" ************************* ")
                    input = self.ser.readline() # eat the extra newline char
                    break  # once receive the handshake message, go to next loop           
                self.current_command = self.current_command + 1
                if self.current_command == 5:
                    self.current_command = 1
                time.sleep(0.01)

    def execute_command(self):
        cmdStr = str(self.current_command) + ' '
        cmdStr += str(self.current_param) + ' '        
        print ("Sending out ::"+ cmdStr + " to Arduino")
        
        cmdStr += '\n'  # add newline char
        self.ser.write( cmdStr.encode() )
        self.ser.flush()

    def drive_forward(self, speed):
        self.current_command = 6
        self.current_param = speed

    def drive_backward(self, speed):
        self.current_command = 7
        self.current_param = speed

    def brake(self):
        self.current_command = 6
        self.current_command = 0

    def turn_right(self, degree):
        self.current_command = 8
        self.current_param = degree

    def turn_left(self, degree):
        self.current_command = 9
        self.current_param = degree

    def read_sonic_sensor(self):
        input = self.ser.readline()
        ackResult = int(input)
        print ("Read input ::"+ str(ackResult) + " from Arduino")
        input = self.ser.readline() # eat the extra newline char
        self.sonic_distance = ackResult
