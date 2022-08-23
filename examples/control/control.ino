/*!
 * @file control.ino
 * @brief 通过串口命令控制传感器通用适配器板(Sensor Universal Adapter Board)的CSV数据采集，以及屏幕开关。
 * @n 命令1：RECORD ON: 开启CSV记录
 * @n 命令2：RECORD OFF: 关闭CSV记录
 * @n 命令3：OLED OFF: 关闭OLED屏
 * @n 命令4：OLED ON: 开启OLED屏
 *
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Arya](xue.peng@dfrobot.com)
 * @version  V1.0
 * @date  2021-08-11
 * @url https://github.com/DFRobot/DFRobot_RP2040_SUAB
 */
#include "DFRobot_RP2040_SUAB.h"

DFRobot_RP2040_SUAB_IIC suab(/*addr=*/RP2040_SUAB_DEF_I2C_ADDR, &Wire);

void setup() {
  Serial.begin(115200);
  while(!Serial){                                                     //Waiting for USB Serial COM port to open.
  }
  
  Serial.print("Initialization Sensor Universal Adapter Board...");
  while(suab.begin() != 0){
      Serial.println("failed. Please check whether the hardware connection is wrong.");
      delay(1000);
      Serial.print("Initialization Sensor Universal Adapter Board...");
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
  int idx = cmd.indexOf("\r\n");//返回"\r\n"在字符串中第一次出现的位置索引
  if(idx) subCmd = cmd.substring(0, idx);//去掉"\r\n"，并去掉字符串前后的空格
  subCmd.trim();
  subCmd.toUpperCase();
  if(subCmd.equals("RECORD ON")){
    Serial.println("OPEN CSV FILE RECORD!");
    suab.enableRecord();
  }else if(subCmd.equals("RECORD OFF")){
    Serial.println("Close CSV FILE RECORD!");
    suab.disableRecord();
  }else if(subCmd.equals("OLED OFF")){
    Serial.println("TURN OFF OLED DISPLAY!");
    suab.oledScreenOff();
  }else if(subCmd.equals("OLED ON")){
    Serial.println("TURN ON OLED DISPLAY!");
    suab.oledScreenOn();
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
  Serial.println("Input serial command to operate Sensor Universal Adapter Board: ");
  Serial.println("  RECORD ON  - OPEN CSV FILE RECORD!");
  Serial.println("  RECORD OFF - Close CSV FILE RECORD!");
  Serial.println("  OLED ON    - TURN ON OLED DISPLAY!");
  Serial.println("  OLED OFF   - TURN OFF OLED DISPLAY!");
  Serial.println("  HELP       - PRINT ALL COMMAND TIPS!");
  Serial.println();
}
