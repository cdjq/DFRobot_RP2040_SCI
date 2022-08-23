# -*- coding:utf-8 -*-

'''
  @file demo_value_unit.py
  @brief 根据SEN0334 温湿度传感器的数据名，获取相应的值和单位
  
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

  suab.set_IF1_mode(suab.eI2CMode)
  suab.set_IF1_mode(suab.eI2CMode)

  IF0_list = suab.get_IF0_config()
  IF1_list = suab.get_IF1_config()
  IF2_list = suab.get_IF2_config()

  print("IF0: TYPE-%s SKU-%s"%(suab.get_AD_sensor_mode_describe(IF0_list[suab.INDEX_MODE]), IF0_list[suab.INDEX_SKU]))
  print("IF1: TYPE-%s SKU-%s"%(suab.get_I2CUART_sensor_mode_describe(IF1_list[suab.INDEX_MODE]), IF1_list[suab.INDEX_SKU]))
  print("IF2: TYPE-%s SKU-%s"%(suab.get_I2CUART_sensor_mode_describe(IF2_list[suab.INDEX_MODE]), IF2_list[suab.INDEX_SKU]))
  print("\r\n")
  

  while True:
    Temp_Air_val  = suab.get_value0("Temp_Air")
    Temp_Air_unit = suab.get_unit0("Temp_Air")
    Humi_Air_val  = suab.get_value0("Humi_Air")
    Humi_Air_unit = suab.get_unit0("Humi_Air")
    print("Temp_Air:%s %s, Humi_Air:%s %s"%(Temp_Air_val, Temp_Air_unit, Humi_Air_val, Humi_Air_unit))
    print("\r\n")
    time.sleep(1)