DFRobot_RP2040_SCI
===========================
* [中文版](./README_CN.md)

This SCI acquisition module is a sensor adapter designed by DFRobot. It supports all kinds of digital, analog, I2C, and UART sensors from DFRobot. The module is capable of standardizing sensor output into the format of name+data+unit, which then will be read by main controllers or displayed on the onboard display so users can view it. The following demonstrates more details about this product through Q&A: <br>
* DFRobot has so many sensors, so can this board recognize all of them?<br>
  A: Sorry, it can't. This board only supports part of DFRobot's sensors currently. Users can get the list of supported kinds of sensors from the supported SKU in README, by viewing SKU Select on the onboard interactive display with button or reading it using the maincontroller or in other ways.
* Q2: What if the analog, digital, I2C or UART sensor I want to use is not in the supported SKU list?<br>
  A: Don't worry about it. The SCI Acquisition Module features USB firmware upgrading function, so you can leave comments and we'll add the sensor to the list, and then burn the latest firmware through the function.
* Q3: What's the principle that SCI Acquisition Module can recognize various sensors?<br>
  A: Each sensor from DFRobot has a unique SKU. The adapter can identify the connected sensor through automatic identification or the user-selected SKU, and call the corresponding driver to acquire and convert data. (Note: For some I2C sensors, the adapter can identify the SKU by I2C address, but for the others, it can only identify the connected one by user-selected SKU.)
* Q4: How is the SCI Acquisition Module connected to these sensors?<br>
  A: The adapter has an onboard Gravity 3pin analog/digital interfaces (for connecting analog or digital sensors) and 2 Gravity 4pin I2C/UART interfaces (for connecting I2C or UART sensors), so users can connect the corresponding sensor by switching to the corresponding interface mode.
* What's the onboard interactive display and the button used for?<br>
  A: Through the configurations, users can view the module's parameters, such as I2C slave address, time, switchable interface mode, SKU select, firmware version, and sensor data.
* Q6: How can I use Arduino or Raspberry Pi to read and set parameters of SCI Acquisition Module, and read the sensor data?<br> 
  A: The SCI Acquisition Module has an onboard Gravity I2C interface, which can be used by the maincontroller to control the adapter.
* Q7: What's the USB on the module used for? <br>
  A: It's used for firmware upgrading or CSV file export. Press the boot button to power on and enter USB firmware upgrading mode, and you can upgrade the firmware. When it's powered on directly, a USB will pop up and users can view or export the CSV file of recorded sensor data in the USB.

![产品效果图](./resources/images/SEN0443.png)


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
This library of the SCI acquisition module based on Arduino is designed to provide a series of interface functions for users to set and read parameters of the adapter and read the data from the connected sensor. It has the following functions:<br>
* 1. Read/set the I2C address of SCI Acquisition Module within the range of 0x01~0x7F;
* 2. Read/set the time information of year, month, day, hour, minute and second of SCI Acquisition Module;
* 3. Enable/disable sensor data record of CSV file;
* 4. Enable/disable the display;
* 5. Read/set the interface mode and SKU of the sensor;
* 6. Read sensor data (name + value + unit);
* 7. Read the list of supported SKU of analog, digital, I2C, UART and other types of sensors;

## Installation

There two methods: 
1. To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.
2. Search the DFRobot_RP2040_SCI library from the Arduino Software Library Manager and download it.

## Methods

```C++
  /**
   * @fn DFRobot_RP2040_SCI_IIC
   * @brief Constructor for DFRobot_RP2040_SCI_IIC class
   * @param addr:  7-bit I2C address, support the following address settings
   * @n RP2040_SCI_ADDR_0X21      0x21 Default I2C address of the adapter
   * @n RP2040_SCI_ADDR_0X22      0x22
   * @n RP2040_SCI_ADDR_0X23      0x23
   * @n Or view the I2C address on the initial page of the onboard OLED display, the factory default I2C address is 0x01
   * @param pWire:   TwoWire class & object pointer
   */
  DFRobot_RP2040_SCI_IIC(uint8_t addr = RP2040_SCI_ADDR_0X21, TwoWire *pWire = &Wire);
  ~DFRobot_RP2040_SCI_IIC();
  /**
   * @fn setI2CAddress
   * @brief Set the I2C communication address of SCI Acquisition Module
   * 
   * @param addr    I2C communication address of SCI Acquisition Module, support the following address settings
   * @n RP2040_SCI_ADDR_0X21      0x21 Default I2C address of the adapter
   * @n RP2040_SCI_ADDR_0X22      0x22
   * @n RP2040_SCI_ADDR_0X23      0x23
   * @return uint8_t Error Code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch 
   * @n      ERR_CODE_I2C_ADRESS   or 0x0A  Invalid I2C address
   */
  uint8_t setI2CAddress(uint8_t addr);
  /**
   * @fn getI2CAddress
   * @brief Get the I2C communication address of SCI Acquisition Module
   * @return I2C communication address
   */
  uint8_t getI2CAddress();

  /**
   * @fn DFRobot_RP2040_SCI
   * @brief Constructor of DFRobot_RP2040_SCI class.
   */
  DFRobot_SCI();

  /**
   * @fn  ~DFRobot_RP2040_SCI
   * @brief Destructor of class DFRobot_RP2040_SCI. 
   */
  ~DFRobot_SCI();
  
  /**
   * @fn begin
   * @brief Init SCI Acquisition Module, which aims to init the communication interface
   * 
   * @param freq Set communication frequency, no more than 100kHz
   * @return int Init status
   * @n       0  Init successful
   * @n      -1  The communication interface class & object are not passed in
   * @n      -2  Check if the hardware connection is correct
   */
  int begin(uint32_t freq = 100000);

  /**
   * @fn getVersion
   * @brief Get firmware version number of SCI Acquisition Module
   * @n The version number is 16-bit data, high 8 bits (b15~b9): represents the highest version bit
   * @n Middle 4 bits (b8~b4): represents middle version bit
   * @n Low 4 bits: represents low version bit
   * @n For example: 0x0123 corresponds to the version number of V1.2.3
   * 
   * @return 16-bit version number
   */
  uint16_t getVersion();
  /**
   * @fn getVersionDescription
   * @brief Get version description character string
   * 
   * @return Return version description character string, for example, version id: 0x0123 returns the version description character string of V1.2.3
   */
  String getVersionDescription(uint16_t version);

  /**
   * @fn setPort1(char *sku)
   * @brief Set supported SKU on Port1, which can be connected to analog & digital sensors, select the sensor connected to Port1 by SKU
   * 
   * @param sku  Parameters of Port1, the list of supported SKU can be viewed on OLED display or by getAnalogSensorSKU()/getDigitalSensorSKU()
   * @n     "NULL"       Indicates clearing sensor settings of Port1 and configuring sensor mode as analog sensor mode
   * @n     "Analog"     Indicates selecting Analog voltage data acquisition, unit mV
   * @n     SKU of analog sensor indicates selecting the SKU of an analog sensor and configuring mode as analog sensor mode
   * @n     SKU of digital sensor indicates selecting the SKU of an analog sensor and configuring mode as digital sensor mode
   * @return uint8_t Error Code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  Slave break
   * @n      ERR_CODE_ARGS         or 0x07  The set parameter is wrong
   */
  uint8_t setPort1(char *sku);

  /**
   * @fn getPort1(ePort1IFMode_t mode)
   * @brief Get the sensor mode and SKU config of Port1
   * 
   * @param mode  eADIFMode_t enum variable pointer
   * @n     eAnalogMode    Analog sensor mode
   * @n     eDigitalMode   Digital sensor mode
   * @return SKU of the sensor connected to Port1
   * @n      "NULL"        Indicates that Port1 is configured or connected to no sensor 
   * @n      "Analog"      Indicates that Port1 is configured as reading voltage data of Port1
   * @n      7-bit SKU        Indicates that Port1 is configured as reading data from a digital or analog sensor
   */
  String getPort1(ePort1IFMode_t *mode);

  /**
   * @fn setPort2(char *sku)
   * @brief 设置Port2的SKU，此接口可连接I2C传感器和UART传感器，其中UART传感器需通过SKU选择，I2C是连接后，自动选择，只需将Port2配置为I2C模式即可
   * 
   * @param sku  Port2接口的参数，支持的SKU列表可以通过OLED显示或者 getUARTSensorSKU()查看
   * @n     "NULL"       将Port配置为I2C模式，并清除Port2上关于UART传感器的配置
   * @n     UART传感器SKU 表示选择了某个UART传感器的SKU，并将模式配置为UART传感器模式
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
  uint8_t setPort2(char *sku);

  /**
   * @fn getPort2(ePort23Mode_t mode)
   * @brief 获取Port2的传感器模式，及SKU配置
   * 
   * @param mode  eI2CUARTMode_t 枚举变量指针
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return 接口0连接的传感器的SKU
   * @n      "NULL"        表示接口0没有配置或连接传感器
   * @n      7位SKU集合     I2C或UART传感器对应的SKU
   */
  String getPort2(ePort23Mode_t *mode);

  /**
   * @fn setPort3(char *sku)
   * @brief 设置Port3的SKU，此接口可连接I2C传感器和UART传感器，其中UART传感器需通过SKU选择，I2C是连接后，自动选择，只需将Port2配置为I2C模式即可
   * 
   * @param sku  Port3接口的参数，支持的SKU列表可以通过OLED显示或者 getUARTSensorSKU()查看
   * @n     "NULL"       将Port配置为I2C模式，并清除Port3上关于UART传感器的配置
   * @n     UART传感器SKU 表示选择了某个UART传感器的SKU，并将模式配置为UART传感器模式
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
  uint8_t setPort3(char *sku);

  /**
   * @fn getPort3(ePort23Mode_t mode)
   * @brief 获取Port3的传感器模式，及SKU配置
   * 
   * @param mode  eI2CUARTMode_t 枚举变量指针
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return 接口0连接的传感器的SKU
   * @n      "NULL"        表示接口0没有配置或连接传感器
   * @n      7位SKU集合     I2C或UART传感器对应的SKU
   */
  String getPort3(ePort23Mode_t *mode);

  /**
   * @fn setRecvTimeout
   * @brief 设置接收超时时间
   * 
   * @param timeout 当SCI采集模块连接的传感器较多时，在读取大量数据时需要适当提高接收超时时间，默认2s
   */
  void setRecvTimeout(uint32_t timeout = 2000);
  /**
   * @fn adjustRtc(const __FlashStringHelper* date, const __FlashStringHelper* time)
   * @brief 设置SCI采集模块(SCI Acquisition Module)的时间
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
   * @brief 设置SCI采集模块(SCI Acquisition Module)的时间
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
   * @brief 获取SCI采集模块(SCI Acquisition Module)的年月日时分秒周等日期
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
   * @brief 获取SCI采集模块(SCI Acquisition Module)的年月日时分秒周等日期
   * 
   * @return 年/月/日 周 时:分:秒表示的字符串，例 2022/08/09 2 09:08:00 2022年8月9日，星期二 9点8分0秒
   */
  String getRtcTime();
  /**
   * @fn setRefreshRate
   * @brief 设置数据刷新时间
   * 
   * @param refreshRate eRefreshRate_t枚举变量
   * @n eRefreshRateMs     ms级刷新率，按数据的实际刷新率刷新
   * @n eRefreshRate1s     刷新率1s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate3s     刷新率3s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate5s     刷新率5s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate10s    刷新率10s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate30s    刷新率30s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate1min   刷新率1min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate5min   刷新率5min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate10min  刷新率10min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @return uint8_t 错误代码
   * @n      ERR_CODE_NONE         or 0x00  设置成功
   * @n      ERR_CODE_CMD_INVAILED or 0x01  无效命令
   * @n      ERR_CODE_RES_PKT      or 0x02  响应包错误
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  I2C主机内存不够
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  响应包接收超时
   * @n      ERR_CODE_CMD_PKT      or 0x05  无效的命令包或者命令不匹配
   */
  uint8_t setRefreshRate(eRefreshRate_t refreshRate);
  /**
   * @fn getRefreshRate
   * @brief 获取设置的刷新时间，注意此刷新时间可能不是数据实际刷新时间，它们之间满足这样的关系: 设置的刷新时间 <= 数据实际刷新时间
   * 
   * @param refreshRate eRefreshRate_t枚举变量，获取等级
   * @n eRefreshRateMs     ms级刷新率，按数据的实际刷新率刷新
   * @n eRefreshRate1s     刷新率1s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate3s     刷新率3s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate5s     刷新率5s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate10s    刷新率10s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate30s    刷新率30s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate1min   刷新率1min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate5min   刷新率5min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @n eRefreshRate10min  刷新率10min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新
   * @return uint32_t 返回刷新时间，单位ms
   * @n eRefreshRateMs     0ms
   * @n eRefreshRate1s     1000ms
   * @n eRefreshRate3s     3000ms
   * @n eRefreshRate5s     5000ms
   * @n eRefreshRate10s    10000ms
   * @n eRefreshRate30s    30000ms
   * @n eRefreshRate1min   60000ms
   * @n eRefreshRate5min   300000ms
   * @n eRefreshRate10min  600000ms
   */
  uint32_t getRefreshRate(eRefreshRate_t *refreshRate = NULL);
  /**
   * @fn getTimeStamp()
   * @brief 获取时间戳,此时间戳为(SCI Acquisition Module)数据刷新时间
   * 
   * @return 时:分:秒(00:00:00) 或 分:秒.百分之（0~99）秒(00:00.00)
   */
  String getTimeStamp();
  
  /**
   * @fn getSensorModeDescribe(ePort1IFMode_t mode)
   * @brief 获取传感器的模式描述
   * 
   * @param mode  ePort1IFMode_t枚举变量
   * @n     eAnalogMode    模拟传感器模式
   * @n     eDigitalMode   数字传感器模式
   * @return 传感器的模式描述字符串
   * @n      "ANALOG"         模拟传感器模式
   * @n      "DIGITAL"        数字传感器模式
   * @n      "UNKNOWN"        未知模式
   */
  String getSensorModeDescribe(ePort1IFMode_t mode);
  /**
   * @fn getSensorModeDescribe(ePort23Mode_t mode)
   * @brief 获取传感器的模式描述
   * 
   * @param mode  ePort23Mode_t 枚举变量
   * @n     eI2CMode    I2C传感器模式
   * @n     eUARTMode   UART传感器模式
   * @return 传感器的模式描述字符串
   * @n      "I2C"         I2C传感器模式
   * @n      "UART"        UART传感器模式
   * @n      "UNKNOWN"     未知模式
   */
  String getSensorModeDescribe(ePort23Mode_t mode);
  
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
   * @brief 开启SCI采集模块(SCI Acquisition Module)屏显示
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
   * @brief 关闭SCI采集模块(SCI Acquisition Module)屏显示
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
   * @brief 获取SCI采集模块(SCI Acquisition Module)上一个或多个接口连接的传感器的信息，名称:数值 单位,多条信息之间
   * @n 用','号隔开
   * 
   * @param inf    接口选择
   * @n     ePort1                                           选中Port1接口
   * @n     ePort2                                           选中Port2接口
   * @n     ePort3                                           选中Port3接口
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
   * @param timestamp 获取的信息中是否加时间戳
   * @n     false  不加时间戳
   * @n     ture   加时间戳   
   * @return 选中的接口上连接的传感器的属性，每条属性格式为：名称:数值 单位，多条属性之间用','号隔开,单位和数值之间用空格隔开
   * @n 不加时间戳 例SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
   * @n 加时间戳   例SEN0334:  分:秒.百分之(0~99)秒 Temp_Air:28.65 C,Humi_Air:30.12 %RH 或 时:分:秒 Temp_Air:28.65 C,Humi_Air:30.12 %RH
   */
  String getInformation(eInterfaceList_t inf = eALL, bool timestamp = false);
  String getInformation(uint8_t inf, bool timestamp = false);

  /**
   * @fn getSKU
   * @brief 获取SCI采集模块(SCI Acquisition Module)上一个或多个接口连接的传感器的SKU,多个SKU之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     ePort1                                           选中Port1接口
   * @n     ePort2                                           选中Port2接口
   * @n     ePort3                                           选中Port3接口
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
   * @return 选中的接口上连接的传感器的SKU，多个SKU之间用','号隔开,
   * @n 例:  SEN0161,SEN0334
   */
  String getSKU(eInterfaceList_t inf = eALL);
  String getSKU(uint8_t inf);

  /**
   * @fn getKeys
   * @brief 获取传感器SCI采集模块(SCI Acquisition Module)上一个或多个接口连接的传感器的名称，各名称之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     ePort1                                           选中Port1接口
   * @n     ePort2                                           选中Port2接口
   * @n     ePort3                                           选中Port3接口
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
   * @return 选中的接口上连接的传感器的名称，各名称之间用','号隔开
   * @n 例:  Temp_Air,Humi_Air
   */
  String getKeys(eInterfaceList_t inf = eALL);
  String getKeys(uint8_t inf);
  /**
   * @fn getValues
   * @brief 获取SCI采集模块(SCI Acquisition Module)上一个或多个接口连接的传感器的属性值，各属性值之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     ePort1                                           选中Port1接口
   * @n     ePort2                                           选中Port2接口
   * @n     ePort3                                           选中Port3接口
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
   * @return 选中的接口上连接的传感器的属性值，各属性值之间用','号隔开
   * @n 例:  28.65,30.12
   */
  String getValues(eInterfaceList_t inf = eALL);
  String getValues(uint8_t inf);
  /**
   * @fn getUnits
   * @brief 获取传感器SCI采集模块(SCI Acquisition Module)上一个或多个接口连接的传感器的数值的单位，多个单位之间用','号隔开
   * 
   * @param inf    接口选择
   * @n     ePort1                                           选中Port1接口
   * @n     ePort2                                           选中Port2接口
   * @n     ePort3                                           选中Port3接口
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
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
   * @n     ePort1                                          选中Port1接口，在A&D接口所连接的传感器中查找属性名称为keys的属性值
   * @n     ePort2                                          选中Port2接口，在I2C&UART1接口所连接的传感器中查找属性名称为keys的属性值
   * @n     ePort3                                          选中Port3接口，在I2C&UART2接口所连接的传感器中查找属性名称为keys的属性值
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)            选中(ePort1 | ePort2 | ePort3)  接口，在所有接口接口所连接的传感器中查找属性名称为keys的属性值
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
   * @n     ePort1                                          选中Port1接口，在Port1接口所连接的传感器中查找SKU为sku的传感器，并读出属性名称为keys的属性值
   * @n     ePort2                                          选中Port2接口，在Port2接口所连接的传感器中查找SKU为sku的传感器，并读出属性名称为keys的属性值
   * @n     ePort3                                          选中Port3接口，在Port3接口所连接的传感器中查找SKU为sku的传感器，并读出属性名称为keys的属性值
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)            选中(ePort1 | ePort2 | ePort3)  接口，在所有接口接口所连接的传感器中查找SKU为sku的传感器，并读出属性名称为keys的属性值
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
   * @n     ePort1                                          选中Port1接口，在Port1接口所连接的传感器中查找属性名称为keys的属性单位
   * @n     ePort2                                          选中Port2接口，在Port2接口所连接的传感器中查找属性名称为keys的属性单位
   * @n     ePort3                                          选中Port3接口，在Port3接口所连接的传感器中查找属性名称为keys的属性单位
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，在所有接口接口中查找属性名称为keys的属性单位
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
   * @n     ePort1                                          选中Port1接口，在Port1接口所连接的传感器中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @n     ePort2                                          选中Port2接口，在Port2接口所连接的传感器中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @n     ePort3                                          选中Port3接口，在Port3接口所连接的传感器中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)      选中Port1, Port2和Port3接口，在所有接口接口中查找SKU为sku的传感器，并读出属性名称为keys的属性单位
   * @param sku 传感器SKU
   * @param keys  传感器属性名称
   * @return 指定接口所连接的传感器中SKU为sku的传感器中属性名称为 keys 的数据单位，多个属性单位之间用','号隔开
   * @n 例Temp_Air:  C,C
   */
  String getUnit(eInterfaceList_t inf, char sku[7], char *keys);
  String getUnit(uint8_t inf, char sku[7], char *keys);
  /**
   * @fn getAnalogSensorSKU
   * @brief 获取SCI采集模块(SCI Acquisition Module)支持的模拟传感器的SKU清单，各SKU之间用',号隔开   * 
   * @return String 支持的模拟传感器的SKU列表
   */
  String getAnalogSensorSKU();
  /**
   * @fn getDigitalSensorSKU
   * @brief 获取SCI采集模块(SCI Acquisition Module)支持的数字传感器的SKU清单，各SKU之间用',号隔开   * 
   * @return String 支持的数字传感器的SKU列表
   */
  String getDigitalSensorSKU();
  /**
   * @fn getI2CSensorSKU
   * @brief 获取SCI采集模块(SCI Acquisition Module)支持的I2C传感器的SKU清单，各SKU之间用',号隔开   * 
   * @return String 支持的I2C传感器的SKU列表
   */
  String getI2CSensorSKU();
  /**
   * @fn getUARTSensorSKU
   * @brief 获取SCI采集模块(SCI Acquisition Module)支持的UART传感器的SKU清单，各SKU之间用',号隔开   * 
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





