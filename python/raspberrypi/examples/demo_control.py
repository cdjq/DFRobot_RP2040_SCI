# -*- coding:utf-8 -*-

'''
  @file demo_control.py
  @brief 通过串口命令控制SCI采集模块(SCI Acquisition Module)的CSV数据采集，以及屏幕开关。
  @n 命令0：RECORD ON: 开启CSV记录
  @n 命令1：RECORD OFF: 关闭CSV记录
  @n 命令2：OLED OFF: 关闭OLED屏
  @n 命令3：OLED ON: 开启OLED屏
  
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
RECORD_ON   = 0
RECORD_OFF  = 1
SCREEN_ON   = 2
SCREEN_OFF  = 3
INVAILD_CMD = 5
if __name__ == "__main__":
  while sci.begin() != 0:
    print("Initialization SCI Acquisition Module failed.")
    time.sleep(1)
  print("Initialization SCI Acquisition Module done.")

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
      sci.enable_record()
    elif num == RECORD_OFF:
      print("Close CSV FILE RECORD!")
      sci.disable_record()
    elif num == SCREEN_ON:
      print("TURN ON OLED DISPLAY!")
      sci.display_on()
    elif num == SCREEN_OFF:
      print("TURN OFF OLED DISPLAY!")
      sci.display_off()
    else:
      print("INVAILD CMD!")
    print("\r\n")