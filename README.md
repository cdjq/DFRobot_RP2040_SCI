DFRobot_RP2040_SCI
===========================
* [中文版](./README_CN.md)

This SCI acquisition module is a sensor adapter designed by DFRobot. It supports all kinds of digital, analog, I2C, and UART sensors from DFRobot. The module is capable of standardizing sensor output into the format of name+data+unit, which then will be read by main controllers or displayed on the onboard display so users can view it. The following demonstrates more details about this product through Q&A: <br>
* DFRobot has so many sensors, so can this board recognize all of them?<br>
  A: Sorry, it can't. This board only supports part of DFRobot's sensors currently. You can check the supported product list on the library Readme, SKU select on display, or read sensor type through a controller.
* Q2: What if the analog, digital, I2C or UART sensor I want to use is not in the supported SKU list?<br>
  A: Don't worry about it. The SCI Acquisition Module features USB firmware upgrading function. Please leave us comments and we'll add the sensor to the list. Then it will be available once you upgrade your firmware to the latest.
* Q3: How does the SCI Acquisition module recognize different sensors?<br>
  A: Each sensor from DFRobot has a unique SKU. The adapter can identify the connected sensor through automatic identification or the user-selected SKU, and call the corresponding driver to acquire and convert data. (Note: For some I2C sensors, the adapter can identify the SKU by I2C address, but for the others, it can only identify the connected one by user-selected SKU.)
* Q4: How is the SCI Acquisition Module connected to these sensors?<br>
  A: The adapter has an onboard Gravity 3pin analog/digital interfaces (for connecting analog or digital sensors) and 2 Gravity 4pin I2C/UART interfaces (for connecting I2C or UART sensors), so users can connect the corresponding sensor by switching to the corresponding interface mode.
* Q5: What's the onboard display and button used for?<br>
  A: Users can configure or view the module parameters such as I2C slave address, time, switchable interface mode, SKU select, firmware version, and sensor data by the onboard display and buttons.
* Q6: How can I use Arduino or Raspberry Pi to read and set parameters of SCI Acquisition Module, and read the sensor data?<br> 
  A: Connect your controller to the acquisition module via the onboard Gravity I2C interface, and then you can operate the module. Find more details on the wiki page: https://wiki.dfrobot.com/SKU_DFR0999_Gravity_SCI_Acquisition_Module. 
* Q7: What's the USB on the module used for? <br>
  A: It's used for firmware upgrading or CSV file export. Press the boot button and power on the module to enter the firmware upgrading mode, then you can upgrade the firmware. When it's powered on directly, a U-disk will pop up on your PC and you can view or export the CSV file of recorded sensor data in the U-disk.

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
This is an Arduino library for the DFRobot SCI Acquisition module. It aims to provide users with a series of interface functions to set and read module parameters, or read sensor data. It has the following functions:<br>
* 1. Read/set the I2C address of SCI Acquisition Module within the range of 0x01~0x7F;
* 2. Read/set the time information of year, month, day, hour, minute and second of SCI Acquisition Module;
* 3. Enable/disable sensor data record of CSV file;
* 4. Enable/disable the display;
* 5. Read/set the interface mode and SKU of the sensor;
* 6. Read sensor data (name + value + unit);
* 7. Read the supported product SKU list, including, analog, digital, I2C, UART and other types of sensors;

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
   * @n RP2040_SCI_ADDR_0X21      0x21 Default I2C address
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
   * @n The version number is 16-bit data, high 8 bits (b15~b9): represents the leftmost number
   * @n Middle 4 bits (b8~b4): represents the middle number
   * @n Low 4 bits: represents the rightmost number
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
   * @brief Set supported SKU on Port2, which can be connected to I2C & UART sensors, UART sensors need to be selected by SKU; I2C sensors are automatically selected after connection, and you just need to configure Port2 as I2C mode
   * 
   * @param sku  Parameters of Port2, the list of supported SKU can be viewed on the OLED display or by getUARTSensorSKU()
   * @n     "NULL"       Configure Port2 as I2C mode and clear the config related to UART sensor on Port2
   * @n     SKU of a UART sensor indicates the SKU of a UART sensor is selected and the mode is configured as UART sensor mode
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch 
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  Slave break
   * @n      ERR_CODE_ARGS         or 0x07  The set parameter is wrong
   */
  uint8_t setPort2(char *sku);

  /**
   * @fn getPort2(ePort23Mode_t mode)
   * @brief Get the sensor mode and SKU config of Port2
   * 
   * @param mode  eI2CUARTMode_t enum variable pointer
   * @n     eI2CMode    I2C sensor mode
   * @n     eUARTMode   UART sensor mode
   * @return SKU of the sensor connected to Port2
   * @n      "NULL"        Indicates Port2 is configured or connected to no sensor
   * @n      7-bit SKU set     SKU corresponding to I2C or UART sensor
   */
  String getPort2(ePort23Mode_t *mode);

  /**
   * @fn setPort3(char *sku)
   * @brief Set supported SKU on Port3, which can be connected to I2C & UART sensors, UART sensors need to be selected by SKU; I2C sensors are automatically selected after connection, and you just need to configure Port3 as I2C mode
   * 
   * @param sku  Parameters of Port3, the list of supported SKU can be viewed on the OLED display or by getUARTSensorSKU()
   * @n     "NULL"       Configure Port3 as I2C mode and clear the config related to UART sensors on Port3
   * @n     SKU of a UART sensor indicates the SKU of a UART sensor is selected and the mode is configured as UART sensor mode
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch 
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  Slave break
   * @n      ERR_CODE_ARGS         or 0x07  The set parameter is wrong
   */
  uint8_t setPort3(char *sku);

  /**
   * @fn getPort3(ePort23Mode_t mode)
   * @brief Get the sensor mode and SKU config of Port3
   * 
   * @param mode  eI2CUARTMode_t enum variable pointer
   * @n     eI2CMode    I2C sensor mode
   * @n     eUARTMode   UART sensor mode
   * @return SKU of the sensor connected to Port3
   * @n      "NULL"        Indicates Port3 is configured or connected to no sensor 
   * @n      7-bit SKU set     SKU corresponding to I2C or UART sensor
   */
  String getPort3(ePort23Mode_t *mode);

  /**
   * @fn setRecvTimeout
   * @brief Set reception timeout
   * 
   * @param timeout When there are many sensors connected to SCI Acquisition Module, you need to increase the reception timeout value appropriately when reading a large amount of data, the default is 2s
   */
  void setRecvTimeout(uint32_t timeout = 2000);
  /**
   * @fn adjustRtc(const __FlashStringHelper* date, const __FlashStringHelper* time)
   * @brief Set time of SCI Acquisition Module
   * 
   * @param date Year, month & day
   * @param time Hour, minute & second
   * @return Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch 
   */
  uint8_t adjustRtc(const __FlashStringHelper* date, const __FlashStringHelper* time);
	/**
   * @fn adjustRtc(uint16_t year, uint8_t month, uint8_t day, uint8_t week, uint8_t hour, uint8_t minute, uint8_t second)
   * @brief Set time of SCI Acquisition Module
   * 
   * @param year   Year
   * @param month  Month
   * @param day    Day
   * @param week   Week
   * @param hour   Hour
   * @param minute Minute
   * @param second Second
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   */
  uint8_t adjustRtc(uint16_t year, uint8_t month, uint8_t day, uint8_t week, uint8_t hour, uint8_t minute, uint8_t second);
  /**
   * @fn getRtcTime(uint16_t *year, uint8_t *month, uint8_t *day, uint8_t *week, uint8_t *hour, uint8_t *minute, uint8_t *second)
   * @brief Get the time information of year, month, day, hour, minute, second, week, etc. of SCI Acquisition Module
   * 
   * @param year   Year
   * @param month  Month
   * @param day    Day
   * @param week   Week
   * @param hour   Hour
   * @param minute Minute
   * @param second Second
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   */
  uint8_t getRtcTime(uint16_t *year, uint8_t *month, uint8_t *day, uint8_t *week, uint8_t *hour, uint8_t *minute, uint8_t *second);
  /**
   * @fn getRtcTime()
   * @brief Get the time information of year, month, day, hour, minute, second, week, etc. of SCI Acquisition Module
   * 
   * @return The character string for year/month/day week hour:minute:second, for example, 2022/08/09 2 09:08:00 represents Tuesday, August 9, 2022, at 9:08:0 
   */
  String getRtcTime();
  /**
   * @fn setRefreshRate
   * @brief Set data refresh rate
   * 
   * @param refreshRate eRefreshRate_t enum variable
   * @n eRefreshRateMs     Refresh rate measured in ms, refresh at actual data refresh rate
   * @n eRefreshRate1s     Refresh rate 1s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate3s     Refresh rate 3s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate5s     Refresh rate 5s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate10s    Refresh rate 10s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate30s    Refresh rate 30s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate1min   Refresh rate 1min, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate5min   Refresh rate 5min, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate10min  Refresh rate 10min, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   */
  uint8_t setRefreshRate(eRefreshRate_t refreshRate);
  /**
   * @fn getRefreshRate
   * @brief Get the set refresh time, which may not be the actual refresh time, the relationship between them is: the set refresh time <= the actual refresh time
   * 
   * @param refreshRate eRefreshRate_t enum variable, get the level
   * @n eRefreshRateMs     Refresh rate measured in ms, refresh at actual data refresh rate
   * @n eRefreshRate1s     Refresh rate 1s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate3s     Refresh rate 3s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate5s     Refresh rate 5s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate10s    Refresh rate 10s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate30s    Refresh rate 30s, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate1min   Refresh rate 1min, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate5min   Refresh rate 5min, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @n eRefreshRate10min  Refresh rate 10min, if the actual data refresh rate is less than the value, then refresh at the value;l if greater than the value, then refresh at the actual refresh rate
   * @return uint32_t Return refresh rate, unit ms
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
   * @brief Get time stamp, which is the data refresh time of SCI Acquisition Module
   * 
   * @return Hour:minute:second(00:00:00) or minute:second.(0~99)% second (00:00.00)
   */
  String getTimeStamp();
  
  /**
   * @fn getSensorModeDescribe(ePort1IFMode_t mode)
   * @brief Get sensor mode description
   * 
   * @param mode  ePort1IFMode_t enum variable
   * @n     eAnalogMode    Analog sensor mode
   * @n     eDigitalMode   Digital sensor mode
   * @return Character string of sensor mode description
   * @n      "ANALOG"         Analog sensor mode
   * @n      "DIGITAL"        Digital sensor mode
   * @n      "UNKNOWN"        Unknown Mode
   */
  String getSensorModeDescribe(ePort1IFMode_t mode);
  /**
   * @fn getSensorModeDescribe(ePort23Mode_t mode)
   * @brief Get sensor mode description
   * 
   * @param mode  ePort23Mode_t enum variable
   * @n     eI2CMode    I2C sensor mode
   * @n     eUARTMode   UART sensor mode
   * @return Character string of sensor mode description
   * @n      "I2C"         I2C sensor mode
   * @n      "UART"        UART sensor mode
   * @n      "UNKNOWN"     Unknown Mode
   */
  String getSensorModeDescribe(ePort23Mode_t mode);
  
  /**
   * @fn enableRecord
   * @brief Enable CSV file record, after the command is called, the data collected by the sensor will be recorded in a CSV file named with information of year, month, day, hour, minute and second.
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   */
  uint8_t enableRecord();
  /**
   * @fn disableRecord
   * @brief Disable CSV file record, after the command is called, the data collected by the sensor will not be recorded in a CSV file named with information of year, month, day, hour, minute and second
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   */
  uint8_t disableRecord();
  
  /**
   * @fn oledScreenOn
   * @brief Enable display of SCI Acquisition Module
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   */
  uint8_t oledScreenOn();
  /**
   * @fn oledScreenOff
   * @brief Disable display of SCI Acquisition Module
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Set successful
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C master 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet reception timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or command mismatch
   */
  uint8_t oledScreenOff();
  
  /**
   * @fn getInformation
   * @brief Get information about the connected sensor on one or more ports of SCI Acquisition Module, name: value unit,
   * @n separate multiple pieces of information with ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @param timestamp Whether the acquired information is timestamped or not
   * @n     false  Not timestamped
   * @n     ture   Timestamped 
   * @return Properties of the sensor connected to the selected port, each one is in the format of name:value unit, separate properties with "," and separate unit and value with a space
   * @n Not timestamped for example, SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
   * @n Timestamped   for example, SEN0334:  minute:second.(0~99)% second Temp_Air:28.65 C,Humi_Air:30.12 %RH or hour:minute:second Temp_Air:28.65 C,Humi_Air:30.12 %RH
   */
  String getInformation(eInterfaceList_t inf = eALL, bool timestamp = false);
  String getInformation(uint8_t inf, bool timestamp = false);

  /**
   * @fn getSKU
   * @brief Get the SKU of the connected sensor on one or more ports of SCI Acquisition Module, separate multiple SKUs with ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The SKU of the connected sensor on the selected port, separate SKUs with ","
   * @n For example:  SEN0161,SEN0334
   */
  String getSKU(eInterfaceList_t inf = eALL);
  String getSKU(uint8_t inf);

  /**
   * @fn getKeys
   * @brief Get the name of the connected sensor on one or more ports of SCI Acquisition Module, name:value unit, separate multiple names with ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The name of the connected sensor on the selected port, separate multiple names with ","
   * @n For example:  Temp_Air,Humi_Air
   */
  String getKeys(eInterfaceList_t inf = eALL);
  String getKeys(uint8_t inf);
  /**
   * @fn getValues
   * @brief Get the property value of the connected sensor on one or more ports of SCI Acquisition Module, separate multiple property values with ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The property values of the connected sensor on the selected port, separate multiple property values with ","
   * @n For example:  28.65,30.12
   */
  String getValues(eInterfaceList_t inf = eALL);
  String getValues(uint8_t inf);
  /**
   * @fn getUnits
   * @brief Get the value unit of the connected sensor on one or more ports of the SCI acquisition module, separate multiple units with ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The value unit of the connected sensor on the selected port, separate multiple units with ","
   * @n For example:  C,%RH
   */
  String getUnits(eInterfaceList_t inf = eALL);
  String getUnits(uint8_t inf);

  /**
   * @fn getValue(char *keys)
   * @brief Get data values of the properties with name of keys in the connected sensors on all the ports, separate multiple property values with ',' 
   * @param keys  Sensor property name
   * @return Data values of the properties with name of keys in the connected sensors on all the ports, separate multiple property values with ',' 
   * @n For example, Temp_Air:  28.65,28.65
   */
  String getValue(char *keys);
  /**
   * @fn getValue(eInterfaceList_t inf, char *keys)
   * @brief Get data values of the properties with name of keys in the connected sensors on the designated ports, separate multiple property values with ','
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select Port1, and find values of properties with the name of keys in the connected sensors on all the A&D ports
   * @n     ePort2                                          Select Port2, and find values of properties with the name of keys in the connected sensors on all the I2C&UART1 ports
   * @n     ePort3                                          Select Port3, and find values of properties with the name of keys in the connected sensors on all the I2C&UART2 ports
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)            Select Port1, Port2 & Port3, and find values of properties with the name of keys in the connected sensors on all the ports
   * @param keys  Sensor property name
   * @return Get data values of the properties with name of keys in the connected sensors on the designated ports, separate multiple property values with ','
   * @n For example, Temp_Air:  28.65,28.65
   */
  String getValue(eInterfaceList_t inf, char *keys);
  String getValue(uint8_t inf, char *keys);
  /**
   * @fn getValue(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data values of the properties with name of keys in the connected sensor whose SKU is sku on the designated ports, separate multiple property values with ','
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select Port1, find the sensor whose SKU is sku in the connected sensors on Port1, and read the value of the property with the name of keys
   * @n     ePort2                                          Select Port2, find the sensor whose SKU is sku in the connected sensors on Port2, and read the value of the property with the name of keys
   * @n     ePort3                                          Select Port3, find the sensor whose SKU is sku in the connected sensors on Port3, and read the value of the property with the name of keys
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)            Select Port1, Port2 and Port3, find the sensor whose SKU is sku in the connected sensors on all the ports, and read the value of the property with the name of keys
   * @param sku Sensor SKU
   * @param keys  Sensor property name
   * @return Get data values of the properties with name of keys in the connected sensor whose SKU is sku on the designated ports, separate multiple property values with ','
   * @n For example, Temp_Air:  28.65,28.65
   */
  String getValue(eInterfaceList_t inf, char sku[7], char *keys);
  String getValue(uint8_t inf, char sku[7], char *keys);

  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data units of the properties with the name of keys in the connected sensors on all the ports, separate multiple property units with ','
   * 
   * @param keys  Sensor property name
   * @return  The data units of the properties with the name of keys in the connected sensors on all the ports, separate multiple property units with ','
   * @n For example, Temp_Air:  C,C
   */
  String getUnit(char *keys);
  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data units of the properties with the name of keys in the connected sensors on the designated ports, separate multiple property units with ','
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select Port1, and find units of properties with the name of keys in the connected sensors on Port1
   * @n     ePort2                                          Select Port2, and find units of properties with the name of keys in the connected sensors on Port2
   * @n     ePort3                                          Select Port3, and find units of properties with the name of keys in the connected sensors on Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select Port1, Port2 and Port3, and find units of properties with the name of keys in the connected sensors on all the ports
   * @param keys  Sensor property name
   * @return The data units of the properties with the name of keys in the connected sensors on the designated ports, separate multiple property units with ','
   * @n For example, Temp_Air:  C,C
   */
  String getUnit(eInterfaceList_t inf, char *keys);
  String getUnit(uint8_t inf, char *keys);
  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data units of the properties with the name of keys in the connected sensor whose SKU is sku on the designated ports, separate multiple property units with ','
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select Port1, find the sensor whose SKU is sku in the connected sensors on Port1, and read units of properties with the name of keys
   * @n     ePort2                                          Select Port2, find the sensor whose SKU is sku in the connected sensors on Port2, and read units of properties with the name of keys
   * @n     ePort3                                          Select Port3, find the sensor whose SKU is sku in the connected sensors on Port3, and read units of properties with the name of keys
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select Port1, Port2 and Port3, find the sensor whose SKU is sku in the connected sensors on all the ports, and read units of properties with the name of keys
   * @param sku Sensor SKU
   * @param keys  Sensor property name
   * @return The data units of the properties with the name of keys in the connected sensor whose SKU is sku on the designated ports, separate multiple property units with ','
   * @n For example, Temp_Air:  C,C
   */
  String getUnit(eInterfaceList_t inf, char sku[7], char *keys);
  String getUnit(uint8_t inf, char sku[7], char *keys);
  /**
   * @fn getAnalogSensorSKU
   * @brief Get the SKU list of analog sensors supported by SCI Acquisition Module, separate SKUs with ','   * 
   * @return String SKU list of supported analog sensors
   */
  String getAnalogSensorSKU();
  /**
   * @fn getDigitalSensorSKU
   * @brief Get the SKU list of digital sensors supported by SCI Acquisition Module, separate SKUs with ','   * 
   * @return String SKU list of supported digital sensors
   */
  String getDigitalSensorSKU();
  /**
   * @fn getI2CSensorSKU
   * @brief Get the SKU list of I2C sensors supported by SCI Acquisition Module, separate SKUs with ','   * 
   * @return String SKU list of supported I2C sensors
   */
  String getI2CSensorSKU();
  /**
   * @fn getUARTSensorSKU
   * @brief Get the SKU list of UART sensors supported by SCI Acquisition Module, separate SKUs with ','   * 
   * @return String SKU list of supported UART sensors
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





