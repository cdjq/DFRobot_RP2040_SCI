# -*- coding:utf-8 -*-
'''!
  @file demo_config.py
  @brief Set the I2C address and time of SCI Acquisition Module
  
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2021-08-11
  @url https://github.com/DFRobot/DFRobot_RP2040_SCI
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_RP2040_SCI import *

sci = DFRobot_RP2040_SCI_IIC(addr = DFRobot_RP2040_SCI.RP2040_SCI_ADDR_0X21)

if __name__ == "__main__":
  while sci.begin() != 0:
    print("Initialization SCI Acquisition Module failed.")
    time.sleep(1)
  print("Initialization SCI Acquisition Module done.")
  
  # Set the date and time of the SCI Acquisition Module to the current time of Raspberry Pi
  sci.adjust_rtc_datetime()
  #Set the RTC time manually
  #sci.adjust_rtc(2022,8,17,3,12,0,0);  #Set time: 2022/08/17, Wednesday, 12:00:00

  print(sci.get_rtc_time())

  addr = sci.get_i2c_address()
  print("Address: 0x%x"%addr)
  
  '''!
    @brief Set the I2C address of SCI Acquisition Module 
    @param addr I2C address of SCI Acquisition Module, support the following address settings
    @n RP2040_SCI_ADDR_0X21      0x21 default I2C address 
    @n RP2040_SCI_ADDR_0X22      0x22
    @n RP2040_SCI_ADDR_0X23      0x23
    @return Error code
    @n      ERR_CODE_NONE         or 0x00  Set successful
    @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
    @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
    @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller(master) 
    @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
    @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or unmatched command
    @n      ERR_CODE_I2C_ADRESS   or 0x0A  Invalid I2C address
  '''
  err_code = sci.set_i2c_address(sci.RP2040_SCI_ADDR_0X23)
  if(err_code == sci.ERR_CODE_NONE):
    print("Set I2C Address: 0x23......done.Please power down and restart  off SCI Acquisition Module.")
  else:
    print("Set I2C Address: 0x23......failed. Error Code: %d"%err_code)
  
