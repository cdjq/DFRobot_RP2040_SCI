# -*- coding:utf-8 -*-
'''!
  @file DFRobot_RP2040_SCI.py
  @brief This is an Arduino drive library for the DFRobot SCI Acquisition module. Users can read or set its config and data via I2C. The following demonstrates its detailed functions:
  @n 1. Set or read the I2C address of the module as 0x21, 0x22 or 0x23, the factory default is 0x21, after the I2C address is changed, it will take effect after power-off and reboot;
  @n 2. Set or read the config of Port1, Port2 or Port3:
  @n    Port1: can be configured as analog or digital sensor mode, support NULL, Analog, and analog sensor SKU in analog sensor mode; support digital sensor SKU in digital sensor mode
  @n    Port2: can be configured as I2C or UART sensor mode, support NULL or I2C sensor in I2C sensor mode, in which I2C sensor will be automatically recognized by the module when powered on, and support UART sensor SKU in UART sensor mode
  @n    Port3: can be configured as I2C or UART sensor mode, support NULL or I2C sensor in I2C sensor mode, in which I2C sensor will be automatically recognized by the module when powered on, and support UART sensor SKU in UART sensor mode
  @n 3. Enable/disable data record of CSV file
  @n 4. Switch on/off OLED display
  @n 5. Read the parameters of the sensors connected to the SCI Acquisition module：
  @n      a. Get sensor data "name", separate names by a comma(,);
  @n      b. Get sensor data "value", separate values by a comma(,);
  @n      c. Get sensor data unit, separate units by a comma(,);
  @n      d. Get the SKU of the connected sensor;
  @n      e. Get the complete sensor information in the format of name:value unit, separate multiple pieces of information by a comma(,)
  @n 6. Set and read data refresh rate
  @n 7. Get data refresh timestamp
  @copyright   Copyright (c) 2022 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @maintainer [qsjhyy](yihuan.huang@dfrobot.com)
  @version  V1.0
  @date  2022-07-20
  @url https://github.com/DFRobot/DFRobot_RP2040_SCI
'''
import sys
import smbus
import time
import datetime

class DFRobot_RP2040_SCI:
  ## Default I2C address
  RP2040_SCI_ADDR_0X21        =    0x21
  RP2040_SCI_ADDR_0X22        =    0x22
  RP2040_SCI_ADDR_0X23        =    0x23

  '''enum The port to be set or read'''
  ## Set or read Port1   
  ePort1        =  1 << 0
  ## Set or read Port2 
  ePort2        =  1 << 1 
  ## Set or read Port3  
  ePort3        =  1 << 2
  ## Set or read Port1/2/3 
  eALL          =  0x07

  '''enum A&D port mode select'''
  ## Analog sensor mode  
  eAnalogMode  =  0
  ## Digital sensor mode 
  eDigitalMode =  1

  '''enum  I2C&UART port mode select'''
  ## I2C sensor mode   
  eI2CMode  =  0
  ## UART sensor mode
  eUARTMode =  1  

  '''enum  Set data refresh rate'''
  ## ms-level, refresh at the actual refresh rate
  eRefreshRateMs     = 0
  ## 1s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate1s    = 1   
  ## 3s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate3s     = 2  
  ## 5s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate5s     = 3   
  ## 10s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate10s    = 4   
  ## 30s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate30s    = 5   
  ## 1min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate1min   = 6   
  ## 5min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate5min   = 7   
  ## 10min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
  eRefreshRate10min  = 8   

  ## Set port 0 command, which can be used to configure the function and SKU on A&D ports
  CMD_START   =  0x00
  ## Set port 0 command, which can be used to configure the function and SKU on A&D ports
  CMD_SET_IF0    =   0x00  
  ## Set port 1 command, which can be used to configure the function and SKU on I2C1 & UART1 ports
  CMD_SET_IF1    =   0x01  
  ## Set port 2 command, which can be used to configure the function and SKU on I2C2 & UART2 ports
  CMD_SET_IF2    =   0x02  
  ## Read the function and SKU on port 0
  CMD_READ_IF0   =   0x00  
  ## Read the function and SKU on port 1
  CMD_READ_IF1   =   0x01  
  ## Read the function and SKU on port 2
  CMD_READ_IF2   =   0x02  
  ## Set I2C address (the command will take effect immediately when it's set successfully)
  CMD_SET_ADDR   =   0x03 
  ## Read I2C address (the command will take effect immediately when it's set successfully)
  CMD_READ_ADDR  =   0x03 
  ## Set the time information of year, month, day, hour, minute, second
  CMD_SET_TIME   =   0x04 
  ## Get the time information of year, month, day, hour, minute, second
  CMD_GET_TIME   =   0x04 
  ## Enable CSV recording 
  CMD_RECORD_ON  =   0x05 
  ## Disable CSV recording 
  CMD_RECORD_OFF =   0x06 
  ## Switch on OLED display
  CMD_SCREEN_ON  =   0x07  
  ## Switch off OLED display
  CMD_SCREEN_OFF =   0x08  
  ## Get sensor data name
  CMD_GET_NAME   =   0x09  
  ## Get sensor data value
  CMD_GET_VALUE  =   0x0A  
  ## Get sensor data unit
  CMD_GET_UNIT   =   0x0B  
  ## Get sensor SKU, SKUs are separated by a comma(,)
  CMD_GET_SKU    =   0x0C  
  ## Get the sensor data name, value and unit name, separate value and unit name by space, and others by comma(,)
  CMD_GET_INFO   =   0x0D  
  ## Get the corresponding data value according to the data name
  CMD_GET_KEY_VALUE0  =  0x0E  
  ## Get the corresponding data value according to the data name
  CMD_GET_KEY_VALUE1  =  0x0F
  ## Get the corresponding data value according to the data name  
  CMD_GET_KEY_VALUE2  =  0x10  
  ## Get the corresponding data unit according to the data name
  CMD_GET_KEY_UINT0   =  0x11  
   ## Get the corresponding data unit according to the data name
  CMD_GET_KEY_UINT1   =  0x12 
  ## Get the corresponding data unit according to the data name
  CMD_GET_KEY_UINT2   =  0x13  
  ## Reset I2C peripheral(slave) transmitting cache
  CMD_RESET           =  0x14 
  ## Get the supported Analog sensor SKU 
  CMD_SKU_A           =  0x15  
  ## Get the supported Digital sensor SKU
  CMD_SKU_D           =  0x16  
  ## Get the supported I2C sensor SKU
  CMD_SKU_IIC         =  0x17  
  ## Get the supported UART sensor SKU
  CMD_SKU_UART        =  0x18  
  ## Get timestamp
  CMD_GET_TIMESTAMP     = 0x19  
  ## Set refresh rate
  CMD_SET_REFRESH_TIME  = 0x20  
  ## Get refresh rate
  CMD_GET_REFRESH_TIME  = 0x20  
  CMD_GET_VERSION       = 0x21  ## Get version number

  CMD_END             = CMD_GET_VERSION
  ## Status of successful response   
  STATUS_SUCCESS      = 0x53  
  ## Status of failed response 
  STATUS_FAILED       = 0x63  

  DEBUG_TIMEOUT_MS    = 2 #2s

  ## Normal communication
  ERR_CODE_NONE            =   0x00 
  ## Invalid command
  ERR_CODE_CMD_INVAILED    =   0x01 
  ## Response packet error
  ERR_CODE_RES_PKT         =   0x02 
  ## Insufficient memory of I2C controller(master)
  ERR_CODE_M_NO_SPACE      =   0x03 
  ## Response packet reception timeout
  ERR_CODE_RES_TIMEOUT     =   0x04 
  ## Invalid command packet or unmatched command
  ERR_CODE_CMD_PKT         =   0x05 
  ## Peripheral(slave) fault
  ERR_CODE_SLAVE_BREAK     =   0x06
  ## Set wrong parameters 
  ERR_CODE_ARGS            =   0x07 
  ## The SKU is an invalid SKU or unsupported by SCI Acquisition Module
  ERR_CODE_SKU             =   0x08 
  ## Insufficient memory of I2C peripheral
  ERR_CODE_S_NO_SPACE      =   0x09 
  ## Invalid I2C address
  ERR_CODE_I2C_ADRESS      =   0x0A 

  INDEX_CMD        = 0
  INDEX_ARGS_NUM_L = 1
  INDEX_ARGS_NUM_H = 2
  INDEX_ARGS       = 3

  INDEX_RES_ERR    = 0
  INDEX_RES_STATUS = 1
  INDEX_RES_CMD    = 2
  INDEX_RES_LEN_L  = 3
  INDEX_RES_LEN_H  = 4
  INDEX_RES_DATA   = 5

  INDEX_YEAR     = 0
  INDEX_MONTH    = 1
  INDEX_DAY      = 2
  INDEX_WEEK     = 3
  INDEX_HOUR     = 4
  INDEX_MINUTE   = 5
  INDEX_SECOND   = 6
  INDEX_TIME_STR = 7

  INDEX_ERR_CODE = 0
  INDEX_MODE     = 1
  INDEX_SKU      = 2

  SKU_MAX_VAILD_LEN = 7
  
  def __init__(self):
    pass
  
  def begin(self):
    '''!
      @brief Initalize the SCI Acquisition Module, mainly for initializing communication interface
      @return int Init status
      @n       0      Init successful
      @n      others  Init failed
    '''
    self._reset(self.CMD_RESET)
    return 0
  
  def get_version(self):
    '''!
      @brief Get firmware version number of SCI Acquisition Module
      @n The version number is 16-bit data, the high 8bits(b15-b9) represent the leftmost number
      @n The middle 4bits (b8-b4) represent the middle number 
      @n The low 4bits represent the rightmost number
      @n For example, 0x0123 corresponds to V1.2.3
      @n     Digital sensor SKU, means selecting the SKU of a digital sensor and configuring to digital sensor mode
      @return 16-bit version data
    '''
    rslt = [0,0,"NULL"]
    version = 0
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_VERSION
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_VERSION)
    rslt[self.INDEX_ERR_CODE] = recv_pkt[self.INDEX_RES_ERR]
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length == 2:
        version = ((recv_pkt[self.INDEX_RES_DATA] << 8) | recv_pkt[self.INDEX_RES_DATA + 1]) & 0xFFFF
    return version
  
  def get_version_description(self, version):
    '''!
      @brief Get version description char string
      @return Return version description char string, e.g. id：0x0123 The returned version decription char string is V1.2.3
    '''
    ver_str = "V"
    ver_str += str((version >> 8) & 0xFF)
    ver_str += '.'
    ver_str += str((version >> 4) & 0x0F)
    ver_str += '.'
    ver_str += str(version & 0x0F)
    return ver_str



  def set_port1(self, sku):
    '''!
      @brief Set SKU on Port1, which can be connected to analog & digital sensors. Select the sensor connected to Port1 by SKU
      @param sku  Parameter for port1. The supported SKU list can be viewed on the OLED or by getAnalogSensorSKU()/getDigitalSensorSKU()
      @n     "NULL"       Clear sensor settings for Port1 and configure mode as analog sensor mode
      @n     "Analog"     Select analog voltage data acquisition, unit mV
      @n     Analog sensor SKU Select the SKU of an analog sensor and configure mode as analog sensor mode
      @n     Digital sensor SKU Select the SKU of a digital sensor and configure mode as digital sensor mode
      @return  Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller(master)
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  Peripheral(slave) fault
      @n      ERR_CODE_ARGS         or 0x07  Set wrong parameters 
      @n      ERR_CODE_SKU          or 0x08  The SKU is invalid SKU or unsupported by the SCI Acquisition Module
      @n      ERR_CODE_S_NO_SPACE   or 0x09  Insufficient memory of I2C peripheral(slave)
    '''
    length = len(sku)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF0
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    i = 0
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF0)
    return recv_pkt[self.INDEX_RES_ERR]
  
  def get_port1(self):
    '''!
      @brief Get the sensor mode on port1 and SKU config
      @return List
      @n      The zeroth element in the list: error code
      @n      The first element in the list: sensor mode
      @n      The second element in the list: sku config
    '''
    rslt = [0,0,"NULL"]
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_READ_IF0
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_READ_IF0)
    rslt[self.INDEX_ERR_CODE] = recv_pkt[self.INDEX_RES_ERR]
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        rslt[self.INDEX_MODE] = recv_pkt[self.INDEX_RES_DATA]
        rslt[self.INDEX_SKU]  = ""
        for data in recv_pkt[self.INDEX_RES_DATA + 1:]:
          rslt[self.INDEX_SKU] += chr(data)
    return rslt
  
  def set_port2(self, sku):
    '''!
      @brief Set SKU on Port2, which can be connected to I2C or UART sensor. I2C sensors can be auto selected when connected,
      @ you just need to configure the mode as I2C mode for port2. But for UART sensors, please select by SKU.
      @param sku  The 7-bit SKU code for I2C or UART Sensor
      @return Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  Peripheral fault
      @n      ERR_CODE_ARGS         or 0x07  Set wrong parameters 
      @n      ERR_CODE_SKU          or 0x08  The SKU is invalid SKU or unsupported by the SCI Acquisition Module
      @n      ERR_CODE_S_NO_SPACE   or 0x09  Insufficient memory of I2C peripheral(slave)
    '''
    length = len(sku)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF2
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    i = 0
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF2)
    return recv_pkt[self.INDEX_RES_ERR]

  def get_port2(self):
    '''!
      @brief Get the sensor mode on port2 and SKU config
      @return List
      @n      The zeroth element in the list: error code
      @n      The first element in the list: sensor mode
      @n      The second element in the list: sku config
    '''
    rslt = [0,0,"NULL"]
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_READ_IF1
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_READ_IF1)
    rslt[self.INDEX_ERR_CODE] = recv_pkt[self.INDEX_RES_ERR]
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        rslt[self.INDEX_MODE] = recv_pkt[self.INDEX_RES_DATA]
        rslt[self.INDEX_SKU]  = ""
        for data in recv_pkt[self.INDEX_RES_DATA + 1:]:
          rslt[self.INDEX_SKU] += chr(data)
    return rslt

  def set_port3(self, sku):
    '''!
      @brief Set SKU on Port3, which can be connected to I2C or UART sensor. I2C sensors can be auto selected when connected,
      @ you just need to configure the mode as I2C mode for port2. But for UART sensors, please select by SKU.
      @param sku  The 7-bit SKU code for I2C or UART Sensor
      @return Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  Peripheral fault
      @n      ERR_CODE_ARGS         or 0x07  Set wrong parameters 
      @n      ERR_CODE_SKU          or 0x08  The SKU is invalid SKU or unsupported by the SCI Acquisition Module
      @n      ERR_CODE_S_NO_SPACE   or 0x09  Insufficient memory of I2C peripheral
    '''
    length = len(sku)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF2
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    i = 0
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF2)
    return recv_pkt[self.INDEX_RES_ERR]

  def get_port3(self):
    '''!
      @brief Get the sensor mode on port3 and SKU config
      @return List
      @n      The zeroth element in the list: error code 
      @n      The first element in the list: sensor mode 
      @n      The second element in the list: sku config
    '''
    rslt = [0,0,"NULL"]
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_READ_IF2
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_READ_IF2)
    rslt[self.INDEX_ERR_CODE] = recv_pkt[self.INDEX_RES_ERR]
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        rslt[self.INDEX_MODE] = recv_pkt[self.INDEX_RES_DATA]
        rslt[self.INDEX_SKU]  = ""
        for data in recv_pkt[self.INDEX_RES_DATA + 1:]:
          rslt[self.INDEX_SKU] += chr(data)
    return rslt


  def set_recv_timeout(self,timeout = 2):
    '''!
      @brief Initalize the SCI Acquisition Module, mainly for initializing communication interface
      @param timeout Set Timeout
      @return int Init status
      @n       0      Init successful
      @n      others  Init failed
    '''
    self.DEBUG_TIMEOUT_MS = timeout
    
  def adjust_rtc_datetime(self):
    '''!
      @brief Set the date and time of the SCI Acquisition Module to the current time of Raspbbery Pi
      @return  Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed 
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error 
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout 
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
    '''
    time = datetime.datetime.now()
    week = self._day_of_week(time.year, time.month, time.day)
    return self.adjust_rtc(time.year, time.month, time.day, week, time.hour, time.minute, time.second)

  
  def adjust_rtc(self, year, month, day, week, hour, minute, second):
    '''!
      @brief Set the year, month, day, week, hour, minute, second for the SCI Acquisition Module
      @param year   Year
      @param month  Month
      @param day    Day
      @param week   Week 
      @param hour   Hour
      @param minute Minute
      @param second Second
      @return  Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed 
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command 
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error 
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout 
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
    '''
    length = 8
    addr = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_TIME
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS + 0]        = second
    pkt[self.INDEX_ARGS + 1]        = minute
    pkt[self.INDEX_ARGS + 2]        = hour
    pkt[self.INDEX_ARGS + 3]        = day
    pkt[self.INDEX_ARGS + 4]        = week
    pkt[self.INDEX_ARGS + 5]        = month
    pkt[self.INDEX_ARGS + 6]        = year & 0xFF
    pkt[self.INDEX_ARGS + 7]        = (year >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_TIME)
    return recv_pkt[self.INDEX_RES_ERR]

  def get_rtc_time(self):
    '''!
      @brief @brief Get the year, month, day, week, hour, minute, second of the SCI Acquisition Module
      @return List with a length of 2 data
      @n      The first data in the list: list year, month, day, week, hour, minute, second[year, month, day, week, hour, minute, second]
      @n      The second data in the list: char string, year/month/day week hour:minute/second e.g. 2022/08/09 2 09:08:00
    '''
    rslt = [[0,0,0,0,0,0,0],"0000/00/00 0 00:00:00"]
    length = 0
    addr = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_TIME
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_TIME)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length == 8:
        rslt1 = [0]*8
        rslt1[self.INDEX_SECOND]   = recv_pkt[self.INDEX_RES_DATA + 0]
        rslt1[self.INDEX_MINUTE]   = recv_pkt[self.INDEX_RES_DATA + 1]
        rslt1[self.INDEX_HOUR]     = recv_pkt[self.INDEX_RES_DATA + 2]
        rslt1[self.INDEX_DAY]      = recv_pkt[self.INDEX_RES_DATA + 3]
        rslt1[self.INDEX_WEEK]     = recv_pkt[self.INDEX_RES_DATA + 4]
        rslt1[self.INDEX_MONTH]    = recv_pkt[self.INDEX_RES_DATA + 5]
        rslt1[self.INDEX_YEAR]     = recv_pkt[self.INDEX_RES_DATA + 6] | (recv_pkt[self.INDEX_RES_DATA + 7] << 8)
        rslt1[self.INDEX_TIME_STR] = str(rslt1[self.INDEX_YEAR]) + '/'
        if(rslt1[self.INDEX_MONTH] < 10):
          rslt1[self.INDEX_TIME_STR] += '0'
        rslt1[self.INDEX_TIME_STR] += str(rslt1[self.INDEX_MONTH]) + '/'

        if(rslt1[self.INDEX_DAY] < 10):
          rslt1[self.INDEX_TIME_STR] += '0'
        rslt1[self.INDEX_TIME_STR] += str(rslt1[self.INDEX_DAY]) + ' '

        rslt1[self.INDEX_TIME_STR] += str(rslt1[self.INDEX_WEEK]) + ' '

        if(rslt1[self.INDEX_HOUR] < 10):
          rslt1[self.INDEX_TIME_STR] += '0'
        rslt1[self.INDEX_TIME_STR] += str(rslt1[self.INDEX_HOUR]) + ':'

        if(rslt1[self.INDEX_MINUTE] < 10):
          rslt1[self.INDEX_TIME_STR] += '0'
        rslt1[self.INDEX_TIME_STR] += str(rslt1[self.INDEX_MINUTE]) + ':'

        if(rslt1[self.INDEX_SECOND] < 10):
          rslt1[self.INDEX_TIME_STR] += '0'
        rslt1[self.INDEX_TIME_STR] += str(rslt1[self.INDEX_SECOND])
        rslt[0] = rslt1[:7]
        rslt[1] = rslt1[7]
    return rslt
  
  def set_refresh_rate(self, rate):
    '''!
      @brief Set data refresh rate
      @param rate Enum variable
      @n eRefreshRateMs     ms-level, refresh at the actual refresh rate
      @n eRefreshRate1s     1s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n eRefreshRate3s     3s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n eRefreshRate5s     5s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n eRefreshRate10s    10s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n eRefreshRate30s    30s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n eRefreshRate1min   1min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n eRefreshRate5min   5min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n eRefreshRate10min  10min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @return  Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
    '''
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_REFRESH_TIME
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = rate
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_REFRESH_TIME)
    return recv_pkt[self.INDEX_RES_ERR]

  def get_refresh_rate(self):
    '''!
      @brief Get data refresh rate
      @return  List
      @n      The zeroth element in the list: error code 
      @n      The first element in the list: refresh rate
      @n      0 or eRefreshRateMs     ms-level, refresh at the actual refresh rate
      @n      1 or eRefreshRate1s     1s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate 
      @n      2 or eRefreshRate3s     3s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n      3 or eRefreshRate5s     5s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n      4 or eRefreshRate10s    10s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n      5 or eRefreshRate30s    30s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n      6 or eRefreshRate1min   1min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n      7 or eRefreshRate5min   5min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
      @n      8 or eRefreshRate10min  10min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
    '''
    rslt = [0,0]
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_REFRESH_TIME
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_REFRESH_TIME)
    rslt[self.INDEX_ERR_CODE] = recv_pkt[self.INDEX_RES_ERR]
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        rslt[self.INDEX_MODE] = recv_pkt[self.INDEX_RES_DATA]
    return rslt

  def get_refresh_rate_describe(self, rate):
    '''!
      @brief Get refresh rate description, unit s
    '''
    if rate == self.eRefreshRateMs:
      return 0
    elif rate == self.eRefreshRate1s:
      return 1
    elif rate == self.eRefreshRate3s:
      return 3
    elif rate == self.eRefreshRate5s:
      return 5
    elif rate == self.eRefreshRate10s:
      return 10
    elif rate == self.eRefreshRate30s:
      return 30
    elif rate == self.eRefreshRate1min:
      return 60
    elif rate == self.eRefreshRate5min:
      return 300
    elif rate == self.eRefreshRate10min:
      return 600
    return 0
    
  def get_timestamp(self):
    '''!
      @brief Get time stamp, also the data refresh time of the SCI Acquisition Module
      @return Hour:Minute:Second(00:00:00) or Minute:Second. X%(0-99)second(00:00.00)
    '''
    rslt = ""
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_TIMESTAMP
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_TIMESTAMP)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_AD_sensor_mode_describe(self, mode):
    '''!
      @brief Get mode description of Aanlog & Digital sensor
      @param mode Sensor mode 
      @n     eAnalogMode    Analog sensor mode
      @n     eDigitalMode   Digital sensor mode
      @return Sensor mode description char string
      @n      "ANALOG"         Analog sensor mode 
      @n      "DIGITAL"        Digital sensor mode 
      @n      "UNKNOWN"        Unknown mode 
    '''
    if mode == self.eAnalogMode:
      return "ANALOG" 
    elif mode == self.eDigitalMode:
      return "DIGITAL" 
    else:
      return "UNKNOWN"

  def get_I2CUART_sensor_mode_describe(self, mode):
    '''!
      @brief Get mode description of I2C & UART sensor
      @param mode Sensor mode
      @n     eI2CMode    I2C sensor mode 
      @n     eUARTMode   UART sensor mode
      @return Sensor mode description char string
      @n      "I2C"         I2C sensor mode 
      @n      "UART"        UART sensor mode 
      @n      "UNKNOWN"     Unknown mode
    '''
    if mode == self.eI2CMode:
      return "I2C" 
    elif mode == self.eUARTMode:
      return "UART" 
    else:
      return "UNKNOWN"

  

  def enable_record(self):
    '''!
      @brief Enable data recording in CSV file. When enabled, the sensor data will be recorded in the csv file named by date year, year, day, hour, minute, and second.
      @return Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
    '''
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_RECORD_ON
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_RECORD_ON)
    return recv_pkt[self.INDEX_RES_ERR]

  def disable_record(self):
    '''!
      @brief Disable data recording in CSV file. When disabled, data recording stops 
      @return Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
    '''
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_RECORD_OFF
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_RECORD_OFF)
    return recv_pkt[self.INDEX_RES_ERR]

  def display_on(self):
    '''!
      @brief Switch on SCI Acquisition Module Screen
      @return Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
    '''
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SCREEN_ON
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SCREEN_ON)
    return recv_pkt[self.INDEX_RES_ERR]

  def display_off(self):
    '''!
      @brief Switch off SCI Acquisition Module Screen
      @return Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
    '''
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SCREEN_OFF
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SCREEN_OFF)
    return recv_pkt[self.INDEX_RES_ERR]

  def get_information(self, inf, timestamp = False):
    '''!
      @brief Get the attribute information(attribute: value unit) of all sensors connected to the designated one or more ports. Separate attributes using ","
      @param inf Designate one or more ports
      @n     ePort1                                    Select port1, get attributes of all sensors connected to port1
      @n     ePort2                                    Select port2, get attributes of all sensors connected to port2
      @n     ePort3                                    Select port3, get attributes of all sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get attributes of all sensors connected to all ports
      @param timestamp true or false
      @return The attribute information of all sensors connected to the designated one or more ports of the SCI Acquisition Module
      @n For example, SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
    '''
    rslt = ""
    length = 2
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_INFO
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    pkt[self.INDEX_ARGS + 1]   = timestamp
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_INFO)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_sku(self, inf):
    '''!
      @brief Get the SKUs of all sensors connected to the designated one or more ports. Separate SKUs using ","
      @param inf Designate one or more ports
      @n     ePort1                                    Select port1, get SKUs of all sensors connected to port1
      @n     ePort2                                    Select port2, get SKUs of all sensors connected to port2
      @n     ePort3                                    Select port3, get SKUs of all sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get SKUs of all sensors connected to all ports
      @return The SKUs of all sensors connected to the designated one or more ports of the SCI Acquisition Module
      @n For example:  SEN0161,SEN0334
    '''
    rslt = ""
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_SKU
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_SKU)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_keys(self, inf):
    '''!
      @brief Get attribute names of all sensors connected to the designated one or more ports. Separate attribute names using ","
      @param inf Designate one or more ports
      @n     ePort1                                    Select port1, get attribute names of all sensors connected to port1
      @n     ePort2                                    Select port2, get attribute names of all sensors connected to port2
      @n     ePort3                                    Select port3, get attribute names of all sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get attribute names of all sensors connected to all ports
      @return The attribute names of all sensors connected to the designated one or more ports of the SCI Acquisition Module
      @n For example:  Temp_Air,Humi_Air
    '''
    rslt = ""
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_NAME
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_NAME)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_values(self, inf):
    '''!
      @brief Get attribute data values of all sensors connected to the designated one or more ports. Separate attribute data values using ","
      @param inf Designate one or more ports
      @n     ePort1                                    Select port1, get attribute data values of all sensors connected to port1
      @n     ePort2                                    Select port2, get attribute data values of all sensors connected to port2
      @n     ePort3                                    Select port3, get attribute data values of all sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get attribute data values of all sensors connected to all ports
      @return The attribute data values of all sensors connected to the designated one or more ports of the SCI Acquisition Module
      @n For example:  28.65,30.12
    '''
    rslt = ""
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_VALUE
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_VALUE)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_units(self, inf):
    '''!
      @brief Get attribute units of all sensors connected to the designated one or more ports. Separate attribute units using ","
      @param inf Designate one or more ports
      @n     ePort1                                    Select port1, get attribute units of all sensors connected to port1
      @n     ePort2                                    Select port2, get attribute units of all sensors connected to port2
      @n     ePort3                                    Select port3, get attribute units of all sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get attribute units of all sensors connected to all ports
      @return The attribute units of all sensors connected to the designated one or more ports of the SCI Acquisition Module
      @n For example:  C,%RH
    '''
    rslt = ""
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_UNIT
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_UNIT)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_value0(self, keys):
    '''!
      @brief Get data values of the attribute named keys from sensors connected to all ports. Separate attribute values using ","
      @param keys  Sensor attribute name
      @return Data values of the attribute named keys from sensors connected to all ports. Separate attribute values using ","
      @n For example, Temp_Air:  28.65,28.65
    '''
    rslt = ""
    length = len(keys)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_KEY_VALUE0
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    i = 0
    for c in keys:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_KEY_VALUE0)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_value1(self, inf, keys):
    '''!
      @brief Get data values of the attribute named keys from sensors connected to the designated port. Separate attribute values using ","
      @param inf    Port select, and parameter search range
      @n     ePort1                                    Select port1, get data values of the attribute named keys from sensors connected to port1
      @n     ePort2                                    Select port2, get data values of the attribute named keys from sensors connected to port2
      @n     ePort3                                    Select port3, get data values of the attribute named keys from sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get data values of the attribute named keys from sensors connected to all ports
      @param keys  Sensor attribute name
      @return The data values of the attribute named keys from sensors connected to the designated port. Separate attribute values using ","
      @n For example, Temp_Air:  28.65,28.65
    '''
    length = len(keys) + 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_KEY_VALUE1
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    i = 1
    for c in keys:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)
    
    recv_pkt = self._recv_packet(self.CMD_GET_KEY_VALUE1)
    rslt = ""
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_value2(self, inf, sku, keys):
    '''!
      @brief Get data values of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port. 
      @ Separate attribute values using ","
      @param inf    Port select, and parameter search range
      @n     ePort1                                    Select port1, get the sensor whose SKU is sku from port1, and read data values of the attribute named keys
      @n     ePort2                                    Select port2, get the sensor whose SKU is sku from port2, and read data values of the attribute named keys
      @n     ePort3                                    Select port3, get the sensor whose SKU is sku from port3, and read data values of the attribute named keys
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get sensors whose SKU is sku from all ports, 
      @ and read data values of the attribute named keys
      @param sku Sensor SKU
      @param keys  Sensor attribute name
      @return The data values of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port. 
      @ Separate attribute values using ","
      @n For example, Temp_Air:  28.65,28.65
    '''
    length = len(keys) + 1 + len(sku)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_KEY_VALUE2
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    i = 1
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    for c in keys:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_KEY_VALUE2)
    rslt = ""
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_unit0(self, keys):
    '''!
      @brief Get data units of the attribute named keys from sensors connected to all ports. Separate attribute units using ","
      @param keys  Sensor attribute name
      @return Data units of the attribute named keys from sensors connected to all ports. Separate attribute units using ","
      @n For example, Temp_Air:  C,C
    '''
    length = len(keys)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_KEY_UINT0
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    i = 0
    for c in keys:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_KEY_UINT0)
    rslt = ""
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_unit1(self, inf, keys):
    '''!
      @brief Get data units of the attribute named keys from sensors connected to the designated port. Separate attribute units using ","
      @param inf    Port select, and parameter search range
      @n     ePort1                                    Select port1, get data units of the attribute named keys from sensors connected to port1
      @n     ePort2                                    Select port2, get data units of the attribute named keys from sensors connected to port2
      @n     ePort3                                    Select port3, get data units of the attribute named keys from sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get data units of the attribute named keys from sensors connected to all ports 
      @param keys  Sensor attribute name
      @return The data units of the attribute named keys from sensors connected to the designated port. Separate attribute units using ","
      @n For example, Temp_Air:  C,C
    '''
    length = len(keys) + 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_KEY_UINT1
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    i = 1
    for c in keys:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_KEY_UINT1)
    rslt = ""
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_unit2(self, inf, sku, keys):
    '''!
      @brief Get data units of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port. 
      @ Separate attribute units using ","
      @param inf    Port select, and parameter search range
      @n     ePort1                                    Select port1, get the sensor whose SKU is sku from ePort1, and read data units of the attribute named keys  
      @n     ePort2                                    Select port2, get the sensor whose SKU is sku from ePort2, and read data units of the attribute named keys
      @n     ePort3                                    Select port3, get the sensor whose SKU is sku from ePort3, and read data units of the attribute named keys
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select port1, port2 and port3, get sensors whose SKU is sku from all ports, and read data units of the attribute named keys
      @param sku Sensor SKU
      @param keys  Sensor attribute name
      @return The data units of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port.
      @ Separate attribute units using ","
      @n For example, Temp_Air:  C,C
    '''
    length = len(keys) + 1 + len(sku)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_KEY_UINT2
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    i = 1
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    for c in keys:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_KEY_UINT2)
    rslt = ""
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_analog_sensor_sku(self):
    '''!
      @brief Get the SKU list of analog sensors supported by SCI Acquisition Module
      @return SKU list of supported analog sensors, return NULL if there is not
    '''
    rslt = ""
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SKU_A
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SKU_A)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt
  
  def get_digital_sensor_sku(self):
    '''!
      @brief Get the SKU list of digital sensors supported by SCI Acquisition Module
      @return SKU list of supported digital sensors, return NULL if there is not
    '''
    rslt = ""
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SKU_D
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SKU_D)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_i2c_sensor_sku(self):
    '''!
      @brief Get the SKU list of I2C sensors supported by SCI Acquisition Module
      @return SKU list of supported I2C sensors, return NULL if there is not
    '''
    rslt = ""
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SKU_IIC
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SKU_IIC)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def get_uart_sensor_sku(self):
    '''!
      @brief Get the SKU list of UART sensors supported by SCI Acquisition Module
      @return SKU list of supported UART sensors, return NULL if there is not
    '''
    rslt = ""
    length = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SKU_UART
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SKU_UART)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
    return rslt

  def _recv_packet(self, cmd):
    '''!
      @brief Receive and parse the response data packet
      @param cmd Command to receive the packet
      @return Error code and response packet list
      @n      The zeroth element in the list: error code, only when the error code is ERR_CODE_NONE, there can be other elements
      @n      The first element in the list: response packet status code, 0x53-correct response packet 0x63-wrong response packet
      @n      The second element in the list: response packet command, which indicates the response packet belongs to which communication command
      @n      The third element in the list: low byte of the valid data length after the response packet
      @n      The fourth element in the list: high byte of the valid data length after the response packet
      @n      The 5th element or more in the list: valid data
    '''
    rslt = [0] * 1
    t = time.time()
    while time.time() - t < self.DEBUG_TIMEOUT_MS:
      status = self._recv_data(1)[0]
      #print("status=%x"%status)
      if status == self.STATUS_SUCCESS or status == self.STATUS_FAILED:
        command = self._recv_data(1)[0]
        #print("command=%x cmd=%x"%(command,cmd))
        if command != cmd:
          self._reset(cmd)
          rslt[0] = self.ERR_CODE_RES_PKT
          print("Response pkt is error!")
          return rslt
        lenL = self._recv_data(2)
        length = (lenL[1] << 2) | lenL[0]
        #print("length=%x length=%d"%(length,length))
        rslt[0] = self.ERR_CODE_NONE
        rslt = rslt + [status, command, lenL[0], lenL[1]]
        if length:
          rslt = rslt + self._recv_data(length)
        #print(rslt)
        #print("time: %f"%(time.time() - t))
        return rslt
      time.sleep(0.05)
    self._reset(self.CMD_RESET)
    print("time out: %f"%(time.time() - t))
    return [self.ERR_CODE_RES_TIMEOUT]

  def _reset(self, cmd):
    '''!
      @brief Reset the cache sending of SCI Acquisition Module
      @param cmd Communication command
    '''
    len = 1
    pkt = [0] * (3 + len)
    pkt[self.INDEX_CMD]        = self.CMD_RESET
    pkt[self.INDEX_ARGS_NUM_L] = len & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (len >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = cmd
    self._send_packet(pkt)
    time.sleep(2)
  
  def _day_of_week(self, year, month, day):
    '''!
      @brief Calculate the day of a week according to year/month/day
      @param year   Year
      @param month  Month
      @param day    Day
      @return uint8_t The day of a week(0~6)
      @n 0   Sunday
      @n 1   Monday
      @n 2   Tuesday
      @n 3   Wednesday
      @n 4   Thursday
      @n 5   Friday
      @n 6   Saturday
    '''
    days = day
    if(year > 2000):
      year -= 2000
    i = 1
    while i < month:
      if(i == 2):
        days += 28
      elif (i == 4) or (i == 6) or (i == 9) or (i == 11):
        days += 30
      else:
        days += 31
      i += 1
    if(month > 2) and (year%4 == 0):
      days += 1
    days = days + 365*year + (year + 3) // 4 - 1
    return (days + 6) % 7


  def _send_packet(self, pkt):
    pass
   
  def _recv_data(self, len):
    pass


class DFRobot_RP2040_SCI_IIC(DFRobot_RP2040_SCI):
  def __init__(self,addr):
    '''!
      @brief DFRobot_SCI_IIC Constructor
      @param addr:  7-bit IIC address, support the following address settings
      @n RP2040_SCI_ADDR_0X21      0x21 default I2C address
      @n RP2040_SCI_ADDR_0X22      0x22
      @n RP2040_SCI_ADDR_0X23      0x23
    '''
    self._addr = addr
    self._bus = smbus.SMBus(1)
    DFRobot_RP2040_SCI.__init__(self)
    
  def get_i2c_address(self):
    '''!
      @brief Get SCI Acquisition Module I2C address
      @return I2C address
    '''
    length = 0
    addr = 0
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_READ_ADDR
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_READ_ADDR)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length == 1:
        addr = recv_pkt[self.INDEX_RES_DATA]
    return addr
  
  def set_i2c_address(self, addr):
    '''!
      @brief Set SCI Acquisition Module I2C address 
      @param addr SCI Acquisition Module I2C address, support the following address settings
      @n RP2040_SCI_ADDR_0X21      0x21 default I2C address
      @n RP2040_SCI_ADDR_0X22      0x22
      @n RP2040_SCI_ADDR_0X23      0x23
      @return Error code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed 
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command 
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error 
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller(master) 
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout 
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
      @n      ERR_CODE_I2C_ADRESS   or 0x0A  Invalid I2C address
    '''
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_ADDR
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = addr
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_READ_ADDR)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      self._addr = addr
    return recv_pkt[0]

  def _send_packet(self, pkt):
    '''!
      @brief Send data
      @param pkt List of data to be sent
      @return None
    '''
    for data in pkt:
      try:
        self._bus.write_byte(self._addr, data)
      except:
        pass
    
  def _recv_data(self, len):
    '''!
      @brief Read data
      @param len Number of bytes to be read
      @return The read data list
    '''
    rslt = [0]*len
    i = 0
    while i < len:
      try:
        rslt[i] = self._bus.read_byte(self._addr)
      except:
        rslt[i] = 0
      i += 1
    return rslt
