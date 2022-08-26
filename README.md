DFRobot_RP2040_SUAB
===========================
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

![产品效果图](./resources/images/SEN0443.png)


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
这是一个基于Arduino平台的传感器通用适配器板(Sensor Universal Adapter Board)库。旨在为用户提供一系列接口函数去设置和读取该适配器板的参数，以及读取适配器板上各传感器的数据，它具有以下功能：<br>
* 1. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C地址，范围0x01~0x7F；
* 2. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的年，月，日，时，分，秒的时间；
* 3. 开启/关闭传感器数据CSV文件记录；
* 4. 开启/关闭屏显示
* 5. 读取和设置接口传感器模式，以及SKU
* 6. 以读取传感器数据(名称+数值+单位)
* 7. 读取模拟、数字、I2C、UART等类型传感器的SKU支持列表
               |  

## Installation

There two methods: 
1. To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.
2. Search the DFRobot_RP2040_SUAB library from the Arduino Software Library Manager and download it.

## Methods

```C++
  /**
   * @fn DFRobot_RP2040_SUAB_IIC
   * @brief DFRobot_RP2040_SUAB_IIC类的构造函数.
   * @param addr:  7位I2C地址，范围1~127（0x01~0x7F），如果你不知道该填什么，可以调用demo(i2cDetect.ino)来扫描板子的I2C地址
   * @n 或通过板子的OLED屏的初始页查看I2C地址，出厂默认I2C地址为0x01
   * @param pWire:   TwoWire类对象指针.
   */
  DFRobot_RP2040_SUAB_IIC(uint8_t addr = RP2040_SUAB_DEF_I2C_ADDR, TwoWire *pWire = &Wire);
  ~DFRobot_RP2040_SUAB_IIC();
  /**
   * @fn setI2CAddress
   * @brief 设置传感器通用适配器板的I2C通信地址
   * 
   * @param addr    传感器通用适配器板(Sensor Universal Adapter Board)的I2C通信地址，范围1~0x7F
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配 
   * @n      ERR_CODE_I2C_ADRESS   or 0x0A  I2C地址无效
   */
  uint8_t setI2CAddress(uint8_t addr);
  /**
   * @fn getI2CAddress
   * @brief 获取通用适配器板(Sensor Universal Adapter Board)的I2C通信地址
   * @return I2C通信地址
   */
  uint8_t getI2CAddress();
  /**
   * @fn begin
   * @brief 传感器通用适配器板(Sensor Universal Adapter Board)初始化，旨在初始化通信接口
   * 
   * @param freq 设置通信频率,不能超过100kHz
   * @return int 初始化状态
   * @n       0  初始化成功
   * @n      -1  通信接口类对象未传入
   * @n      -2  请检测硬件连接是否正确
   */
  int begin(uint32_t freq = 100000);
  /**
   * @fn setRecvTimeout
   * @brief 设置接收超时时间
   * 
   * @param timeout 当传感器通用适配器板(Sensor Universal Adapter Board)连接的传感器较多时，在读取大量数据时需要适当提高接收超时时间，默认2s
   */
  void setRecvTimeout(uint32_t timeout = 2000);
  /**
   * @fn adjustRtc(const __FlashStringHelper* date, const __FlashStringHelper* time)
   * @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的时间
   * 
   * @param date 年月日
   * @param time 时分秒
   * @return 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t adjustRtc(const __FlashStringHelper* date, const __FlashStringHelper* time);

	/**
   * @fn adjustRtc(uint16_t year, uint8_t month, uint8_t day, uint8_t week, uint8_t hour, uint8_t minute, uint8_t second)
   * @brief 设置传感器通用适配器板(Sensor Universal Adapter Board)的时间
   * 
   * @param year   年
   * @param month  月
   * @param day    日
   * @param week   周
   * @param hour   时
   * @param minute 分
   * @param second 秒
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t adjustRtc(uint16_t year, uint8_t month, uint8_t day, uint8_t week, uint8_t hour, uint8_t minute, uint8_t second);
  /**
   * @fn getRtcTime(uint16_t *year, uint8_t *month, uint8_t *day, uint8_t *week, uint8_t *hour, uint8_t *minute, uint8_t *second)
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)的年月日时分秒周等日期
   * 
   * @param year   年
   * @param month  月
   * @param day    日
   * @param week   周
   * @param hour   时
   * @param minute 分
   * @param second 秒
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t getRtcTime(uint16_t *year, uint8_t *month, uint8_t *day, uint8_t *week, uint8_t *hour, uint8_t *minute, uint8_t *second);
  /**
   * @fn getRtcTime()
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)的年月日时分秒周等日期
   * 
   * @return 年/月/日 周 时:分:秒表示的字符串，例 2022/08/09 2 09:08:00 2022年8月9日，星期二 9点8分0秒
   */
  String getRtcTime();

  /**
   * @fn setIF0(eADIFMode_t mode)
   * @brief 配置接口0(A&D)的传感器模式
   * 
   * @param mode  eADIFMode_t枚举变量
   * @n     eAnalogMode    模拟传感器模式
   * @n     eDigitalMode   数字传感器模式
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   */
  uint8_t setIF0(eADIFMode_t mode);
  /**
   * @fn setIF0(char sku[7])
   * @brief 配置接口0(A&D)的SKU
   * 
   * @param sku  模拟传感器或者数字传感器的7位SKU代码,,可以通过 getAnalogSensorSKU/getDigitalSensorSKU 函数获取支持的SKU代码
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   * @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
   * @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
   */
  uint8_t setIF0(char sku[7]);
  /**
   * @fn setIF0(char sku[7])
   * @brief 配置接口0(A&D)的接口模式，以及所对应的SKU
   * 
   * @param mode  eADIFMode_t枚举变量
   * @n     eAnalogMode  或 0   模拟传感器模式
   * @n     eDigitalMode 或 1   数字传感器模式
   * @param sku  模拟传感器或者数字传感器的7位SKU代码,,可以通过 getI2CSensorSKU/getUARTSensorSKU 函数获取支持的SKU代码
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   * @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
   * @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
   */
  uint8_t setIF0(eADIFMode_t mode, char sku[7]);
 
  /**
   * @fn setIF1(eI2CUARTMode_t mode)
   * @brief 配置接口1(I2C&UART1)的传感器模式
   * 
   * @param mode  eI2CUARTMode_t 枚举变量
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   */
  uint8_t setIF1(eI2CUARTMode_t mode);
  /**
   * @fn setIF1(char sku[7])
   * @brief 配置接口1(I2C&UART1)的SKU
   * 
   * @param sku  I2C传感器或者UART传感器的7位SKU代码,可以通过 getI2CSensorSKU/getUARTSensorSKU 函数获取支持的SKU代码
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   * @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
   * @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
   */
  uint8_t setIF1(char sku[7]);
  /**
   * @fn setIF1(eI2CUARTMode_t mode, char sku[7])
   * @brief 配置接口1(I2C&UART1)的接口模式，以及所对应的SKU
   * 
   * @param mode  eI2CUARTMode_t 枚举变量
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @param sku  I2C传感器或者UART传感器的7位SKU代码,,可以通过 getI2CSensorSKU/getUARTSensorSKU 函数获取支持的SKU代码
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   * @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
   * @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
   */
  uint8_t setIF1(eI2CUARTMode_t mode, char sku[7]);
  /**
   * @fn setIF2(eI2CUARTMode_t mode)
   * @brief 配置接口2(I2C&UART2)的传感器模式
   * 
   * @param mode  eI2CUARTMode_t 枚举变量
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   */
  uint8_t setIF2(eI2CUARTMode_t mode);
  /**
   * @fn setIF2(char sku[7])
   * @brief 配置接口2(I2C&UART2)的SKU
   * 
   * @param sku  I2C传感器或者UART传感器的7位SKU代码,可以通过 getI2CSensorSKU/getUARTSensorSKU 函数获取支持的SKU代码
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   * @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
   * @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
   */
  uint8_t setIF2(char sku[7]);
  /**
   * @fn setIF2(eI2CUARTMode_t mode, char sku[7])
   * @brief 配置接口2(I2C&UART2)的接口模式，以及所对应的SKU
   * 
   * @param mode  eI2CUARTMode_t 枚举变量
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @param sku  I2C传感器或者UART传感器的7位SKU代码,可以通过 getI2CSensorSKU/getUARTSensorSKU 函数获取支持的SKU代码
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  从机故障
   * @n      ERR_CODE_ARGS         or 0x07  设置的参数错误
   * @n      ERR_CODE_SKU          or 0x08  该SKU为无效SKU，或者传感器通用适配器板(Sensor Universal Adapter Board)不支持
   * @n      ERR_CODE_S_NO_SPACE   or 0x09  I2C从机内存不够
   */
  uint8_t setIF2(eI2CUARTMode_t mode, char sku[7]);
  
  /**
   * @fn getSensorModeDescribe(eADIFMode_t mode)
   * @brief 获取传感器的模式描述
   * 
   * @param mode  eADIFMode_t枚举变量
   * @n     eAnalogMode    模拟传感器模式
   * @n     eDigitalMode   数字传感器模式
   * @return 传感器的模式描述字符串
   * @n      "ANALOG"         模拟传感器模式
   * @n      "DIGITAL"        数字传感器模式
   * @n      "UNKNOWN"        未知模式
   */
  String getSensorModeDescribe(eADIFMode_t mode);
  /**
   * @fn getSensorModeDescribe(eI2CUARTMode_t mode)
   * @brief 获取传感器的模式描述
   * 
   * @param mode  eI2CUARTMode_t 枚举变量
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return 传感器的模式描述字符串
   * @n      "I2C"         I2C传感器模式
   * @n      "UART"        UART传感器模式
   * @n      "UNKNOWN"     未知模式
   */
  String getSensorModeDescribe(eI2CUARTMode_t mode);
  
  /**
   * @fn getIF0Config(eADIFMode_t *mode)
   * @brief 获取接口0(A&D)的传感器模式，及SKU配置
   * 
   * @param mode  eADIFMode_t枚举变量指针
   * @n     eAnalogMode    模拟传感器模式
   * @n     eDigitalMode   数字传感器模式
   * @return 接口0连接的传感器的SKU
   * @n      "NULL"        表示接口0没有配置或连接传感器
   * @n      7位SKU        数字或模拟传感器对应的SKU
   */
  String getIF0Config(eADIFMode_t *mode);
  /**
   * @fn getIF1Config(eI2CUARTMode_t *mode)
   * @brief 获取接口1(I2C&UART1)的传感器模式，及SKU配置
   * 
   * @param mode  eI2CUARTMode_t 枚举变量指针
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return 接口0连接的传感器的SKU
   * @n      "NULL"        表示接口0没有配置或连接传感器
   * @n      7位SKU集合     I2C或UART传感器对应的SKU
   */
  String getIF1Config(eI2CUARTMode_t *mode);
  /**
   * @fn getIF2Config(eI2CUARTMode_t *mode)
   * @brief 获取接口2(I2C&UART2)的传感器模式，及SKU配置
   * 
   * @param mode  eI2CUARTMode_t 枚举变量指针
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return 接口0连接的传感器的SKU
   * @n      "NULL"        表示接口0没有配置或连接传感器
   * @n      7位SKU集合     I2C或UART传感器对应的SKU
   */
  String getIF2Config(eI2CUARTMode_t *mode);
  /**
   * @fn enableRecord
   * @brief 开启CSV文件记录，调用此命令后，会将传感器采集到的数据记录在以年月日时分秒命名的CSV文件中
   * 
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t enableRecord();
  /**
   * @fn disableRecord
   * @brief 关闭CSV文件记录，调用此命令后，会停止将传感器采集到的数据记录在以年月日时分秒命名的CSV文件中
   * 
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t disableRecord();
  
  /**
   * @fn oledScreenOn
   * @brief 开启传感器通用适配器板(Sensor Universal Adapter Board)屏显示
   * 
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t oledScreenOn();
  /**
   * @fn oledScreenOff
   * @brief 关闭传感器通用适配器板(Sensor Universal Adapter Board)屏显示
   * 
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t oledScreenOff();
  
  /**
   * @fn getInformation
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上一个或多个接口连接的传感器的信息，名称:数值 单位,多条信息之间
   * @n 用','号隔开
   * 
   * @param inf    接口选择
   * @n     eAD                                           选中A&D接口
   * @n     eI2C_UART1                                    选中I2C&UART1接口
   * @n     eI2C_UART2                                    选中I2C&UART2接口
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口
   * @return 选中的接口上连接的传感器的属性，每条属性格式为：名称:数值 单位，多条属性之间用','号隔开,单位和数值之间用空格隔开
   * @n 例SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
   */
  String getInformation(eInterfaceList_t inf = eALL);
  String getInformation(uint8_t inf);

  /**
   * @fn getSKU
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上一个或多个接口连接的传感器的SKU,多个SKU之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     eAD                                           选中A&D接口
   * @n     eI2C_UART1                                    选中I2C&UART1接口
   * @n     eI2C_UART2                                    选中I2C&UART2接口
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口
   * @return 选中的接口上连接的传感器的SKU，多个SKU之间用','号隔开,
   * @n 例:  SEN0161,SEN0334
   */
  String getSKU(eInterfaceList_t inf = eALL);
  String getSKU(uint8_t inf);

  /**
   * @fn getKeys
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上一个或多个接口连接的传感器的名称，各名称之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     eAD                                           选中A&D接口
   * @n     eI2C_UART1                                    选中I2C&UART1接口
   * @n     eI2C_UART2                                    选中I2C&UART2接口
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口
   * @return 选中的接口上连接的传感器的名称，各名称之间用','号隔开
   * @n 例:  Temp_Air,Humi_Air
   */
  String getKeys(eInterfaceList_t inf = eALL);
  String getKeys(uint8_t inf);
  /**
   * @fn getValues
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上一个或多个接口连接的传感器的属性值，各属性值之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     eAD                                           选中A&D接口
   * @n     eI2C_UART1                                    选中I2C&UART1接口
   * @n     eI2C_UART2                                    选中I2C&UART2接口
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口
   * @return 选中的接口上连接的传感器的属性值，各属性值之间用','号隔开
   * @n 例:  28.65,30.12
   */
  String getValues(eInterfaceList_t inf = eALL);
  String getValues(uint8_t inf);
  /**
   * @fn getUnits
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)上一个或多个接口连接的传感器的数值的单位，多个单位之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     eAD                                           选中A&D接口
   * @n     eI2C_UART1                                    选中I2C&UART1接口
   * @n     eI2C_UART2                                    选中I2C&UART2接口
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口
   * @return 选中的接口上连接的传感器的的数值的单位，多个单位之间用','号隔开
   * @n 例:  C,%RH
   */
  String getUnits(eInterfaceList_t inf = eALL);
  String getUnits(uint8_t inf);

  /**
   * @fn getValue(char *keys)
   * @brief 获取所有接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
   * @param keys  传感器属性名称
   * @return 所有接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
   * @n 例Temp_Air:  28.65,28.65
   */
  String getValue(char *keys);
  /**
   * @fn getValue(eInterfaceList_t inf, char *keys)
   * @brief 获取指定接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
   * @param inf    接口选择，及参数查找范围
   * @n     eAD                                           选中A&D接口，在A&D接口所连接的传感器中查找属性名称为keys的属性值
   * @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口所连接的传感器中查找属性名称为keys的属性值
   * @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口所连接的传感器中查找属性名称为keys的属性值
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性值
   * @param keys  传感器属性名称
   * @return 指定接口所连接的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
   * @n 例Temp_Air:  28.65,28.65
   */
  String getValue(eInterfaceList_t inf, char *keys);
  String getValue(uint8_t inf, char *keys);
  /**
   * @fn getValue(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief 获取指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
   * @param inf    接口选择，及参数查找范围
   * @n     eAD                                           选中A&D接口，在A&D接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
   * @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
   * @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性值
   * @param sku 传感器SKU
   * @param keys  传感器属性名称
   * @return 指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据值，多个属性值之间用','号隔开
   * @n 例Temp_Air:  28.65,28.65
   */
  String getValue(eInterfaceList_t inf, char sku[7], char *keys);
  String getValue(uint8_t inf, char sku[7], char *keys);

  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief 获取所有接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
   * 
   * @param keys  传感器属性名称
   * @return  所有接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
   * @n 例Temp_Air:  C,C
   */
  String getUnit(char *keys);
  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief 获取指定接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
   * @param inf    接口选择，及参数查找范围
   * @n     eAD                                           选中A&D接口，在A&D接口所连接的传感器中查找属性名称为keys的属性单位
   * @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口所连接的传感器中查找属性名称为keys的属性单位
   * @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口所连接的传感器中查找属性名称为keys的属性单位
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性单位
   * @param keys  传感器属性名称
   * @return 指定接口所连接的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
   * @n 例Temp_Air:  C,C
   */
  String getUnit(eInterfaceList_t inf, char *keys);
  String getUnit(uint8_t inf, char *keys);
  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief 获取指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
   * @param inf    接口选择，及参数查找范围
   * @n     eAD                                           选中A&D接口，在A&D接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @n     eI2C_UART1                                    选中I2C&UART1接口，在I2C&UART1接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @n     eI2C_UART2                                    选中I2C&UART2接口，在I2C&UART2接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @n     eALL  or  (eAD | eI2C_UART1 | eI2C_UART2)     选中A&D, I2C&UART1和I2C&UART2接口，在所有接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @param sku 传感器SKU
   * @param keys  传感器属性名称
   * @return 指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
   * @n 例Temp_Air:  C,C
   */
  String getUnit(eInterfaceList_t inf, char sku[7], char *keys);
  String getUnit(uint8_t inf, char sku[7], char *keys);
  /**
   * @fn getAnalogSensorSKU
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)支持的模拟传感器的SKU清单，各SKU之间用',号隔开   * 
   * @return String 支持的模拟传感器的SKU列表
   */
  String getAnalogSensorSKU();
  /**
   * @fn getDigitalSensorSKU
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)支持的数字传感器的SKU清单，各SKU之间用',号隔开   * 
   * @return String 支持的数字传感器的SKU列表
   */
  String getDigitalSensorSKU();
  /**
   * @fn getI2CSensorSKU
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)支持的I2C传感器的SKU清单，各SKU之间用',号隔开   * 
   * @return String 支持的I2C传感器的SKU列表
   */
  String getI2CSensorSKU();
  /**
   * @fn getUARTSensorSKU
   * @brief 获取传感器通用适配器板(Sensor Universal Adapter Board)支持的UART传感器的SKU清单，各SKU之间用',号隔开   * 
   * @return String 支持的UART传感器的SKU列表
   */
  String getUARTSensorSKU();
```

## Compatibility

MCU                |  Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino Uno        |       √       |              |             | 
Mega2560           |      √       |              |             | 
Leonardo           |      √       |              |             | 
ESP32              |      √       |              |             | 
ESP8266            |      √       |              |             | 
micro:bit          |      √       |              |             | 
FireBeetle M0      |      √       |              |             | 

## History

- 2021/08/17 - Version 1.0.0 released.

## Credits

Written by Arya(xue.peng@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))





