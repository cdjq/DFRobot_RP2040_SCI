# -*- coding:utf-8 -*-

'''
  @file demo_sensor_data.py
  @brief 获取传感器数据。
  
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

  IF0_list = suab.get_IF0_config()
  IF1_list = suab.get_IF1_config()
  IF2_list = suab.get_IF2_config()

  print("IF0: TYPE-%s SKU-%s"%(suab.get_AD_sensor_mode_describe(IF0_list[suab.INDEX_MODE]), IF0_list[suab.INDEX_SKU]))
  print("IF1: TYPE-%s SKU-%s"%(suab.get_I2CUART_sensor_mode_describe(IF1_list[suab.INDEX_MODE]), IF1_list[suab.INDEX_SKU]))
  print("IF2: TYPE-%s SKU-%s"%(suab.get_I2CUART_sensor_mode_describe(IF2_list[suab.INDEX_MODE]), IF2_list[suab.INDEX_SKU]))
  print("\r\n")

  while True:
    '''!
      @fn get_sku/get_information
      @param inf 指定一个或多个接口参数
      @n     eAD                                           指定A&D接口
      @n     eI2C_UART1                                    指定I2C&UART1接口
      @n     eI2C_UART2                                    选中I2C&UART2接口
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2等所有接口
    '''
    sku   = suab.get_sku(inf = suab.eALL)
    ifAll = suab.get_information(inf = suab.eALL)
    print("SKU: "+ sku)
    print("IF : "+ ifAll)
    print("\r\n")
    time.sleep(1)