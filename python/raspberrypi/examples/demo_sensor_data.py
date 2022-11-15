# -*- coding:utf-8 -*-

'''
  @file demo_sensor_data.py
  @brief 获取传感器数据。
  
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

  sci.set_refresh_rate(sci.eRefreshRate1s)
  rate = sci.get_refresh_rate()
  if rate[0] == sci.ERR_CODE_NONE:
    print("Refresh rate: %d s"%sci.get_refresh_rate_describe(rate[1]))
  version = sci.get_version()
  print("Version: %s"%sci.get_version_description(version))
  
  IF0_list = sci.get_port1()
  IF1_list = sci.get_port2()
  IF2_list = sci.get_port3()

  print("IF0: TYPE-%s SKU-%s"%(sci.get_AD_sensor_mode_describe(IF0_list[sci.INDEX_MODE]), IF0_list[sci.INDEX_SKU]))
  print("IF1: TYPE-%s SKU-%s"%(sci.get_I2CUART_sensor_mode_describe(IF1_list[sci.INDEX_MODE]), IF1_list[sci.INDEX_SKU]))
  print("IF2: TYPE-%s SKU-%s"%(sci.get_I2CUART_sensor_mode_describe(IF2_list[sci.INDEX_MODE]), IF2_list[sci.INDEX_SKU]))
  print("\r\n")

  while True:
    '''!
      @fn get_sku/get_information
      @param inf 指定一个或多个接口参数
      @n     ePort1                                           选中Port1接口
      @n     ePort2                                           选中Port2接口
      @n     ePort3                                           选中Port3接口
      @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
    '''
    sku   = sci.get_sku(inf = sci.eALL)
    ifAll = sci.get_information(inf = sci.eALL, timestamp = True)
    print("SKU: "+ sku)
    print("IF : "+ ifAll)
    print("\r\n")
    time.sleep(1)