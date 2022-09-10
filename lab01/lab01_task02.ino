/************************************************************
 * Authors: Hunter Long (mia014) and Ryan Gill (jie134)
 * Group 9
 * CS-4833-001
 * Lab 1 Task 2
 * September 10th, 2022
 ************************************************************/

#include <PRIZM.h>
#include <Wire.h>

PRIZM prizm;
int distance;

void setup() {
  prizm.PrizmBegin();
  prizm.setMotorInvert(1,1);
  Serial.begin(9600);                      
}

void loop() {
  distance = prizm.readSonicSensorCM(3);
  Serial.print(distance);
  Serial.println(" Centimeters");

  if(distance < 10){
    prizm.setMotorPowers(-30, -30);
  }
  else if(distance >= 10 && distance <= 20){
    prizm.setMotorPowers(125, 125);
  }
  else{
    prizm.setMotorPowers(30, 30);
  }
}