# -*- coding:utf-8 -*-
'''!
  @file DFRobot_RP2040_SUAB.py
  @brief 这是一个传感器通用适配器板(Sensor Universal Adapter Board)，旨在配置适配器板参数，以及读取适配器板上各传感器的参数，具体功能如下所示：
  @n 配置适配器板参数：
  @n      1. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C地址，范围1~5；
  @n      2. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的年，月，日，时，分，秒的时间；
  @n      3. 开启/关闭数据记录，开启数据记录后，会将传感器通用适配器板(Sensor Universal Adapter Board)上各传感器的数据以CSV格式的文件记录下来保存到FLASH中，
  @n  用户可以通过U盘拷贝或查看该CSV记录文件，CSV文件的名字是以开启记录那刻时的年_月_日_时_分_秒的时间命名的。
  @n      4. 开启/关闭OLED屏显示，（开启显示，是进入初始化页面还是进入关闭前的页面）
  @n      5. 读取/设置 对应A/D，I2C1/UART1，I2C2/UART2等接口所对应的功能，及传感器的SKU, 默认配置为(A, NULL),(I2C1, NULL),(I2C2, NULL), NULL表示对应的接口上没有传感器
  @n 读取适配器板上各传感器的参数：
  @n      1. 获取传感器数据的"名称"，各名称之间用逗号(,)隔开;;
  @n      2. 获取传感器数据的"值"，各值之间用逗号(,)隔开;
  @n      3. 获取传感器数据值的单位，各单位之间用逗号(,)隔开;；
  @n      4. 获取接入传感器的SKU；
  @n      5. 以名称:值 单位的方式获取完整的传感器信息，各信息之间用逗号（,）隔开
  @copyright   Copyright (c) 2022 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2022-07-20
  @url https://github.com/DFRobot/DFRobot_RP2040_SUAB
'''
import sys
import smbus
import time
import datetime

class DFRobot_SUAB:
  ## 转换板默认I2C地址
  RP2040_SUAB_DEF_I2C_ADDR    =    0x05

  '''enum 将要设置或者读取的接口'''
  ## 设置或读取A&D接口   
  eAD        =  1 << 0
  ## 设置或读取I2C&UART1接口 
  eI2C_UART1 =  1 << 1 
  ## 设置或读取I2C&UART2接口  
  eI2C_UART2 =  1 << 2
  ## 设置或读取I2C&UART1接口 
  eALL       =  0x07

  '''enum A&D接口模式选择'''
  ## 模拟传感器模式  
  eAnalogMode  =  0
  ## 数字传感器模式 
  eDigitalMode =  1

  '''enum  I2C&UART接口模式选择'''
  ## I2C传感器模式   
  eI2CMode  =  0
  ## UART传感器模式
  eUARTMode =  1  

  ## 设置接口0命令，可以用此命令配置A&D接口的功能和SKU
  CMD_START   =  0x00
  ## 设置接口0命令，可以用此命令配置A&D接口的功能和SKU
  CMD_SET_IF0    =   0x00  
  ## 设置接口1命令，可以用此命令配置I2C1&UART1接口的功能和SKU
  CMD_SET_IF1    =   0x01  
  ## 设置接口2命令，可以用此命令配置I2C2&UART2接口的功能和SKU
  CMD_SET_IF2    =   0x02  
  ## 读取接口0的功能和SKU
  CMD_READ_IF0   =   0x00  
  ## 读取接口1的功能和SKU
  CMD_READ_IF1   =   0x01  
  ## 读取接口2的功能和SKU
  CMD_READ_IF2   =   0x02  
  ## 设置I2C地址命令（此命令，设置成功后，立即生效）
  CMD_SET_ADDR   =   0x03 
  ## 读取I2C地址命令（此命令，设置成功后，立即生效）
  CMD_READ_ADDR  =   0x03 
  ## 设置时间的年，月，日，时，分，秒
  CMD_SET_TIME   =   0x04 
  ## 获取时间的年，月，日，时，分，秒
  CMD_GET_TIME   =   0x04 
  ## 启动csv记录
  CMD_RECORD_ON  =   0x05 
  ## 停止CSV记录
  CMD_RECORD_OFF =   0x06 
  ## 开启oled显示
  CMD_SCREEN_ON  =   0x07  
  ## 关闭oled显示
  CMD_SCREEN_OFF =   0x08  
  ## 获取传感器数据名
  CMD_GET_NAME   =   0x09  
  ## 获取传感器数据值
  CMD_GET_VALUE  =   0x0A  
  ## 获取传感器数据单位
  CMD_GET_UNIT   =   0x0B  
  ## 获取传感器的SKU, SKU之间用逗号(,)分开
  CMD_GET_SKU    =   0x0C  
  ## 获取传感器的数据名，值和单位名，值和单位名之间空一格，其他用逗号(,)分开
  CMD_GET_INFO   =   0x0D  
  ## 根据数据名获取对应的数据的值
  CMD_GET_KEY_VALUE0  =  0x0E  
  ## 根据数据名获取对应的数据的值
  CMD_GET_KEY_VALUE1  =  0x0F
  ## 根据数据名获取对应的数据的值  
  CMD_GET_KEY_VALUE2  =  0x10  
  ## 根据数据名获取对应的数据的单位
  CMD_GET_KEY_UINT0   =  0x11  
   ## 根据数据名获取对应的数据的单位
  CMD_GET_KEY_UINT1   =  0x12 
  ## 根据数据名获取对应的数据的单位
  CMD_GET_KEY_UINT2   =  0x13  
  ## 复位I2C从机发送缓存命令
  CMD_RESET           =  0x14 
  ## 获取传感器转接板支持的Analog传感器SKU命令 
  CMD_SKU_A           =  0x15  
  ## 获取传感器转接板支持的Digital传感器SKU命令
  CMD_SKU_D           =  0x16  
  ## 获取传感器转接板支持的I2C传感器SKU命令
  CMD_SKU_IIC         =  0x17  
  ## 获取传感器转接板支持的UART传感器SKU命令
  CMD_SKU_UART        =  0x18  
  CMD_END             = CMD_SKU_UART
  ## 响应成功状态   
  STATUS_SUCCESS      = 0x53  
  ## 响应失败状态 
  STATUS_FAILED       = 0x63  

  DEBUG_TIMEOUT_MS    = 1 #1s

  ## 通信正常
  ERR_CODE_NONE            =   0x00 
  ## 无效命令
  ERR_CODE_CMD_INVAILED    =   0x01 
  ## 响应包错误
  ERR_CODE_RES_PKT         =   0x02 
  ## I2C主机内存不够
  ERR_CODE_M_NO_SPACE      =   0x03 
  ## 响应包接收超时
  ERR_CODE_RES_TIMEOUT     =   0x04 
  ## 无效的命令包或者命令不匹配
  ERR_CODE_CMD_PKT         =   0x05 
  ## 从机故障
  ERR_CODE_SLAVE_BREAK     =   0x06
  ## 设置的参数错误 
  ERR_CODE_ARGS            =   0x07 
  ## 该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
  ERR_CODE_SKU             =   0x08 
  ## I2C从机内存不够
  ERR_CODE_S_NO_SPACE      =   0x09 
  ## I2C地址无效
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
  
  def __init__(self):
    pass
  
  def begin(self):
    '''!
      @brief 传感器通用适配器板(Sensor Universal Adapter Board)初始化，旨在初始化通信接口
      @param freq 设置通信频率
      @return int 初始化状态
      @n       0      初始化成功
      @n      others  初始化失败
    '''
    self._reset(self.CMD_RESET)
    return 0
  
  def adjust_rtc_datetime(self):
    '''!
      @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的日期和时间为树莓派的当前时间
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
      @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的年月日时分秒周等日期
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
      @brief @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)的年月日时分秒周等日期
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

  def set_IF0_mode(self, mode):
    '''!
      @brief 配置接口0(A&D)的传感器模式
      @param mode  eADIFMode_t枚举变量
      @n     eAnalogMode    模拟传感器模式
      @n     eDigitalMode   数字传感器模式
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
    '''
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF0
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = mode
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF0)
    return recv_pkt[self.INDEX_RES_ERR]

  def set_IF0_sku(self, sku):
    '''!
      @brief 配置接口0(A&D)的SKU
      @param sku  模拟传感器或者数字传感器的7位SKU代码
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
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

  def set_IF0_mode_sku(self, mode, sku):
    '''!
      @brief 配置接口0(A&D)的接口模式，以及所对应的SKU
      @param mode  eADIFMode_t枚举变量
      @n     eAnalogMode  或 0   模拟传感器模式
      @n     eDigitalMode 或 1   数字传感器模式
      @param sku  模拟传感器或者数字传感器的7位SKU代码
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
      @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
    '''
    length = len(sku) + 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF0
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = mode
    i = 1
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF0)
    return recv_pkt[self.INDEX_RES_ERR]

  def set_IF1_mode(self, mode):
    '''!
      @brief 配置接口1(I2C&UART1)的传感器模式
      @param mode  eI2CUARTMode_t 枚举变量
      @n     eI2CMode    I2C传感器模式
      @n     eUARTMode   UART传感器模式
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
    '''
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF1
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = mode
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF1)
    return recv_pkt[self.INDEX_RES_ERR]

  def set_IF1_sku(self, sku):
    '''!
      @brief 配置接口1(I2C&UART1)的SKU
      @param sku  I2C传感器或者UART传感器的7位SKU代码
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
      @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
    '''
    length = len(sku)
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF1
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    i = 0
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF1)
    return recv_pkt[self.INDEX_RES_ERR]

  def set_IF1_mode_sku(self, mode, sku):
    '''!
      @brief 配置接口1(I2C&UART1)的接口模式，以及所对应的SKU
      @param mode  eI2CUARTMode_t 枚举变量
      @n     eI2CMode    I2C传感器模式
      @n     eUARTMode   UART传感器模式
      @param sku  I2C传感器或者UART传感器的7位SKU代码
      @return  错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
      @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
      @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
      @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
    '''
    length = len(sku) + 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF1
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = mode
    i = 1
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF1)
    return recv_pkt[self.INDEX_RES_ERR]

  def set_IF2_mode(self, mode):
    '''!
     @brief 配置接口2(I2C&UART2)的传感器模式
     @param mode  eI2CUARTMode_t 枚举变量
     @n     eI2CMode    I2C传感器模式
     @n     eUARTMode   UART传感器模式
     @return  错误代码
     @n      ERR_CODE_NONE         or 0x00  设置成功
     @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
     @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
     @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
     @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
     @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
     @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
     @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
    '''
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF2
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = mode
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF2)
    return recv_pkt[self.INDEX_RES_ERR]

  def set_IF2_sku(self, sku):
    '''!
      @brief 配置接口2(I2C&UART2)的SKU
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
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
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

  def set_IF2_mode_sku(self, mode, sku):
    '''!
      @brief 配置接口2(I2C&UART2)的接口模式，以及所对应的SKU
      
      @param mode  传感器模式
      @n     eI2CMode    I2C传感器模式
      @n     eUARTMode   UART传感器模式
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
      @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
      @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
    '''
    length = len(sku) + 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_SET_IF2
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = mode
    i = 1
    for c in sku:
      pkt[self.INDEX_ARGS + i] = ord(c)
      i += 1
    
    #print(pkt)
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_SET_IF2)
    return recv_pkt[self.INDEX_RES_ERR]

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

  def get_IF0_config(self):
    '''!
      @brief 获取接口0(I2C&UART2)的传感器模式，及SKU配置
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
        rslt[self.INDEX_SKU] += '\0'
    return rslt

  def get_IF1_config(self):
    '''!
      @brief 获取接口1(I2C&UART2)的传感器模式，及SKU配置
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
        rslt[self.INDEX_SKU] += '\0'
    return rslt

  def get_IF2_config(self):
    '''!
      @brief 获取接口2(I2C&UART2)的传感器模式，及SKU配置
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
        rslt[self.INDEX_SKU] += '\0'
    return rslt

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
      @brief 开启传感器通用适配器板(Sensor Universal Adapter Board)屏显示
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
      @brief 关闭传感器通用适配器板(Sensor Universal Adapter Board)屏显示
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

  def get_information(self, inf):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的属性项(属性名称:数据值 单位)信息，属性项与属性项之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     eAD                                           指定A&D接口，获取A&D接口上所连接的所有传感器的属性项
      @n     eI2C_UART1                                    指定I2C&UART1接口，获取I2C&UART1接口上所连接的所有传感器的属性项
      @n     eI2C_UART2                                    选中I2C&UART2接口，获取I2C&UART2接口上所连接的所有传感器的属性项
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，获取所有接口上所连接的所有传感器的属性项
      @return 传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的属性项
      @n 例 SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
    '''
    rslt = ""
    length = 1
    pkt = [0] * (3 + length)
    pkt[self.INDEX_CMD]        = self.CMD_GET_INFO
    pkt[self.INDEX_ARGS_NUM_L] = length & 0xFF
    pkt[self.INDEX_ARGS_NUM_H] = (length >> 8) & 0xFF
    pkt[self.INDEX_ARGS]       = inf
    self._send_packet(pkt)

    recv_pkt = self._recv_packet(self.CMD_GET_INFO)
    if (len(recv_pkt) >= 5) and (recv_pkt[self.INDEX_RES_ERR] == self.ERR_CODE_NONE and recv_pkt[self.INDEX_RES_STATUS] == self.STATUS_SUCCESS):
      length = recv_pkt[self.INDEX_RES_LEN_L] | (recv_pkt[self.INDEX_RES_LEN_H] << 8)
      if length:
        for data in recv_pkt[self.INDEX_RES_DATA:]:
          rslt += chr(data)
        rslt += '\0'
    return rslt

  def get_sku(self, inf):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的SKU，SKU与SKU之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     eAD                                           指定A&D接口，获取A&D接口上所连接的所有传感器的SKU
      @n     eI2C_UART1                                    指定I2C&UART1接口，获取I2C&UART1接口上所连接的所有传感器的SKU
      @n     eI2C_UART2                                    选中I2C&UART2接口，获取I2C&UART2接口上所连接的所有传感器的SKU
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，获取所有接口上所连接的所有传感器的SKU
      @return 传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的SKU
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
        rslt += '\0'
    return rslt

  def get_keys(self, inf):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的所有属性名，属性名与属性名之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     eAD                                           指定A&D接口，获取A&D接口上所连接的所有传感器的所有属性名
      @n     eI2C_UART1                                    指定I2C&UART1接口，获取I2C&UART1接口上所连接的所有传感器的所有属性名
      @n     eI2C_UART2                                    选中I2C&UART2接口，获取I2C&UART2接口上所连接的所有传感器的所有属性名
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，获取所有接口上所连接的所有传感器的所有属性名
      @return 传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的所有属性名
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
        rslt += '\0'
    return rslt

  def get_values(self, inf):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的所有属性数据值，数据值与数据值之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     eAD                                           指定A&D接口，获取A&D接口上所连接的所有传感器的所有属性数据值
      @n     eI2C_UART1                                    指定I2C&UART1接口，获取I2C&UART1接口上所连接的所有传感器的所有属性数据值
      @n     eI2C_UART2                                    选中I2C&UART2接口，获取I2C&UART2接口上所连接的所有传感器的所有属性数据值
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，获取所有接口上所连接的所有传感器的所有属性数据值
      @return 传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的所有属性数据值
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
        rslt += '\0'
    return rslt

  def get_units(self, inf):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的所有属性单位，单位与单位之间用','号隔开
      @param inf 指定一个或多个接口参数
      @n     eAD                                           指定A&D接口，获取A&D接口上所连接的所有传感器的所有属性单位
      @n     eI2C_UART1                                    指定I2C&UART1接口，获取I2C&UART1接口上所连接的所有传感器的所有属性单位
      @n     eI2C_UART2                                    选中I2C&UART2接口，获取I2C&UART2接口上所连接的所有传感器的所有属性单位
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，获取所有接口上所连接的所有传感器的所有属性单位
      @return 传感器通用适配器板(Sensor Universal Adapter Board)上指定的一个或多个接口上所连接的所有传感器的所有属性单位
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
        rslt += '\0'
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
        rslt += '\0'
    return rslt

  def get_value1(self, inf, keys):
    '''!
      @brief 获取指定接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     eAD                                           选中A&D接口，在A&D接口所连接的传感器中查找属性名称为keys的属性值
      @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口所连接的传感器中查找属性名称为keys的属性值
      @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口所连接的传感器中查找属性名称为keys的属性值
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性值
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
        rslt += '\0'
    return rslt

  def get_value2(self, inf, sku, keys):
    '''!
      @brief 获取指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     eAD                                           选中A&D接口，在A&D接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
      @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
      @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
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
        rslt += '\0'
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
        rslt += '\0'
    return rslt

  def get_unit1(self, inf, keys):
    '''!
      @brief 获取指定接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     eAD                                           选中A&D接口，在A&D接口所连接的传感器中查找属性名称为keys的属性单位
      @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口所连接的传感器中查找属性名称为keys的属性单位
      @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口所连接的传感器中查找属性名称为keys的属性单位
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性单位
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
        rslt += '\0'
    return rslt

  def get_unit2(self, inf, sku, keys):
    '''!
      @brief 获取指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @param inf    接口选择，及参数查找范围
      @n     eAD                                           选中A&D接口，在A&D接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
      @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
      @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
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
        rslt += '\0'
    return rslt

  def get_analog_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)Analog系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)Analog系列传感器的SKU支持列表，如果没有则返回NULL
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
        rslt += '\0'
    return rslt
  
  def get_digital_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)Digital系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)Digital系列传感器的SKU支持列表，如果没有则返回NULL
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
        rslt += '\0'
    return rslt

  def get_i2c_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)I2C系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)I2C系列传感器的SKU支持列表，如果没有则返回NULL
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
        rslt += '\0'
    return rslt

  def get_uart_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)UART系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)UART系列传感器的SKU支持列表，如果没有则返回NULL
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
        rslt += '\0'
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
      @brief 复位传感器通用适配器板(Sensor Universal Adapter Board)的发送缓存
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


class DFRobot_SUAB_IIC(DFRobot_SUAB):
  def __init__(self,addr):
    '''!
      @brief DFRobot_SUAB_IIC构造函数
      @param addr:  7-bit IIC address, 范围1~127，默认0x05
    '''
    self._addr = addr
    self._bus = smbus.SMBus(1)
    DFRobot_SUAB.__init__(self)
    
  def get_i2c_address(self):
    '''!
      @brief 获取通用适配器板(Sensor Universal Adapter Board)的I2C通信地址
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
      @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C通信地址 
      @param addr 传感器通用适配器板(Sensor Universal Adapter Board)的I2C通信地址，范围1~0x7F
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