# -*- coding:utf-8 -*-

'''
  @file demo_sku_support_list.py
  @brief 获取各类型传感器的支持列表
  
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
  
  while True:
    analog_sku   = suab.get_analog_sensor_sku()
    digital_sku  = suab.get_digital_sensor_sku()
    i2c_sku      = suab.get_i2c_sensor_sku()
    uart_sku     = suab.get_uart_sensor_sku()
    print("Analog  SKU: %s"%analog_sku)
    print("Digital SKU: %s"%digital_sku)
    print("I2C     SKU: %s"%i2c_sku)
    print("UART    SKU: %s"%uart_sku)
    print("\r\n")
    time.sleep(1)