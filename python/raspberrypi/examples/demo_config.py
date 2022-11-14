# -*- coding:utf-8 -*-

'''
  @file demo_config.py
  @brief 设置SCI采集模块(SCI Acquisition Module)的I2C地址和时间。
  
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

sci = DFRobot_RP2040_SCI_IIC(addr = DFRobot_SCI.RP2040_SCI_ADDR_0X21)

if __name__ == "__main__":
  while sci.begin() != 0:
    print("Initialization SCI Acquisition Module failed.")
    time.sleep(1)
  print("Initialization SCI Acquisition Module done.")
  
  # 将树莓派的本地时间设置为适配板的时间
  sci.adjust_rtc_datetime()
  #Set the RTC time manually
  #sci.adjust_rtc(2022,8,17,3,12,0,0);  #Set time: 2022/08/17, 星期3, 12:00:00

  print(sci.get_rtc_time())

  addr = sci.get_i2c_address()
  print("Address: 0x%x"%addr)
  
  '''!
    @brief 设置SCI采集模块(SCI Acquisition Module)的I2C通信地址 
    @param addr SCI采集模块(SCI Acquisition Module)的I2C通信地址，支持以下地址设置
    @n RP2040_SCI_ADDR_0X21      0x21 转换板默认I2C地址
    @n RP2040_SCI_ADDR_0X22      0x22
    @n RP2040_SCI_ADDR_0X23      0x23
    @return 错误代码
    @n      ERR_CODE_NONE         or 0x00  设置成功
    @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
    @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
    @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
    @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
    @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配 
    @n      ERR_CODE_I2C_ADRESS   or 0x0A  I2C地址无效
  '''
  err_code = sci.set_i2c_address(sci.RP2040_SCI_ADDR_0X23)
  if(err_code == sci.ERR_CODE_NONE):
    print("Set I2C Address: 0x23......done.Please power down and restart  off SCI Acquisition Module.")
  else:
    print("Set I2C Address: 0x23......failed. Error Code: %d"%err_code)
  