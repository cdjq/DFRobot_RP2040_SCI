# -*- coding:utf-8 -*-
'''!
  @file demo_get_config_and_data.py
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

  print(sci.set_port1("SEN0161"))
  print(sci.set_port2("NULL"))
  print(sci.set_port3("NULL"))

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
      @param inf Parameters for selecting port
      @n     ePort1                                           Select Port1
      @n     ePort2                                           Select Port2
      @n     ePort3                                           Select Port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
    '''
    sku0  = sci.get_sku(inf = sci.ePort1)
    sku1  = sci.get_sku(inf = sci.ePort2)
    sku2  = sci.get_sku(inf = sci.ePort3)
    info0 = sci.get_information(inf = sci.ePort1)
    info1 = sci.get_information(inf = sci.ePort2)
    info2 = sci.get_information(inf = sci.ePort3)
    print("IF0: SKU-%s DATA-%s"%(sku0, info0))
    print("IF1: SKU-%s DATA-%s"%(sku1, info1))
    print("IF2: SKU-%s DATA-%s"%(sku2, info2))
    print("\r\n")
    time.sleep(1)
