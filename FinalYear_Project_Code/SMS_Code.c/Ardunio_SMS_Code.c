/*****************************************************************************************************************************************************************************
* Programmer: Jonathan Logue                                                                                                                                                 *
* Date: 18/3/2021                                                                                                                                                            *
* Project: Sligo IT Final Year project - CHLORINE DISINFECTION SYSTEM DATA ANALYSIS & CONTROL                                                                                *
*                                                                                                                                                                            *
* Code Description: Code to be run on an ardunio nano to enable SMS alarm functionality within the project using a sim800c module. The on-site Raspberry                     *
* pi's status & local process alarms will be passed to the real time cloud database & will be monitoredby another raspberry pi located in the office accessing               *
* this database. Should the on-site Pi's heartbeat be lost or any of the process alarms flagged, the office Pi will pick this up & send an output from its defined GPIO pin. *
* this will then be read as an input at the arduino pin & the corresponding hard coded SMS message from that input will be sent out to alert a competent person to the issue.*
*****************************************************************************************************************************************************************************/

// import the serial library to enable serial communication between the sim800c & the arduino
#include <SoftwareSerial.h>


// Configure software serial port to pins 3 & 2 - 3 being the arduino Rx & 2 being the Tx
SoftwareSerial SIM800c(3, 2); 
// declare variables & assign them to digital pins on the arduino 
const int smsTrig1 = 8; // input 1 - Text alarm 1 trigger input
const int smsTrig2 = 9; // input 2 - Text alarm 2 trigger input
const int smsTrig3 = 10;// input 3 - Text alarm 3 trigger input
const int smsTrig4 = 11;// input 4 - Text alarm 4 trigger input
const int ledPin = 12;  // output 1 - Local status indicator - LED turns ON when a SMS function is called - LED then flickers before turning OFF after function has been completed.

int ipState1 = 0; //variable to read input 1 state
int ipState2 = 0; //variable to read input 2 state
int ipState3 = 0; //variable to read input 3 state
int ipState4 = 0; //variable to read input 4 state


void setup() {

  //Configure digital pins I/O status
  pinMode(smsTrig1,INPUT_PULLUP); // smsTrig1 (DI8) set as input_pullup, which means the internal pullup resistors hold the pin to 5v to eliminate a floating pin scenario.
  pinMode(smsTrig2,INPUT_PULLUP); // smsTrig2 (DI9) set as input_pullup, which means the internal pullup resistors hold the pin to 5v to eliminate a floating pin scenario.
  pinMode(smsTrig3,INPUT_PULLUP); // smsTrig3 (DI10) set as input_pullup, which means the internal pullup resistors hold the pin to 5v to eliminate a floating pin scenario.
  pinMode(smsTrig4,INPUT_PULLUP); // smsTrig4 (DI11) set as input_pullup, which means the internal pullup resistors hold the pin to 5v to eliminate a floating pin scenario.
  pinMode(ledPin,OUTPUT); // ledPin (DI12) set as output

  // Arduino communicates with SIM800c GSM shield at a baud rate of 19200
  // Make sure that corresponds to the baud rate of your module
  SIM800c.begin(19200);
  // Sets up comms with serial monitor locally for troubleshooting
  Serial.begin(9600);
  // Give time to your GSM shield log on to network & print status to serial monitor
  Serial.println("</> GSM Module booting & establishing network connection, please wait... </> ");
  delay(15000);   
  Serial.println("</> GSM Module Ready for use </> ");
}  

void loop() { 
  //Read in digital pins states to variables 
  ipState1 = digitalRead(smsTrig1);
  ipState2 = digitalRead(smsTrig2);
  ipState3 = digitalRead(smsTrig3);
  ipState4 = digitalRead(smsTrig4);
  
  //On ipState1 trigger enter function - set LED ON -  Enter sendSMS1 function - wait 3 seconds - Enter flicker function - set LED OFF
  if(ipState1 == HIGH){
    digitalWrite(ledPin, HIGH);
    sendSMS1();
    delay(3000);
    flicker();
    digitalWrite(ledPin, LOW);
  }
  //On ipState2 trigger enter function - set LED ON -  Enter sendSMS2 function - wait 3 seconds - Enter flicker function - set LED OFF
  if(ipState2 == HIGH){
    digitalWrite(ledPin, HIGH);
    sendSMS2();
    delay(3000);
    flicker();
    digitalWrite(ledPin, LOW);
  }
  //On ipState3 trigger enter function - set LED ON -  Enter sendSMS3 function - wait 3 seconds - Enter flicker function - set LED OFF
  if(ipState3 == HIGH){
    digitalWrite(ledPin, HIGH);
    sendSMS3();
    delay(3000);
    flicker();
    digitalWrite(ledPin, LOW);
  }
  //On ipState4 trigger enter function - set LED ON -  Enter sendSMS4 function - wait 3 seconds - Enter flicker function - set LED OFF
  if(ipState4 == HIGH){
    digitalWrite(ledPin, HIGH);
    sendSMS4();
    delay(3000);
    flicker();
    digitalWrite(ledPin, LOW);
  }
}

// Text message no.1 function - loaded AT commands set SIM to SMS mode, set recipients number - Holds hard coded SMS message string - Ends AT Commands
void sendSMS1() {
  Serial.println("</> GSM function 1 process started </>");
  // AT command to set SIM800c to SMS mode
  SIM800c.print("AT+CMGF=1\r"); 
  delay(100);

  // Recipients mobile number in international format
  SIM800c.println("AT+CMGS=\"+353868907923\""); 
  delay(100);
  
  // Hard coded SMS message string
  SIM800c.println("</> On-site raspberry Pi heartbeat_RTU failure, please check local internet connection or device power status. </>"); 
  delay(100);

  // End AT command with a ^Z, ASCII code 26
  SIM800c.println((char)26); 
  delay(100);
  SIM800c.println();
  // Give module time to send SMS
  delay(5000); 
  Serial.println("</> GSM function process finished </>");
}
// Text message no.2 function - loaded AT commands set SIM to SMS mode, set recipients number - Holds hard coded SMS message string - Ends AT Commands
void sendSMS2() {
  Serial.println("</> GSM function 2 process started </>");
  // AT command to set SIM800c to SMS mode
  SIM800c.print("AT+CMGF=1\r"); 
  delay(100);

  // Recipients mobile number in international format
  SIM800c.println("AT+CMGS=\"+353868907923\""); 
  delay(100);
  
  // Hard coded SMS message string
  SIM800c.println("</> ML algorithim SP suggestion outside of +/- 5% tolerance, please verify water characteristics before using suggested Set-point. </>"); 
  delay(100);

  // End AT command with a ^Z, ASCII code 26
  SIM800c.println((char)26); 
  delay(100);
  SIM800c.println();
  // Give module time to send SMS
  delay(5000); 
  Serial.println("</> GSM function process finished </>");
}
// Text message no.3 function - loaded AT commands set SIM to SMS mode, set recipients number - Holds hard coded SMS message string - Ends AT Commands
void sendSMS3() {
  Serial.println("</> GSM function 3 process started </>");
  // AT command to set SIM800c to SMS mode
  SIM800c.print("AT+CMGF=1\r"); 
  delay(100);

  // Recipients mobile number in international format
  SIM800c.println("AT+CMGS=\"+353868907923\""); 
  delay(100);
  
  // Hard coded SMS message string
  SIM800c.println("</> Data harvesting process failed, ML algorithim not in operation at this time, use manual set-point selection, contact Automation rep @ +35386XXXXXXX. </>"); 
  delay(100);

  // End AT command with a ^Z, ASCII code 26
  SIM800c.println((char)26); 
  delay(100);
  SIM800c.println();
  // Give module time to send SMS
  delay(5000); 
  Serial.println("</> GSM function process finished </>");
}
// Text message no.4 function - loaded AT commands set SIM to SMS mode, set recipients number - Holds hard coded SMS message string - Ends AT Commands
void sendSMS4() {
  Serial.println("</> GSM function 4 process started </>");
  // AT command to set SIM800c to SMS mode
  SIM800c.print("AT+CMGF=1\r"); 
  delay(100);

  // Recipients mobile number in international format
  SIM800c.println("AT+CMGS=\"+353868907923\""); 
  delay(100);
  
  // Hard coded SMS message string
  SIM800c.println("</> CL001 Value High limit reached, re-evaluate set-point selection </>"); 
  delay(100);

  // End AT command with a ^Z, ASCII code 26
  SIM800c.println((char)26); 
  delay(100);
  SIM800c.println();
  // Give module time to send SMS
  delay(5000); 
  Serial.println("</> GSM function process finished </>");
}
// Flicker function to pulse led for a period.
void flicker(){
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150);
  digitalWrite(ledPin, LOW);
  delay(150);
  digitalWrite(ledPin, HIGH);
  delay(150); 
}
