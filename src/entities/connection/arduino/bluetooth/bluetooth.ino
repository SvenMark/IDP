// Basic Bluetooth sketch HC-05_02_38400
// Connect the HC-05 module and communicate using the serial monitor
//
// The HC-05 defaults to commincation mode when first powered on.
// Needs to be placed in to AT mode
// After a factory reset the default baud rate for communication mode is 38400
//
//
//  Pins
//  BT VCC to Arduino 5V out. 
//  BT GND to GND
//  BT RX to Arduino pin 3 (through a voltage divider)
//  BT TX to Arduino pin 2 (no need voltage divider)
//98d3,31,fd1353  98d3,31,fd15c1


 
 
#include <SoftwareSerial.h>
#include <Nextion.h>

SoftwareSerial nextion(5,4);// Nextion TX to pin 2 and RX to pin 3 of Arduino


Nextion myNextion(nextion, 9600); //create a Nextion object named myNextion using the nextion serial port @ 9600bps

boolean button1State;
boolean button2State;
boolean button3State;
boolean button4State;
boolean button5State;
boolean button6State;
boolean button7State;
boolean button8State;
String Data;
int page=0;
unsigned int value_X,value_Y,value_V,value_H;

const int button1 = 3;
const int button2 = 12;
int button_1_activated, button_2_activated;
int deploy,stp;
int mode=0;

long previousMillis = 0; 
long interval = 50;
 
void setup() 
{
    myNextion.init(); // send the initialization commands for Page 0
    // start communication with the HC-05 using 38400
    Serial.begin(38400);  

    pinMode(button1, INPUT);
    pinMode(button2, INPUT);

    
}
 
 
void loop()
{
    String message = myNextion.listen(); //check for message
    unsigned long currentMillis = millis();
    
  if ((digitalRead (button1) == true) && (button_1_activated ==0)){
    if(stp == 1){
      stp = 0;
    }
    else{
      stp = 1;
    }
    button_1_activated = 1;
  }
  
  if (digitalRead (button1) == false){
    button_1_activated = 0;
  }

  if ((digitalRead (button2) == true) && (button_2_activated ==0)){
    if(deploy == 1){
      deploy = 0;
    }
    else{
      deploy = 1;
    }
    button_2_activated = 1;
  }
      
  if (digitalRead (button2) == false){
    button_2_activated = 0;
  }

  if(currentMillis - previousMillis > interval){
    value_V = 1023 - analogRead(8);
    value_H = 1023 - analogRead(9);
    value_X = 1023 - analogRead(0);
    value_Y = 1023 - analogRead(1);

    String finaldata = " s " + String(stp) + " v " + String(value_V) + " h " + String(value_H)+ " d " + String(deploy) + " x " + String(value_X) + " y " + String(value_Y)+ " e " + String(mode);
    Serial.print(finaldata);
    Serial.print("\n");
    delay(20);
  }
            
  if (message == "65 0 1 0 ff ff ff") {
    mode=1;
    myNextion.sendCommand("b0.picc=2"); //set "b0" image to 2
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh    
  }
  
  if (message == "65 0 2 0 ff ff ff") {
    mode=2;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=2"); //set "b1" image to 2
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh
  }

  if (message == "65 0 3 0 ff ff ff") {
    mode=3;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=2"); //set "b2" image to 2
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh
  }

  if (message == "65 0 4 0 ff ff ff") {
    mode=4;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=2"); //set "b3" image to 2
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh
  }

  if (message == "65 0 5 0 ff ff ff") {
    mode=5;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=2"); //set "b4" image to 2
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh
  }

  if (message == "65 0 6 0 ff ff ff") {
    mode=6;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=2"); //set "b5" image to 2
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh
  }

  if (message == "65 0 7 0 ff ff ff") {
    mode=7;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=2"); //set "b6" image to 2
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh
  }

  if (message == "65 0 8 0 ff ff ff") {
    mode=8;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=2"); //set "b7" image to 2
    myNextion.sendCommand("ref b7"); //refresh
  }
  if (message == "65 0 9 0 ff ff ff") {
    mode=0;
    myNextion.sendCommand("b0.picc=0"); //set "b0" image to 0
    myNextion.sendCommand("ref b0"); //refresh
    myNextion.sendCommand("b1.picc=0"); //set "b1" image to 0
    myNextion.sendCommand("ref b1"); //refresh
    myNextion.sendCommand("b2.picc=0"); //set "b2" image to 0
    myNextion.sendCommand("ref b2"); //refresh
    myNextion.sendCommand("b3.picc=0"); //set "b3" image to 0
    myNextion.sendCommand("ref b3"); //refresh
    myNextion.sendCommand("b4.picc=0"); //set "b4" image to 0
    myNextion.sendCommand("ref b4"); //refresh
    myNextion.sendCommand("b5.picc=0"); //set "b5" image to 0
    myNextion.sendCommand("ref b5"); //refresh
    myNextion.sendCommand("b6.picc=0"); //set "b6" image to 0
    myNextion.sendCommand("ref b6"); //refresh
    myNextion.sendCommand("b7.picc=0"); //set "b7" image to 0
    myNextion.sendCommand("ref b7"); //refresh
  }
}
