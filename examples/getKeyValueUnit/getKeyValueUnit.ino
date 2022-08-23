/*!
 * @file getKeyValueUnit.ino
 * @brief 获取板子上所有的key，value，unit值
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
 /**
   * @fn getKeys/getValues/getUnits
   * 
   * @param inf    接口选择
   * @n     eAD                                           选中A&D接口
   * @n     eI2C_UART1                                    选中I2C&UART1接口
   * @n     eI2C_UART2                                    选中I2C&UART2接口
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口
   */
  String keys  = suab.getKeys(/*inf =*/suab.eALL);
  String vals  = suab.getValues(/*inf =*/suab.eALL);
  String units = suab.getUnits(/*inf =*/suab.eALL);
  Serial.println("KEYS  : " + keys);
  Serial.println("VALUES: " + vals);
  Serial.println("UNITS : " + units);
  Serial.println();
  delay(1000);
}
