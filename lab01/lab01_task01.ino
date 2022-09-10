/************************************************************
 * Authors: Hunter Long (mia014) and Ryan Gill (jie134)
 * Group 9
 * CS-4833-001
 * Lab 1 Task 1
 * September 10th, 2022
 ************************************************************/

#define RIGHT 100
#define LEFT  101

#include <PRIZM.h>
#include <Wire.h>
PRIZM prizm;

void inPlaceTurn(int degree, int direction);

void setup() {
  prizm.PrizmBegin();
  prizm.setMotorInvert(1,1);                
}

void loop() {
    inPlaceTurn(90, LEFT);
    delay(2500);
    inPlaceTurn(90, RIGHT);
    delay(2500);
    
    inPlaceTurn(180, LEFT);
    delay(2500);
    inPlaceTurn(180, RIGHT);
    delay(2500);
    
    inPlaceTurn(270, LEFT);
    delay(2500);
    inPlaceTurn(270, RIGHT);
    delay(2500);
    
    inPlaceTurn(360, LEFT);
    delay(2500);
    inPlaceTurn(360, RIGHT);
    delay(2500);

    delay(10000);
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