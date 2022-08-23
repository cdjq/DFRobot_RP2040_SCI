# -*- coding:utf-8 -*-

'''
  @file demo_get_config_and_data.py
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

  #print(suab.set_IF0_mode(suab.eAnalogMode))
  #print(suab.set_IF0_sku("SEN0161"))
  print(suab.set_IF0_mode_sku(suab.eAnalogMode, "SEN0161"))
  print(suab.set_IF1_mode(suab.eI2CMode))
  print(suab.set_IF1_mode(suab.eI2CMode))

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
    sku0  = suab.get_sku(inf = suab.eAD)
    sku1  = suab.get_sku(inf = suab.eI2C_UART1)
    sku2  = suab.get_sku(inf = suab.eI2C_UART2)
    info0 = suab.get_information(inf = suab.eAD)
    info1 = suab.get_information(inf = suab.eI2C_UART1)
    info2 = suab.get_information(inf = suab.eI2C_UART2)
    print("IF0: SKU-%s DATA-%s"%(sku0, info0))
    print("IF1: SKU-%s DATA-%s"%(sku1, info1))
    print("IF2: SKU-%s DATA-%s"%(sku2, info2))
    print("\r\n")
    time.sleep(1)
