# -*- coding:utf-8 -*-

'''
  @file demo_control.py
  @brief 通过串口命令控制传感器通用适配器板(Sensor Universal Adapter Board)的CSV数据采集，以及屏幕开关。
  @n 命令0：RECORD ON: 开启CSV记录
  @n 命令1：RECORD OFF: 关闭CSV记录
  @n 命令2：OLED OFF: 关闭OLED屏
  @n 命令3：OLED ON: 开启OLED屏
  
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
RECORD_ON   = 0
RECORD_OFF  = 1
SCREEN_ON   = 2
SCREEN_OFF  = 3
INVAILD_CMD = 5
if __name__ == "__main__":
  while suab.begin() != 0:
    print("Initialization Sensor Universal Adapter Board failed.")
    time.sleep(1)
  print("Initialization Sensor Universal Adapter Board done.")

  while True:
    global num
    try:
      num = input("Enter your input number(0: RECORD ON, 1: RECORD OFF, 2: SCREEN ON, 3: SCREEN OFF): ")
    except:
      num = INVAILD_CMD
    if isinstance(num, str):
      num = int(num)
    if num == RECORD_ON:
      print("OPEN CSV FILE RECORD!")
      suab.enable_record()
    elif num == RECORD_OFF:
      print("Close CSV FILE RECORD!")
      suab.disable_record()
    elif num == SCREEN_ON:
      print("TURN ON OLED DISPLAY!")
      suab.display_on()
    elif num == SCREEN_OFF:
      print("TURN OFF OLED DISPLAY!")
      suab.display_off()
    else:
      print("INVAILD CMD!")
    print("\r\n")