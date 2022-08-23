# DFRobot_RP2040_SUAB

* [中文版](./README_CN.md)

传感器通用适配器板(Sensor Universal Adapter Board)是DFRobot设计的一款传感器转接板，它能够连接DFRobot的模拟、数字、I2C、UART等传感器，并将传感器采集到的数据转换为 名称+数据+单位的格式，供主控读取，或显示在板载的显示屏上供用户查看。看到这里，相信很多人都对它的使用有疑问，接下来我就用问答的方式来详细的介绍这块板子的功能: <br>
* 问题1. DFRobot有那么多传感器，这块板子都能识别么？
  答：不是哦，目前这个板子只支持了DFRobot的部分传感器，用户可以通过README的SKU支持列表、板载的按钮和屏的交互界面查看SKU Select、或通过主控读取等方式获取各类型传感器的支持列表。
* 问题2：我想使用的模拟、数字、I2C或UART传感器不在支持列表里面怎么办?
  答：完全不用担心这个问题，传感器通用适配器板(Sensor Universal Adapter Board)有U盘固件升级的功能，你可以给我们留言，我们会将该传感器加入支持列表中，后续只要通过这个U盘固件升级功能烧录最新的固件就可以了。
* 问题3: 传感器通用适配器板(Sensor Universal Adapter Board)能识别不同的传感器的原理是什么呢？
  答：DFRobot每个传感器都有一个唯一的SKU，适配器板通过自动识别或用户选择的SKU来识别连接的是那个传感器，并调用相应的驱动程序来采集和转换数据。（注意：除部分I2C传感器可以通过I2C地址识别SKU外，其他的传感器只能通过用户手动选择SKU，告诉适配器板连接的是哪个传感器）
* 问题4：传感器通用适配器板(Sensor Universal Adapter Board)和这些传感器之间是通过什么连接的呢？
  答：适配器板上板载了1个Gravity 3pin的模拟/数字切换接口(A&D 连接模拟或数字传感器),以及2个Gravity 4pin的I2C/UART接口(I2C&UART 连接I2C或UART传感器), 用户可以通过切换对应接口的模式来连接相应的传感器。
* 问题5：板载的按钮和屏交互界面有什么用呢?
  答: 用户可以通过这些配置和查看传感器通用适配器板(Sensor Universal Adapter Board)的参数，比如I2C从机地址，时间，接口模式切换，选择SKU，固件版本，传感器数据。
* 问题6：如何用Arduino主控或树莓派读取和设置传感器通用适配器板(Sensor Universal Adapter Board)的参数，以及读取传感器数据呢?
  答：传感器通用适配器板(Sensor Universal Adapter Board)板载了一个Gravity I2C接口，主控可以通过这个接口操作适配器板。
* 问题7：通用适配器板(Sensor Universal Adapter Board)上的USB有什么用呢？
  答：固件升级或导出CSV文件。按住boot键上电进入U盘固件升级模式，可以升级固件，直接上电会弹出一个U盘，用户可以在这里查看或导出记录传感器数据的CSV文件。

![产品效果图](../../resources/images/SEN0443.png)


## Product Link（[https://www.dfrobot.com](https://www.dfrobot.com)）
    SKU: DFR0999
## Supported Analog SKU
* SEN0161 
* SEN0175 

## Supported Digital SKU
* NULL 

## Supported I2C SKU
* SEN0228 
* SEN0497 

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
这是一个基于python平台的传感器通用适配器板(Sensor Universal Adapter Board)库。旨在为用户提供一系列接口函数去设置和读取该适配器板的参数，以及读取适配器板上各传感器的数据，它具有以下功能：<br>
* 1. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C地址，范围0x01~0x7F；
* 2. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的年，月，日，时，分，秒的时间；
* 3. 开启/关闭传感器数据CSV文件记录；
* 4. 开启/关闭屏显示
* 5. 读取和设置接口传感器模式，以及SKU
* 6. 以读取传感器数据(名称+数值+单位)
* 7. 读取模拟、数字、I2C、UART等类型传感器的SKU支持列表   
```python
> sudo nano boot/config.txt
dtparam=i2c_arm=on,i2c_arm_baudrate=100000
> sudo reboot
```

## Installation
1. To use this library, first download the library file<br>
```python
sudo git clone https://github.com/DFRobot/DFRobot_RP2040_SUAB
```
2. Open and run the routine. To execute a routine demo_x.py, enter python demo_x.py in the command line. For example, to execute the demo_config.py routine, you need to enter :<br>

```python
python demo_config.py 
或 
python2 demo_config.py 
或 
python3 demo_config.py
```


## Methods

```python
  def begin(self):
    '''!
      @brief 传感器通用适配器板(Sensor Universal Adapter Board)初始化，旨在初始化通信接口
      @param freq 设置通信频率
      @return int 初始化状态
      @n       0      初始化成功
      @n      others  初始化失败
    '''
  
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

  def get_rtc_time(self):
    '''!
      @brief @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)的年月日时分秒周等日期
      @return 长度为2的列表
      @n      列表中第0个元数: 列表年，月，日，星期，时，分，秒[年，月，日，星期，时，分，秒]
      @n      列表中第2个元数: 字符串，年/月/日 星期 时:分:秒 例: 2022/08/09 2 09:08:00
    '''

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

  def get_IF0_config(self):
    '''!
      @brief 获取接口0(I2C&UART2)的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
    '''

  def get_IF1_config(self):
    '''!
      @brief 获取接口1(I2C&UART2)的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
    '''

  def get_IF2_config(self):
    '''!
      @brief 获取接口2(I2C&UART2)的传感器模式，及SKU配置
      @return 列表
      @n      列表中第0个元素： 错误代码
      @n      列表中第1个元素： 传感器模式
      @n      列表中第2个元素： sku配置
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
      @brief 开启传感器通用适配器板(Sensor Universal Adapter Board)屏显示
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
      @brief 关闭传感器通用适配器板(Sensor Universal Adapter Board)屏显示
      @return 错误代码
      @n      ERR_CODE_NONE         or 0x00  设置成功
      @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
      @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
      @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
      @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
    '''

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
      @n     eAD                                           选中A&D接口，在A&D接口所连接的传感器中查找属性名称为keys的属性值
      @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口所连接的传感器中查找属性名称为keys的属性值
      @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口所连接的传感器中查找属性名称为keys的属性值
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性值
      @param keys  传感器属性名称
      @return 指定接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
      @n 例Temp_Air:  28.65,28.65
    '''

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
      @n     eAD                                           选中A&D接口，在A&D接口所连接的传感器中查找属性名称为keys的属性单位
      @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口所连接的传感器中查找属性名称为keys的属性单位
      @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口所连接的传感器中查找属性名称为keys的属性单位
      @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性单位
      @param keys  传感器属性名称
      @return 指定接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
      @n 例Temp_Air:  C,C
    '''

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

  def get_analog_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)Analog系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)Analog系列传感器的SKU支持列表，如果没有则返回NULL
    '''
  
  def get_digital_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)Digital系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)Digital系列传感器的SKU支持列表，如果没有则返回NULL
    '''

  def get_i2c_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)I2C系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)I2C系列传感器的SKU支持列表，如果没有则返回NULL
    '''

  def get_uart_sensor_sku(self):
    '''!
      @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)UART系列传感器的SKU支持列表
      @return 传感器通用适配器板(Sensor Universal Adapter Board)UART系列传感器的SKU支持列表，如果没有则返回NULL
    '''

class DFRobot_SUAB_IIC(DFRobot_SUAB):
  def __init__(self,addr):
    '''!
      @brief DFRobot_SUAB_IIC构造函数
      @param addr:  7-bit IIC address, 范围1~127，默认0x05
    '''
    
  def get_i2c_address(self):
    '''!
      @brief 获取通用适配器板(Sensor Universal Adapter Board)的I2C通信地址
      @return I2C通信地址
    '''
    
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





