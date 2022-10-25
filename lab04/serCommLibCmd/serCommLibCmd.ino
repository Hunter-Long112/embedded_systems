/************************************************************
* Authors: Hunter Long (mia014) and Ryan Gill (jie134)
* Group 9
* CS-4833-001
* Lab 4 Task 1
* November 12th, 2022
*************************************************************/
 
#include <Wire.h>
#include <PRIZM.h>
PRIZM prizm;

#define RIGHT 100
#define LEFT  101

String inputString = "";
boolean stringComplete = false;
int cmd = 0;
int paraOne =0;
int inputIndex =0;
String cmdStr = "";
String paraStr = "";
int cmdStrIndex=0;
int ackValue =0;
String outputString = "";

void setup() {
  Serial.begin(9600);
  
  prizm.PrizmBegin();
  prizm.setMotorInvert(1,1);  
  
  inputString.reserve(200);
  outputString.reserve(200);
  cmdStr.reserve(20);
  paraStr.reserve(20);
}

void loop() {
  if (stringComplete) {
    inputString.trim();
    inputIndex=0;
    while ( inputString.charAt(inputIndex) >= '0' && inputString.charAt(inputIndex) <= '9'  ){
      inputIndex++;
    }
    cmdStr = inputString.substring(0, inputIndex);
    cmd = cmdStr.toInt(); 
    
    paraStr = inputString.substring(inputIndex);
    paraOne = paraStr.toInt();
    
    prizm.setRedLED (LOW);
    prizm.setGreenLED(HIGH);       
    
    switch(cmd){
       case 1:
       case 2:
       case 3:
       case 4:
       case 5: {
          prizm.setRedLED (LOW);
          prizm.setGreenLED(HIGH);        
          ackValue = 100; 
          break;
       }
       //Move Forward - parameter is power to motors, if parameters are 0, this means stop
       case 6: {
          if(paraOne == 0){
            prizm.setMotorPowers(125, 125);
            ackValue = prizm.readSonicSensorCM(3);
            break;
          }
          prizm.setMotorPowers(paraOne, paraOne);
          ackValue = prizm.readSonicSensorCM(3);
          break;
       }
       //Move Backwards - parameter is power to motors
       case 7: {
          prizm.setMotorPowers(-paraOne, -paraOne);
          ackValue = prizm.readSonicSensorCM(3);
          break;  
       }
       //Turn Right - parameter is degree to turn
       case 8:{
          inPlaceTurn(paraOne, RIGHT);
          ackValue = prizm.readSonicSensorCM(3);
          break;
       }
       //Turn Left - parameter is degree to turn
       case 9:{
          inPlaceTurn(paraOne, LEFT);
          ackValue = prizm.readSonicSensorCM(3);
          break;
       }
       default:{
          prizm.setMotorPowers(125, 125);
          ackValue = prizm.readSonicSensorCM(3);
          break;   
       }           
    }
    
    outputString = String(ackValue);
    outputString += " \n";
    Serial.println(outputString);

    inputString = "";
    outputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
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
