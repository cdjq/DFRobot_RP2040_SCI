# -*- coding:utf-8 -*-

'''
  @file demo_get_key_value_unit.py
  @brief 获取板子上所有的key，value，unit值
  
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

  sci.set_port1("SEN0161")
  sci.set_port2("NULL")
  sci.set_port3("NULL")

  IF0_list = sci.get_port1()
  IF1_list = sci.get_port2()
  IF2_list = sci.get_port3()

  print("IF0: TYPE-%s SKU-%s"%(sci.get_AD_sensor_mode_describe(IF0_list[sci.INDEX_MODE]), IF0_list[sci.INDEX_SKU]))
  print("IF1: TYPE-%s SKU-%s"%(sci.get_I2CUART_sensor_mode_describe(IF1_list[sci.INDEX_MODE]), IF1_list[sci.INDEX_SKU]))
  print("IF2: TYPE-%s SKU-%s"%(sci.get_I2CUART_sensor_mode_describe(IF2_list[sci.INDEX_MODE]), IF2_list[sci.INDEX_SKU]))
  print("\r\n")

  while True:
    '''!
      @fn get_keys/get_values/get_units
      @param inf 指定一个或多个接口参数
      @n     ePort1                                           选中Port1接口
      @n     ePort2                                           选中Port2接口
      @n     ePort3                                           选中Port3接口
      @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
    '''
    keys  = sci.get_keys(inf = sci.eALL)
    vals  = sci.get_values(inf = sci.eALL)
    units = sci.get_units(inf = sci.eALL)
    print("KEYS  : " + keys)
    print("VALUES: " + vals)
    print("UNITS : " + units)
    print("\r\n")
    time.sleep(1)