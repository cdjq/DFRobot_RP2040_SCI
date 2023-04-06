# -*- coding:utf-8 -*-
'''!
  @file demo_value_unit.py
  @brief According to the data name of SEN0334 temperature and humidity sensor, get the corresponding value and unit.
  
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

  sci.set_port1("NULL")
  sci.set_port2("NULL")

  IF0_list = sci.get_port1()
  IF1_list = sci.get_port2()
  IF2_list = sci.get_port3()

  print("IF0: TYPE-%s SKU-%s"%(sci.get_AD_sensor_mode_describe(IF0_list[sci.INDEX_MODE]), IF0_list[sci.INDEX_SKU]))
  print("IF1: TYPE-%s SKU-%s"%(sci.get_I2CUART_sensor_mode_describe(IF1_list[sci.INDEX_MODE]), IF1_list[sci.INDEX_SKU]))
  print("IF2: TYPE-%s SKU-%s"%(sci.get_I2CUART_sensor_mode_describe(IF2_list[sci.INDEX_MODE]), IF2_list[sci.INDEX_SKU]))
  print("\r\n")
  

  while True:
    Temp_Air_val  = sci.get_value0("Temp_Air")
    Temp_Air_unit = sci.get_unit0("Temp_Air")
    Humi_Air_val  = sci.get_value0("Humi_Air")
    Humi_Air_unit = sci.get_unit0("Humi_Air")
    print("Temp_Air1:%s %s, Humi_Air:%s %s"%(Temp_Air_val, Temp_Air_unit, Humi_Air_val, Humi_Air_unit))
    Temp_Air_val  = sci.get_value1(sci.eALL,"Temp_Air")
    Temp_Air_unit = sci.get_unit1(sci.eALL,"Temp_Air")
    Humi_Air_val  = sci.get_value1(sci.eALL,"Humi_Air")
    Humi_Air_unit = sci.get_unit1(sci.eALL,"Humi_Air")
    print("Temp_Air2:%s %s, Humi_Air:%s %s"%(Temp_Air_val, Temp_Air_unit, Humi_Air_val, Humi_Air_unit))
    Temp_Air_val  = sci.get_value2(sci.eALL,"SEN0334","Temp_Air")
    Temp_Air_unit = sci.get_unit2(sci.eALL,"SEN0334","Temp_Air")
    Humi_Air_val  = sci.get_value2(sci.eALL,"SEN0334","Humi_Air")
    Humi_Air_unit = sci.get_unit2(sci.eALL,"SEN0334","Humi_Air")
    print("Temp_Air3:%s %s, Humi_Air:%s %s"%(Temp_Air_val, Temp_Air_unit, Humi_Air_val, Humi_Air_unit))
    print("\r\n\r\n")
    time.sleep(1)
