/*!
 * @file valueUnit.ino
 * @brief Get the supported sensor list
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
}

void loop() {
  String analogSku   = sci.getAnalogSensorSKU();
  String digitalSku  = sci.getDigitalSensorSKU();
  String i2cSku      = sci.getI2CSensorSKU();
  String uartSku     = sci.getUARTSensorSKU();
  Serial.print("Analog  SKU: "); Serial.println(analogSku);
  Serial.print("Digital SKU: "); Serial.println(digitalSku);
  Serial.print("I2C     SKU: "); Serial.println(i2cSku);
  Serial.print("UART    SKU: "); Serial.println(uartSku); 
  Serial.println();
  delay(1000);
}
