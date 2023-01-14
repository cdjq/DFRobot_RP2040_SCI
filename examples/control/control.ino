/*!
 * @file control.ino
 * @brief Control the CSV data acquisition and display On/Off of SCI Acquisition Module via serial commands.
 * @n Command 1: RECORD ON: Enable CSV recording
 * @n Command 2: RECORD OFF: Disable CSV recording
 * @n Command 3: OLED OFF: Switch off OLED display
 * @n Command 4: OLED ON: Switch on OLED display
 *
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Arya](xue.peng@dfrobot.com)
 * @version  V1.0
 * @date  2021-08-11
 * @url https://github.com/DFRobot/DFRobot_RP2040_SCI
 */
#include "DFRobot_RP2040_SCI.h"

DFRobot_RP2040_SCI_IIC sci(/*addr=*/RP2040_SCI_ADDR_0X21, &Wire);

void setup() {
  Serial.begin(115200);
  while(!Serial){                                                     //Waiting for USB Serial COM port to open.
  }
  
  Serial.print("Initialization SCI Acquisition Module...");
  while(sci.begin() != 0){
      Serial.println("failed. Please check whether the hardware connection is wrong.");
      delay(1000);
      Serial.print("Initialization SCI Acquisition Module...");
  }
  Serial.println("done.");
  usage();
}

void loop() {
  while(!Serial.available());
  uint8_t i = 0;
  char cmd[11];
  
  while(Serial.available()){
    char c =  Serial.read();
    if(i < 11) cmd[i++] = c;
    delay(2);
  }
  cmd[i] = '\0';
  parseCmd(cmd);
  
}

void parseCmd(char *s){
  String cmd = String(s);
  String subCmd;
  int idx = cmd.indexOf("\r\n");//Return the index to the location where "\r\n" appears in the character string for the first time 
  if(idx) subCmd = cmd.substring(0, idx);//Remove "\r\n" and the spaces before and after the character string
  subCmd.trim();
  subCmd.toUpperCase();
  if(subCmd.equals("RECORD ON")){
    Serial.println("OPEN CSV FILE RECORD!");
    sci.enableRecord();
  }else if(subCmd.equals("RECORD OFF")){
    Serial.println("Close CSV FILE RECORD!");
    sci.disableRecord();
  }else if(subCmd.equals("OLED OFF")){
    Serial.println("TURN OFF OLED DISPLAY!");
    sci.oledScreenOff();
  }else if(subCmd.equals("OLED ON")){
    Serial.println("TURN ON OLED DISPLAY!");
    sci.oledScreenOn();
  }else if(subCmd.equals("HELP")){
    usage();
    return;
  }else{
    Serial.println("INVAILD CMD!");
  }
  Serial.println();
  usage();
}

void usage(){
  Serial.println("Input serial command to operate SCI Acquisition Module: ");
  Serial.println("  RECORD ON  - OPEN CSV FILE RECORD!");
  Serial.println("  RECORD OFF - Close CSV FILE RECORD!");
  Serial.println("  OLED ON    - TURN ON OLED DISPLAY!");
  Serial.println("  OLED OFF   - TURN OFF OLED DISPLAY!");
  Serial.println("  HELP       - PRINT ALL COMMAND TIPS!");
  Serial.println();
}
