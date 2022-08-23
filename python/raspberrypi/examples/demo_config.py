# -*- coding:utf-8 -*-

'''
  @file demo_config.py
  @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C地址和时间。
  
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2021-08-11
  @url https://github.com/DFRobot/DFRobot_RP2040_SUAB
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_RP2040_SUAB import *

suab = DFRobot_SUAB_IIC(addr = DFRobot_SUAB.RP2040_SUAB_DEF_I2C_ADDR)

if __name__ == "__main__":
  while suab.begin() != 0:
    print("Initialization Sensor Universal Adapter Board failed.")
    time.sleep(1)
  print("Initialization Sensor Universal Adapter Board done.")
  
  # 将树莓派的本地时间设置为适配板的时间
  suab.adjust_rtc_datetime()
  #Set the RTC time manually
  #suab.adjust_rtc(2022,8,17,3,12,0,0);  #Set time: 2022/08/17, 星期3, 12:00:00

  print(suab.get_rtc_time())

  addr = suab.get_i2c_address()
  print("Address: %d"%addr)
  
  '''!
    @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C通信地址 
    @param addr 传感器通用适配器板(Sensor Universal Adapter Board)的I2C通信地址，范围1~0x7F
    @return 错误代码
    @n      ERR_CODE_NONE         or 0x00  设置成功
    @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
    @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
    @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
    @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
    @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配 
    @n      ERR_CODE_I2C_ADRESS   or 0x0A  I2C地址无效
  '''
  err_code = suab.set_i2c_address(3)
  if(err_code == suab.ERR_CODE_NONE):
    print("Set I2C Address: 3......done.Please power down and restart  off Sensor Universal Adapter Board.")
  else:
    print("Set I2C Address: 3......failed. Error Code: %d"%err_code)
  