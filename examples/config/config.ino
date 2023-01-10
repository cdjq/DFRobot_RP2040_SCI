/*!
 * @file config.ino
 * @brief Set the I2C address and time of SCI Acquisition Module
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

  //Set time according to the time for burning
  sci.adjustRtc(F(__DATE__), F(__TIME__)); 
  
  //Set the RTC time manually
  //sci.adjustRtc(2017,6,19,1,12,7,0);  //Set time: 2017/6/19, Monday, 12:07:00
  
  uint8_t addr = sci.getI2CAddress();
  Serial.print("Address: 0x"); Serial.println(addr,HEX);
  Serial.println(sci.getRtcTime());
  
  //Set I2C address as 3
  Serial.print("Set I2C Address: 0x23......");
  /**
   * @fn setI2CAddress
   * @brief Set the I2C address of SCI Acquisition Module
   * 
   * @param addr    I2C address of SCI Acquisition Module, support the following address settings
   * @n RP2040_SCI_ADDR_0X21      0x21 default I2C address
   * @n RP2040_SCI_ADDR_0X22      0x22
   * @n RP2040_SCI_ADDR_0X23      0x23
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller(master) 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or unmatched command 
   * @n      ERR_CODE_I2C_ADRESS   or 0x0A  Invalid I2C address
   */
  uint8_t errCode = sci.setI2CAddress(RP2040_SCI_ADDR_0X23);
  if(errCode == 0){
    Serial.println("done. Please power down and restart  off SCI Acquisition Module.");
  }else{
    Serial.print("failed! Error code: ");Serial.println(errCode);
  }
}

void loop() {
  
}
