# DFRobot_RP2040_SCI

* [中文版](./README_CN.md)

This SCI acquisition module is a multi-functional data acquisition module designed by DFRobot. It supports all kinds of digital, analog, I2C, and UART sensors from DFRobot. The module is capable of standardizing sensor output into the format of name+data+unit, which then can be read by main controllers or displayed on the onboard display so users can view it. The following demonstrates more details about this product through Q&A. <br/>
* Q1: DFRobot has so many sensors, so can this board support all of them? 
  A: Sorry, it can't. This board only supports part of DFRobot's sensors currently. You can check the supported product list on the library Readme, SKU select on display, or read sensor type through a controller.
* Q2: What if the analog, digital, I2C or UART sensor I want to use is not in the supported SKU list?
  A: Don't worry about it. The SCI Acquisition Module features USB firmware upgrading function. Please leave us comments and we'll add the sensor to the list. Then it will be available once you upgrade your firmware to the latest.
* Q3: How does the SCI Acquisition module recognize different sensors? 
  A: Each sensor from DFRobot has a unique SKU. The module can identify the connected sensor through automatic identification or the user-selected SKU, and call the corresponding driver to acquire and convert data. (Note: For some I2C sensors, the adapter can identify the SKU by I2C address, but for the others, it can only identify the connected one by user-selected SKU.)
* Q4: How is the SCI Acquisition Module connected to these sensors?
  A: The module has an onboard Gravity 3pin analog/digital interface (for connecting analog or digital sensors) and 2 Gravity 4pin I2C/UART interfaces (for connecting I2C or UART sensors), so users can connect the corresponding sensor by switching to the corresponding interface mode.
* Q5: What's the onboard display and button used for? 
  A: Users can configure or view the module parameters such as I2C slave address, time, switchable interface mode, SKU select, firmware version, and sensor data by the onboard display and buttons.
* Q6: How can I use Arduino or Raspberry Pi to read and set parameters of the SCI Acquisition Module, and read the sensor data?
  Connect your controller to the acquisition module via the onboard Gravity I2C interface, and then you can operate the module. Find more details on [the wiki page](https://wiki.dfrobot.com/SKU_DFR0999_Gravity_SCI_Acquisition_Module). 
* Q7: What's the USB on the module used for? 
  It's used for firmware upgrading or CSV file export. Press the boot button and power on the module to enter the firmware upgrading mode, then you can upgrade the firmware. When it's powered on directly, a U-disk will pop up on your PC and you can view or export the CSV file of recorded sensor data there. 

![Product Image](../../resources/images/SEN0443.png)


## Product Link（[https://www.dfrobot.com](https://www.dfrobot.com)）
    SKU: DFR0999   
## Supported Analog SKU
* SEN0161 
* SEN0232
* SEN0244
* SEN0231
* SEN0193
* DFR0300


## Supported Digital SKU
* KIT0021

## Supported I2C SKU
* SEN0497
* SEN0514
* SEN0334
* SEN0228
* DFR0216
* SEN0322 
* SEN0364 
* SEN0517
* SEN0456
* SEN0529
* KIT0176
* SEN0304
* SEN0321 
* SEN0498
* SEN0460
* SEN0206
* SEN0291
* SEN0536

## Supported UART SKU
* NULL  

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary
This is an Arduino library for the DFRobot SCI Acquisition module. It aims to provide users with a series of interface functions to set and read module parameters or read sensor data. Its functions are as follows: <br>
* 1. Read/set the I2C address of SCI Acquisition Module within the range of 0x01-0x7F;
* 2. Read/set the time information of year, month, day, hour, minute and second of SCI Acquisition Module;
* 3. Enable/disable sensor data record of CSV file;
* 4. Enable/disable the display;
* 5. Read/set the interface mode and SKU of the sensor;
* 6. Read sensor data (name + value + unit);
* 7. Read the supported product SKU list, including, analog, digital, I2C, UART and other types of sensors;

```python
> sudo nano boot/config.txt
dtparam=i2c_arm=on,i2c_arm_baudrate=100000
> sudo reboot
```

## Installation
1. To use this library, first download the library file<br>
```python
sudo git clone https://github.com/DFRobot/DFRobot_RP2040_SCI
```
2. Open and run the routine. To execute a routine demo_x.py, enter python demo_x.py in the command line. For example, to execute the demo_config.py routine, you need to enter :<br>

```python
python demo_config.py 
or 
python2 demo_config.py 
or 
python3 demo_config.py
```


## Methods

```python
class DFRobot_RP2040_SCI_IIC(DFRobot_SCI):
  def __init__(self,addr):
    '''!
      @brief DFRobot_SCI_IIC 构造函数
      @param addr:  7-bit IIC address，支持以下地址设置
      @n RP2040_SCI_ADDR_0X21      0x21 转换板默认I2C地址
      @n RP2040_SCI_ADDR_0X22      0x22
      @n RP2040_SCI_ADDR_0X23      0x23
    '''
    
  def get_i2c_address(self):
    '''!
      @brief 获取SCI采集模块(SCI Acquisition Module)的I2C通信地址
      @return I2C通信地址
    '''
  
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
class DFRobot_SCI:
  def begin(self):
    '''!
      @brief SCI采集模块(SCI Acquisition Module)初始化，旨在初始化通信接口
      @param freq 设置通信频率
      @return int 初始化状态
      @n       0      初始化成功
      @n      others  初始化失败
    '''
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
  def get_version_description(self, version):
    '''!
      @brief 获取版本描述字符串
      @return 返回版本描述字符串，例版本id：0x0123返回的版本描述字符串为 V1.2.3
    '''
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
  
  def get_port1(self):
    '''!
      @brief 获取Port1接口的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
    '''
  
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

  def get_port2(self):
    '''!
      @brief 获取Port2的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
    '''

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

  def get_port3(self):
    '''!
      @brief 获取Port3接口的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
    '''

  def set_recv_timeout(self,timeout = 2):
    '''!
      @brief SCI采集模块(SCI Acquisition Module)初始化，旨在初始化通信接口
      @param freq 设置通信频率
      @return int 初始化状态
      @n       0      初始化成功
      @n      others  初始化失败
    '''
    
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

  def get_rtc_time(self):
    '''!
      @brief @brief 获取SCI采集模块(SCI Acquisition Module)的年月日时分秒周等日期
      @return 长度为2的列表
      @n      列表中第0个元数: 列表年，月，日，星期，时，分，秒[年，月，日，星期，时，分，秒]
      @n      列表中第2个元数: 字符串，年/月/日 星期 时:分:秒 例: 2022/08/09 2 09:08:00
    '''
  
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

  def get_refresh_rate_describe(self, rate):
    '''!
      @brief 获取刷新率的描述，单位s
    '''
    
  def get_timestamp(self):
    '''!
      @brief 获取时间戳,此时间戳为(SCI Acquisition Module)数据刷新时间
      @return 时:分:秒(00:00:00) 或 分:秒.百分之（0~99）秒(00:00.00)
    '''

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

  def get_value0(self, keys):
    '''!
      @brief 获取所有接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @param keys  传感器属性名称
      @return 所有接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @n 例Temp_Air:  28.65,28.65
    '''

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

  def get_unit0(self, keys):
    '''!
      @brief 获取所有接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @param keys  传感器属性名称
      @return 所有接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @n 例Temp_Air:  C,C
    '''

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

  def get_analog_sensor_sku(self):
    '''!
      @brief 获取SCI采集模块(SCI Acquisition Module)Analog系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)Analog系列传感器的SKU支持列表，如果没有则返回NULL
    '''
  
  def get_digital_sensor_sku(self):
    '''!
      @brief 获取SCI采集模块(SCI Acquisition Module)Digital系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)Digital系列传感器的SKU支持列表，如果没有则返回NULL
    '''

  def get_i2c_sensor_sku(self):
    '''!
      @brief 获取SCI采集模块(SCI Acquisition Module)I2C系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)I2C系列传感器的SKU支持列表，如果没有则返回NULL
    '''

  def get_uart_sensor_sku(self):
    '''!
      @brief 获取SCI采集模块(SCI Acquisition Module)UART系列传感器的SKU支持列表
      @return SCI采集模块(SCI Acquisition Module)UART系列传感器的SKU支持列表，如果没有则返回NULL
    '''
```

## Compatibility

| 主板         | 通过 | 未通过 | 未测试 | 备注 |
| ------------ | :--: | :----: | :----: | :--: |
| RaspberryPi2 |      |        |   √    |      |
| RaspberryPi3 |      |        |   √    |      |
| RaspberryPi4 |  √   |        |        |      |

* Python 版本

| Python  | 通过 | 未通过 | 未测试 | 备注 |
| ------- | :--: | :----: | :----: | ---- |
| Python2 |  √   |        |        |      |
| Python3 |  √   |        |        |      |

## History

- 2021/08/19 - Version 1.0.0 released.

## Credits

Written by Arya(xue.peng@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))





