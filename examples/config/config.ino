/*!
 * @file config.ino
 * @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C地址和时间。
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

  //根据烧录时间，设置时间
  suab.adjustRtc(F(__DATE__), F(__TIME__)); 
  
  //Set the RTC time manually
  //suab.adjustRtc(2017,6,19,1,12,7,0);  //Set time: 2017/6/19, Monday, 12:07:00
  
  uint8_t addr = suab.getI2CAddress();
  Serial.print("Address: "); Serial.println(addr);
  Serial.println(suab.getRtcTime());
  
  //将I2C地址设置为3
  Serial.print("Set I2C Address: 3......");
  /**
   * @fn setI2CAddress
   * @brief 设置传感器通用适配器板的I2C通信地址
   * 
   * @param addr    传感器通用适配器板(Sensor Universal Adapter Board)的I2C通信地址，范围1~0x7F
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配 
   * @n      ERR_CODE_I2C_ADRESS   or 0x0A  I2C地址无效
   */
  uint8_t errCode = suab.setI2CAddress(3);
  if(errCode == 0){
    Serial.println("done. Please power down and restart  off Sensor Universal Adapter Board.");
  }else{
    Serial.print("failed! Error code: ");Serial.println(errCode);
  }
}

void loop() {
  
}
