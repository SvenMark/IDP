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

bool button1State;
bool button2State;
bool button3State;
bool button4State;
bool button5State;
bool button6State;
bool button7State;
bool button8State;
String Data;
int page=0;

int value_X,value_Y,value_V,value_H;

//stp, value_V, value_H, deploy, value_X, value_Y
struct struct_data {
  int stop_motors;
  int vertical;
  int horizontal;
  int deploy;
  int x_axis;
  int y_axis;
};
 

const int button1 = 13;
const int button2 = 3;
int button_1_activated, button_2_activated;
int deploy,stp;
 
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
      if (message == "65 0 1 0 ffff ffff ffff") {
        page=1;
      }
      
      value_V = 1023 - analogRead(A0);
      myNextion.setComponentText("t0", String(value_V));
      
      
      value_H = 1023 - analogRead(A1);
      myNextion.setComponentText("t1", String(value_H));
     

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

      value_X = 1023 - analogRead(A2);
      myNextion.setComponentText("t2", String(value_X));
      
      
      value_Y = 1023 - analogRead(A3);
      myNextion.setComponentText("t3", String(value_Y));
       


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
      
      struct_data data_holder = {
        stp, value_V, value_H, deploy, value_X, value_Y
        };
      int len_struct = sizeof(data_holder);
      
      //String finaldata = " s " + String(stp) + " v " + String(value_V) + " h " + String(value_H)+ " d " + String(deploy) + " x " + String(value_X) + " y " + String(value_Y);
      //Serial.print(finaldata);
      //Serial.print("\n");

      Serial.write('S');
      Serial.write((uint8_t *)&data_holder, len_struct);
      Serial.write('E');
      
    
//    if (page==1){        
      if (message == "65 1 1 0 ffff ffff ffff") {
        myNextion.buttonToggle(button1State, "b0", 0, 2);     
      }
      
      if (message == "65 1 2 0 ffff ffff ffff") {
        myNextion.buttonToggle(button2State, "b1", 0, 2);
      }
  
      if (message == "65 1 3 0 ffff ffff ffff") {
        myNextion.buttonToggle(button3State, "b2", 0, 2);
      }
  
      if (message == "65 1 4 0 ffff ffff ffff") {
        myNextion.buttonToggle(button4State, "b3", 0, 2);
      }
  
      if (message == "65 1 5 0 ffff ffff ffff") {
        myNextion.buttonToggle(button5State, "b4", 0, 2);
      }
  
      if (message == "65 1 6 0 ffff ffff ffff") {
        myNextion.buttonToggle(button6State, "b5", 0, 2);
      }
  
      if (message == "65 1 7 0 ffff ffff ffff") {
        myNextion.buttonToggle(button7State, "b6", 0, 2);
      }
  
      if (message == "65 1 8 0 ffff ffff ffff") {
        myNextion.buttonToggle(button8State, "b7", 0, 2);
      }
      if (message == "65 1 9 0 ffff ffff ffff") {
        page=0;
      }
//    }
    
}
