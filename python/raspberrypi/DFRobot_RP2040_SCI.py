# -*- coding:utf-8 -*-
'''!
  @file DFRobot_RP2040_SCI.py
  @brief This is an Arduino drive library for the DFRobot SCI Acquisition module. Users can read or set its relevant config and data through the I2C interface. The following demonstrates its detailed functions:
  @n 1. Set or read the I2C communication address of SCI acquisition module as 0x21, 0x22 or 0x23, the factory default is 0x21, after the I2C address is changed, it takes effect after power-off and reboot;
  @n 2. Set or read the config of Port1, Port2 or Port3:
  @n    Port1: can be configured as analog or digital sensor mode, supporting NULL, Analog, and analog sensor SKU in analog sensor mode, and supporting digital sensor SKU in digital sensor mode
  @n    Port2: can be configured as I2C or UART sensor mode, supporting NULL or I2C sensor in I2C sensor mode, in which I2C sensor will be automatically recognized by the module when powered on, and supporting UART sensor SKU in UART sensor mode
  @n    Port3: can be configured as I2C or UART sensor mode, supporting NULL or I2C sensor in I2C sensor mode, in which I2C sensor will be automatically recognized by the module when powered on, and supporting UART sensor SKU in UART sensor mode
  @n 3. Enable/disable data record of CSV file
  @n 4. Enable/disable OLED display
  @n 5. Read the parameters of the sensors on the board：
  @n      a. Get the "name" of sensor data, the names are separated by a comma(,);
  @n      b. Get the "value" of sensor data, the values are separated by a comma(,);
  @n      c. Get the unit of sensor data, the units are separated by a comma(,);
  @n      d. Get the SKU of the connected sensor;
  @n      e. Get the complete sensor information in the format of name:value unit, multiple pieces of information are separated by a comma (,)
  @n 6. Set and read data refresh time
  @n 7. Get data refresh timestamp
  @copyright   Copyright (c) 2022 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2022-07-20
  @url https://github.com/DFRobot/DFRobot_RP2040_SCI
'''
import sys
import smbus
import time
import datetime

class DFRobot_SCI:
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
  ## Set port 1 command, which can be used to configure the function and SKU on I2C1&UART1 ports
  CMD_SET_IF1    =   0x01  
  ## Set port 2 command, which can be used to configure the function and SKU on I2C2 & UART2 ports
  CMD_SET_IF2    =   0x02  
  ## Read the function and SKU on port 0
  CMD_READ_IF0   =   0x00  
  ## Read the function and SKU on port 1
  CMD_READ_IF1   =   0x01  
  ## Read the function and SKU on port 2
  CMD_READ_IF2   =   0x02  
  ## Set I2C address command (the command will take effect immediately when it's set successfully)
  CMD_SET_ADDR   =   0x03 
  ## Read I2C address command (the command will take effect immediately when it's set successfully)
  CMD_READ_ADDR  =   0x03 
  ## Set the time information of year, month, day, hour, minute, second
  CMD_SET_TIME   =   0x04 
  ## Get the time information of year, month, day, hour, minute, second
  CMD_GET_TIME   =   0x04 
  ## Enable CSV record
  CMD_RECORD_ON  =   0x05 
  ## Disable CSV record
  CMD_RECORD_OFF =   0x06 
  ## Enable OLED display
  CMD_SCREEN_ON  =   0x07  
  ## Disable OLED display
  CMD_SCREEN_OFF =   0x08  
  ## Get sensor data name
  CMD_GET_NAME   =   0x09  
  ## Get sensor data value
  CMD_GET_VALUE  =   0x0A  
  ## Get sensor data unit
  CMD_GET_UNIT   =   0x0B  
  ## Get sensor SKU, SKUs are separated by a comma(,)
  CMD_GET_SKU    =   0x0C  
  ## Get the sensor data name, value and unit name, the value and unit name are separated by space, and others are separated by comma(,)
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
  ## Command to copy I2C peripheral(slave) and send cache
  CMD_RESET           =  0x14 
  ## Command to get the supported Analog sensor SKU 
  CMD_SKU_A           =  0x15  
  ## Command to get the supported Digital sensor SKU
  CMD_SKU_D           =  0x16  
  ## Command to get the supported I2C sensor SKU
  CMD_SKU_IIC         =  0x17  
  ## Command to get the supported UART sensor SKU
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
  ## The SKU is an invalid SKU, or the one unsupported by SCI Acquisition Module
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
      @brief SCI采集模块(SCI Acquisition Module)初始化，旨在初始化通信接口
      @param freq 设置通信频率
      @return int 初始化状态
      @n       0      初始化成功
      @n      others  初始化失败
    '''
    self._reset(self.CMD_RESET)
    return 0
  
  def get_version(self):
    '''!
      @brief 获取SCI采集模块(SCI Acquisition Module)的固件版本号
      @n 版本号是一个16位数据，高8位(b15~b9): 代表最高版本位
      @n 中4位(b8~b4):表示中间版本位
      @n 低4位：表示低版本位
      @n 例0x0123对应的版本号为 V1.2.3
      @n     数字传感器SKU 表示选择了某个数字传感器的SKU，并将模式配置为数字传感器模式
      @return 16位版本号
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
      @brief 获取版本描述字符串
      @return 返回版本描述字符串，例版本id：0x0123返回的版本描述字符串为 V1.2.3
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
      @brief 设置Port1的SKU，此接口可连接模拟传感器和数字传感器，通过SKU选择Port1上连接的传感器
      @param sku  Port1接口的参数，支持的SKU列表可以通过OLED显示或者 getAnalogSensorSKU()/getDigitalSensorSKU()查看
      @n     "NULL"       表示清除Port1接口的传感器设置,并将传感器模式配置为模拟传感器配置
      @n     "Analog"     表示选择Analog电压数据采集，单位mV
      @n     模拟传感器SKU 表示选择了某个模拟传感器的SKU，并将模式配置为模拟传感器模式
      @n     数字传感器SKU 表示选择了某个数字传感器的SKU，并将模式配置为数字传感器模式
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者SCI采集模块(SCI Acquisition Module)不支持
      @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
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
      @brief 获取Port1接口的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
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
      @brief 设置Port2的SKU，此接口可连接I2C传感器和UART传感器，其中UART传感器需通过SKU选择，I2C是连接后，自动选择，只需将Port2配置为I2C模式即可
      @param sku  I2C传感器或者UART传感器的7位SKU代码
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者SCI采集模块(SCI Acquisition Module)不支持
      @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
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
      @brief 获取Port2的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
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
      @brief 设置Port3的SKU，此接口可连接I2C传感器和UART传感器，其中UART传感器需通过SKU选择，I2C是连接后，自动选择，只需将Port2配置为I2C模式即可
      @param sku  I2C传感器或者UART传感器的7位SKU代码
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者SCI采集模块(SCI Acquisition Module)不支持
      @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
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
      @brief 获取Port3接口的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
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
      @brief SCI采集模块(SCI Acquisition Module)初始化，旨在初始化通信接口
      @param freq 设置通信频率
      @return int 初始化状态
      @n       0      初始化成功
      @n      others  初始化失败
    '''
    self.DEBUG_TIMEOUT_MS = timeout
    
  def adjust_rtc_datetime(self):
    '''!
      @brief 设置SCI采集模块(SCI Acquisition Module)的日期和时间为树莓派的当前时间
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
    '''
    time = datetime.datetime.now()
    week = self._day_of_week(time.year, time.month, time.day)
    return self.adjust_rtc(time.year, time.month, time.day, week, time.hour, time.minute, time.second)

  
  def adjust_rtc(self, year, month, day, week, hour, minute, second):
    '''!
      @brief 设置SCI采集模块(SCI Acquisition Module)的年月日时分秒周等日期
      @param year   年
      @param month  月
      @param day    日
      @param week   周
      @param hour   时
      @param minute 分
      @param second 秒
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
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
      @brief @brief 获取SCI采集模块(SCI Acquisition Module)的年月日时分秒周等日期
      @return 长度为2的列表
      @n      列表中第0个元数: 列表年，月，日，星期，时，分，秒[年，月，日，星期，时，分，秒]
      @n      列表中第2个元数: 字符串，年/月/日 星期 时:分:秒 例: 2022/08/09 2 09:08:00
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
      @brief 设置数据刷新时间
      @param rate 枚举变量
      @n eRefreshRateMs     ms级刷新率，按数据的实际刷新率刷新
      @n eRefreshRate1s     刷新率1s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate3s     刷新率3s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate5s     刷新率5s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate10s    刷新率10s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate30s    刷新率30s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate1min   刷新率1min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate5min   刷新率5min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate10min  刷新率10min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
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
      @brief 获取数据刷新时间
      @param rate 枚举变量
      @n eRefreshRateMs     ms级刷新率，按数据的实际刷新率刷新
      @n eRefreshRate1s     刷新率1s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate3s     刷新率3s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate5s     刷新率5s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate10s    刷新率10s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate30s    刷新率30s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate1min   刷新率1min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate5min   刷新率5min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n eRefreshRate10min  刷新率10min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @return  列表
      @n      列表中第0个元素：错误代码
      @n      列表中第1个元素：刷新率
      @n      0 or eRefreshRateMs     ms级刷新率，按数据的实际刷新率刷新
      @n      1 or eRefreshRate1s     刷新率1s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n      2 or eRefreshRate3s     刷新率3s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n      3 or eRefreshRate5s     刷新率5s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n      4 or eRefreshRate10s    刷新率10s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n      5 or eRefreshRate30s    刷新率30s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n      6 or eRefreshRate1min   刷新率1min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n      7 or eRefreshRate5min   刷新率5min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
      @n      8 or eRefreshRate10min  刷新率10min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
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
      @brief 获取刷新率的描述，单位s
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
      @brief 获取时间戳,此时间戳为(SCI Acquisition Module)数据刷新时间
      @return 时:分:秒(00:00:00) 或 分:秒.百分之（0~99）秒(00:00.00)
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
      @brief 获取A&D类型传感器的模式描述
      @param mode 传感器类型模式
      @n     eAnalogMode    模拟传感器模式
      @n     eDigitalMode   数字传感器模式
      @return 传感器的模式描述字符串
      @n      "ANALOG"         模拟传感器模式
      @n      "DIGITAL"        数字传感器模式
      @n      "UNKNOWN"        未知模式
    '''
    if mode == self.eAnalogMode:
      return "ANALOG" 
    elif mode == self.eDigitalMode:
      return "DIGITAL" 
    else:
      return "UNKNOWN"

  def get_I2CUART_sensor_mode_describe(self, mode):
    '''!
      @brief 获取I2C&UART类型传感器的模式描述
      @param mode 传感器类型模式
      @n     eI2CMode    I2C传感器模式
      @n     eUARTMode   UART传感器模式
      @return 传感器的模式描述字符串
      @n      "I2C"         I2C传感器模式
      @n      "UART"        UART传感器模式
      @n      "UNKNOWN"     未知模式
    '''
    if mode == self.eI2CMode:
      return "I2C" 
    elif mode == self.eUARTMode:
      return "UART" 
    else:
      return "UNKNOWN"

  

  def enable_record(self):
    '''!
      @brief 开启CSV文件记录，调用此命令后，会将传感器采集到的数据记录在以年月日时分秒命名的CSV文件中
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
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
      @brief 关闭CSV文件记录，调用此命令后，会停止将传感器采集到的数据记录在以年月日时分秒命名的CSV文件中
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
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
      @brief 开启SCI采集模块(SCI Acquisition Module)屏显示
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
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
      @brief 关闭SCI采集模块(SCI Acquisition Module)屏显示
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
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
      @brief 获取SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的属性项(属性名称:数据值 单位)信息，属性项与属性项之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     ePort1                                    指定Port1接口，获取Port1接口上所连接的所有传感器的属性项
      @n     ePort2                                    指定Port2接口，获取ePort2接口上所连接的所有传感器的属性项
      @n     ePort3                                    选中Port3接口，获取ePort3接口上所连接的所有传感器的属性项
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，获取所有接口上所连接的所有传感器的属性项
      @return SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的属性项
      @n 例 SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
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
      @brief 获取SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的SKU，SKU与SKU之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     ePort1                                    指定Port1接口，获取Port1接口上所连接的所有传感器的SKU
      @n     ePort2                                    指定Port2接口，获取Port2接口上所连接的所有传感器的SKU
      @n     ePort3                                    指定Port3接口，获取Port3接口上所连接的所有传感器的SKU
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，获取所有接口上所连接的所有传感器的SKU
      @return SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的SKU
      @n 例:  SEN0161,SEN0334
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
      @brief 获取SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的所有属性名，属性名与属性名之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     ePort1                                    选中Port1接口，获取Port1接口上所连接的所有传感器的所有属性名
      @n     ePort2                                    选中Port2接口，获取Port2接口上所连接的所有传感器的所有属性名
      @n     ePort3                                    选中Port3接口，获取Port3接口上所连接的所有传感器的所有属性名
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，获取所有接口上所连接的所有传感器的所有属性名
      @return SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的所有属性名
      @n 例:  Temp_Air,Humi_Air
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
      @brief 获取SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的所有属性数据值，数据值与数据值之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     ePort1                                    选中Port1接口，获取Port1接口上所连接的所有传感器的所有属性数据值
      @n     ePort2                                    选中Port2接口，获取Port2接口上所连接的所有传感器的所有属性数据值
      @n     ePort3                                    选中Port3接口，获取Port3接口上所连接的所有传感器的所有属性数据值
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，获取所有接口上所连接的所有传感器的所有属性数据值
      @return SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的所有属性数据值
      @n 例:  28.65,30.12
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
      @brief 获取SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的所有属性单位，单位与单位之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     ePort1                                    选中Port1接口，获取Port1接口上所连接的所有传感器的所有属性单位
      @n     ePort2                                    选中Port2接口，获取Port2接口上所连接的所有传感器的所有属性单位
      @n     ePort3                                    选中Port3接口，获取Port3接口上所连接的所有传感器的所有属性单位
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，获取所有接口上所连接的所有传感器的所有属性单位
      @return SCI采集模块(SCI Acquisition Module)上指定的一个或多个接口上所连接的所有传感器的所有属性单位
      @n 例:  C,%RH
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
      @brief 获取所有接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @param keys  传感器属性名称
      @return 所有接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @n 例Temp_Air:  28.65,28.65
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
      @brief 获取指定接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     ePort1                                    选中Port1接口，获取Port1接口所连接的传感器中查找属性名称为keys的属性值
      @n     ePort2                                    选中Port2接口，获取Port2接口所连接的传感器中查找属性名称为keys的属性值
      @n     ePort3                                    选中Port3接口，获取Port3接口所连接的传感器中查找属性名称为keys的属性值
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，获取所有接口上在所有接口接口所连接的传感器中查找属性名称为keys的属性值
      @param keys  传感器属性名称
      @return 指定接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @n 例Temp_Air:  28.65,28.65
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
      @brief 获取指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     ePort1                                    选中Port1接口，获取Port1接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
      @n     ePort2                                    选中Port2接口，获取Port2接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
      @n     ePort3                                    选中Port3接口，获取Port3接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，在所有接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
      @param sku 传感器SKU
      @param keys  传感器属性名称
      @return 指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @n 例Temp_Air:  28.65,28.65
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
      @brief 获取所有接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @param keys  传感器属性名称
      @return 所有接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @n 例Temp_Air:  C,C
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
      @brief 获取指定接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     ePort1                                    选中Port1接口，获取Port1接口所连接的传感器中查找属性名称为keys的属性单位
      @n     ePort2                                    选中Port2接口，获取Port2接口所连接的传感器中查找属性名称为keys的属性单位
      @n     ePort3                                    选中Port3接口，获取Port3接口所连接的传感器中查找属性名称为keys的属性单位
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性单位
      @param keys  传感器属性名称
      @return 指定接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @n 例Temp_Air:  C,C
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
      @brief 获取指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     ePort1                                    选中Port1接口，获取ePort1接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
      @n     ePort2                                    选中Port2接口，获取ePort2接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
      @n     ePort3                                    选中Port3接口，获取ePort3接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，在所有接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
      @param sku 传感器SKU
      @param keys  传感器属性名称
      @return 指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @n 例Temp_Air:  C,C
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
      @brief 获取SCI采集模块(SCI Acquisition Module)Analog系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)Analog系列传感器的SKU支持列表，如果没有则返回NULL
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
      @brief 获取SCI采集模块(SCI Acquisition Module)Digital系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)Digital系列传感器的SKU支持列表，如果没有则返回NULL
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
      @brief 获取SCI采集模块(SCI Acquisition Module)I2C系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)I2C系列传感器的SKU支持列表，如果没有则返回NULL
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
      @brief 获取SCI采集模块(SCI Acquisition Module)UART系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)UART系列传感器的SKU支持列表，如果没有则返回NULL
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
      @brief 接收并解析响应的数据包
      @param cmd 要接收包的命令
      @return 错误代码以及响应包列表
      @n      列表中第0个元素    ： 错误代码，当错误代码为ERR_CODE_NONE时，才会有其他的元素
      @n      列表中第1个元素    ： 响应包状态码，0x53-正确响应包 0x63-错误响应包
      @n      列表中第2个元素    ： 响应包命令，即该响应包属于那个通信命令
      @n      列表中第3个元素    ： 响应包后面有效数据长度低字节
      @n      列表中第4个元素    ： 响应包后面有效数据长度高字节
      @n      列表中第5及以上元素： 有效数据
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
      @brief 复位SCI采集模块(SCI Acquisition Module)的发送缓存
      @param cmd 通信命令
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
      @brief 根据年/月/日计算星期数
      @param year   年
      @param month  月
      @param day    日
      @return uint8_t 0~6星期数
      @n 0   星期天
      @n 1   星期一
      @n 2   星期二
      @n 3   星期三
      @n 4   星期四
      @n 5   星期五
      @n 6   星期六
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


class DFRobot_RP2040_SCI_IIC(DFRobot_SCI):
  def __init__(self,addr):
    '''!
      @brief DFRobot_SCI_IIC 构造函数
      @param addr:  7-bit IIC address，支持以下地址设置
      @n RP2040_SCI_ADDR_0X21      0x21 转换板默认I2C地址
      @n RP2040_SCI_ADDR_0X22      0x22
      @n RP2040_SCI_ADDR_0X23      0x23
    '''
    self._addr = addr
    self._bus = smbus.SMBus(1)
    DFRobot_SCI.__init__(self)
    
  def get_i2c_address(self):
    '''!
      @brief 获取SCI采集模块(SCI Acquisition Module)的I2C通信地址
      @return I2C通信地址
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
      @brief 设置SCI采集模块(SCI Acquisition Module)的I2C通信地址 
      @param addr SCI采集模块(SCI Acquisition Module)的I2C通信地址，支持以下地址设置
      @n RP2040_SCI_ADDR_0X21      0x21 转换板默认I2C地址
      @n RP2040_SCI_ADDR_0X22      0x22
      @n RP2040_SCI_ADDR_0X23      0x23
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配 
      @n      ERR_CODE_I2C_ADRESS   or 0x0A  I2C地址无效
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
      @brief 发送数据
      @param pkt 要发送的数据列表
      @return None
    '''
    for data in pkt:
      try:
        self._bus.write_byte(self._addr, data)
      except:
        pass
    
  def _recv_data(self, len):
    '''!
      @brief 读取数据
      @param len 要读取得字节数
      @return 读取的数据列表
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
