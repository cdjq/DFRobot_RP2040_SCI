/*!
 * @file valueUnit.ino
 * @brief According to the data name of SEN0334 temperature and humidity sensor, get the corresponding value and unit
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
  Serial.println((char *)"done.");
  
  sci.setPort2((char *)"NULL");
  sci.setPort3((char *)"NULL");
  
  DFRobot_RP2040_SCI_IIC::ePort1IFMode_t mode0 = 0;
  DFRobot_RP2040_SCI_IIC::ePort23Mode_t mode1 = 0, mode2 = 0;
  String skuIF0, skuIF1, skuIF2;
  skuIF0 = sci.getPort1(&mode0);
  skuIF1 = sci.getPort2(&mode1);
  skuIF2 = sci.getPort3(&mode2);

  Serial.println("Configuration: ");
  Serial.print("IF0: "); Serial.print("TYPE-" + sci.getSensorModeDescribe(mode0) + ' ');Serial.println(" SKU-" + skuIF0);
  Serial.print("IF1: "); Serial.print("TYPE-" + sci.getSensorModeDescribe(mode1) + ' ');Serial.println(" SKU-" + skuIF1);
  Serial.print("IF2: "); Serial.print("TYPE-" + sci.getSensorModeDescribe(mode2) + ' ');Serial.println(" SKU-" + skuIF2);
  Serial.println();
}

void loop() {
  String Temp_Air_val  = sci.getValue((char *)"Temp_Air") + ' ';
  String Temp_Air_unit = sci.getUnit((char *)"Temp_Air");
  String Humi_Air_val  = sci.getValue((char *)"Humi_Air")+ ' ';
  String Humi_Air_unit = sci.getUnit((char *)"Humi_Air");
  Serial.print("Temp_Air: "); Serial.print(Temp_Air_val); Serial.print(Temp_Air_unit);
  Serial.print(" Humi_Air: "); Serial.print(Humi_Air_val); Serial.println(Humi_Air_unit);
  Serial.println();
  delay(1000);
}
