# -*- coding:utf-8 -*-
'''!
  @file demo_control.py
  @brief Control the CSV data acquisition and display On/Off of SCI Acquisition Module via serial commands.
  @n Command 0: RECORD ON: Enable CSV recording 
  @n Command 1: RECORD OFF: Disable CSV recording 
  @n Command 2: OLED OFF: Switch off OLED display
  @n Command 3: OLED ON: Switch on OLED display
  
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
