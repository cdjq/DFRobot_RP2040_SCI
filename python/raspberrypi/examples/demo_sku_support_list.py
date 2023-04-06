# -*- coding:utf-8 -*-
'''!
  @file demo_sku_support_list.py
  @brief Get the supported sensor list
  
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
  
  while True:
    analog_sku   = sci.get_analog_sensor_sku()
    digital_sku  = sci.get_digital_sensor_sku()
    i2c_sku      = sci.get_i2c_sensor_sku()
    uart_sku     = sci.get_uart_sensor_sku()
    print("Analog  SKU: %s"%analog_sku)
    print("Digital SKU: %s"%digital_sku)
    print("I2C     SKU: %s"%i2c_sku)
    print("UART    SKU: %s"%uart_sku)
    print("\r\n")
    time.sleep(1)
