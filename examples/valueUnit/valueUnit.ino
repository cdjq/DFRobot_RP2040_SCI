/*!
 * @file valueUnit.ino
 * @brief 根据SEN0334 温湿度传感器的数据名，获取相应的值和单位
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
  
  suab.setIF1(suab.eI2CMode);
  suab.setIF2(suab.eI2CMode);

  DFRobot_RP2040_SUAB_IIC::eADIFMode_t mode0;
  DFRobot_RP2040_SUAB_IIC::eI2CUARTMode_t mode1, mode2;
  String skuIF0, skuIF1, skuIF2;
  skuIF0 = suab.getIF0Config(&mode0);
  skuIF1 = suab.getIF1Config(&mode1);
  skuIF2 = suab.getIF2Config(&mode2);

  Serial.println("Configuration: ");
  Serial.print("IF0: "); Serial.print("TYPE-" + suab.getSensorModeDescribe(mode0) + ' ');Serial.println(" SKU-" + skuIF0);
  Serial.print("IF1: "); Serial.print("TYPE-" + suab.getSensorModeDescribe(mode1) + ' ');Serial.println(" SKU-" + skuIF1);
  Serial.print("IF2: "); Serial.print("TYPE-" + suab.getSensorModeDescribe(mode2) + ' ');Serial.println(" SKU-" + skuIF2);
  Serial.println();
}

void loop() {
  String Temp_Air_val  = suab.getValue("Temp_Air") + ' ';
  String Temp_Air_unit = suab.getUnit("Temp_Air");
  String Humi_Air_val  = suab.getValue("Humi_Air")+ ' ';
  String Humi_Air_unit = suab.getUnit("Humi_Air");
  Serial.print("Temp_Air: "); Serial.print(Temp_Air_val); Serial.print(Temp_Air_unit);
  Serial.print(" Humi_Air: "); Serial.print(Humi_Air_val); Serial.println(Humi_Air_unit);
  Serial.println();
  delay(1000);
}
