/************************************************************
* Authors: Hunter Long (mia014) and Ryan Gill (jie134)
* Group 9
* CS-4833-001
* Lab 3 Task 3
* October 22nd, 2022
*************************************************************/
 
#include <Wire.h>    // include the PRIZM library in the sketch
#include <PRIZM.h>    // include the PRIZM library in the sketch
PRIZM prizm;          // instantiate a PRIZM object “prizm” so we can use its functions

#define RIGHT 100
#define LEFT  101

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
int cmd = 0;
int paraOne =0;
int paraTwo =0;
int inputIndex =0;
String cmdStr = "";
String paraStr = "";
int cmdStrIndex=0;

int ackValue =0;
String outputString = "";

void setup() {
  // initialize serial:
  Serial.begin(9600);
  
  prizm.PrizmBegin();
  
  prizm.setMotorInvert(1,1);  
  
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  outputString.reserve(200);
  cmdStr.reserve(20);
  paraStr.reserve(20);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    //at this moment, the single line command is in inputString
    inputString.trim();
    inputIndex=0; //start from beginning
    //get cmd first
    while ( inputString.charAt(inputIndex) >= '0' && inputString.charAt(inputIndex) <= '9'  ){
      inputIndex++;
    }
    cmdStr = inputString.substring(0, inputIndex);
    cmd = cmdStr.toInt(); 
    
    //process the parameter
    paraStr = inputString.substring(inputIndex);
    paraOne = paraStr.toInt();
       
    ackValue = paraOne; //send back first parameter
    
    prizm.setRedLED (LOW);
    prizm.setGreenLED(HIGH);     
    //delay(50);   
    
    switch(cmd){
       case 1:
       case 2:
       case 3:
       case 4:
       case 5: {
          prizm.setRedLED (LOW);
          prizm.setGreenLED(HIGH);     
          //delay(50);   
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
       //Move Backwards - parameter are power to motors
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
    
    //prepare the acknowledge message, end with '\n'
    outputString = String(ackValue);
    outputString += " \n";
    Serial.println(outputString);

    // clear the string for next round:
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

