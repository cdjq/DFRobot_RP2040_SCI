/*!
 * @file valueUnit.ino
 * @brief 获取各类型传感器的支持列表
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
}

void loop() {
  String analogSku   = suab.getAnalogSensorSKU();
  String digitalSku  = suab.getDigitalSensorSKU();
  String i2cSku      = suab.getI2CSensorSKU();
  String uartSku     = suab.getUARTSensorSKU();
  Serial.print("Analog  SKU: "); Serial.println(analogSku);
  Serial.print("Digital SKU: "); Serial.println(digitalSku);
  Serial.print("I2C     SKU: "); Serial.println(i2cSku);
  Serial.print("UART    SKU: "); Serial.println(uartSku); 
  Serial.println();
  delay(1000);
}
