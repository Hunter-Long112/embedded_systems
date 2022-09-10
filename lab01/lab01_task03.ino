/************************************************************
 * Authors: Hunter Long (mia014) and Ryan Gill (jie134)
 * Group 9
 * CS-4833-001
 * Lab 1 Task 3
 * September 10th, 2022
 ************************************************************/

#include <PRIZM.h>
#include <Wire.h>

#define RIGHT 100
#define LEFT  101
#define FORWARD 200
#define BACKWARD 201
#define STOP 125

PRIZM prizm;
int distanceInFront;
int distanceBehind;
int middle;
int count = 0;

void inPlaceTurn(int degree, int direction);
void driveUntilStop(int stopDistance, int direction);

void setup() {
  prizm.PrizmBegin();
  prizm.setMotorInvert(1,1);
  Serial.begin(9600);                 
}

void loop() {
  distanceInFront = prizm.readSonicSensorCM(3);
  inPlaceTurn(180, RIGHT);
  brake();
  distanceBehind = prizm.readSonicSensorCM(3);

  middle = (distanceInFront + distanceBehind) / 2;

  if(distanceInFront > distanceBehind){
    driveUntilStop(middle, BACKWARD);
  }
  else if(distanceInFront < distanceBehind){
    driveUntilStop(middle, FORWARD);
  }

  delay(500);
  
  inPlaceTurn(90, RIGHT);
  brake();

  distanceInFront = prizm.readSonicSensorCM(3);
  inPlaceTurn(180, RIGHT);
  brake();
  distanceBehind = prizm.readSonicSensorCM(3);

  middle = (distanceInFront + distanceBehind) / 2;

  if(distanceInFront > distanceBehind){
    driveUntilStop(middle, BACKWARD);
  }
  if(distanceInFront < distanceBehind){
    driveUntilStop(middle, FORWARD);
  }

  count++;
  if (count > 3)
    prizm.PrizmBegin();
}

void inPlaceTurn(int degree, int direction){
  
  int time = map(degree, 0, 360, 0, 3200);
  
  // turn right
  if(direction == RIGHT){
    prizm.setMotorPowers(30, -30);
    delay(time);
    prizm.setMotorPowers(125, 125);
  }
  
  // turn left
  if(direction == LEFT){
    prizm.setMotorPowers(-30, 30);
    delay(time);
    prizm.setMotorPowers(125, 125);
  }
  
}

void driveUntilStop(int stopDistance, int direction){
  if(direction == FORWARD){
    while(prizm.readSonicSensorCM(3) > stopDistance){
      prizm.setMotorPowers(30, 30);
    }
    prizm.setMotorPowers(125, 125);
    return;
  }

  if(direction == BACKWARD){
    while(prizm.readSonicSensorCM(3) < (stopDistance - 30)){
      prizm.setMotorPowers(-30, -30);
    }
    prizm.setMotorPowers(125, 125);
    return;
  }
}

void brake() { 
  prizm.setMotorPowers(STOP, STOP);
  delay(500);
}