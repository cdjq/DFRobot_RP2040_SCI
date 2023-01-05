# DFRobot_RP2040_SCI

* [中文版](./README_CN.md)

This SCI acquisition module is a multi-functional data acquisition module designed by DFRobot. It supports all kinds of digital, analog, I2C, and UART sensors from DFRobot. The module is capable of standardizing sensor output into the format of name+data+unit, which then can be read by main controllers or displayed on the onboard display so users can view it. The following demonstrates more details about this product through Q&A. <br>
* **Q1: DFRobot has so many sensors, so can this board support all of them?** <br>
  A: Sorry, it can't. This board only supports part of DFRobot's sensors currently. You can check the supported product list on the library Readme, SKU select on display, or read sensor type through a controller.
* **Q2: What if the analog, digital, I2C or UART sensor I want to use is not in the supported SKU list?**<br>
  A: Don't worry about it. The SCI Acquisition Module features USB firmware upgrading function. Please leave us comments and we'll add the sensor to the list. Then it will be available once you upgrade your firmware to the latest.
* **Q3: How does the SCI Acquisition module recognize different sensors?**<br>
  A: Each sensor from DFRobot has a unique SKU. The module can identify the connected sensor through automatic identification or the user-selected SKU, and call the corresponding driver to acquire and convert data. (Note: For some I2C sensors, the adapter can identify the SKU by I2C address, but for the others, it can only identify the connected one by user-selected SKU.)
* **Q4: How is the SCI Acquisition Module connected to these sensors?**<br>
  A: The module has an onboard Gravity 3pin analog/digital interface (for connecting analog or digital sensors) and 2 Gravity 4pin I2C/UART interfaces (for connecting I2C or UART sensors), so users can connect the corresponding sensor by switching to the corresponding interface mode.
* **Q5: What are the onboard display and button used for?** <br>
  A: Users can configure or view the module parameters such as I2C slave address, time, interface mode, SKU select, firmware version, and sensor data by the onboard display and buttons.
* **Q6: How can I use Arduino or Raspberry Pi to read and set parameters of the SCI Acquisition Module, and read the sensor data?**<br>
  Connect your controller to the acquisition module via the onboard Gravity I2C interface, and then you can operate the module. Find more details on [the wiki page](https://wiki.dfrobot.com/SKU_DFR0999_Gravity_SCI_Acquisition_Module). 
* **Q7: What's the USB on the module used for?** <br>
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
      @brief DFRobot_SCI_IIC Constructor
      @param addr:  7-bit IIC address, support the following address settings 
      @n RP2040_SCI_ADDR_0X21      0x21 default I2C address 
      @n RP2040_SCI_ADDR_0X22      0x22
      @n RP2040_SCI_ADDR_0X23      0x23
    '''
    
  def get_i2c_address(self):
    '''!
      @brief Get SCI Acquisition Module I2C address
      @return I2C address
    '''
  
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
class DFRobot_SCI:
  def begin(self):
    '''!
      @brief Initalize the SCI Acquisition Module, mainly for initializing communication interface
      @param freq Set communication frequency
      @return int Init status
      @n       0      Init successful
      @n      others  Init failed
    '''
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
  def get_version_description(self, version):
    '''!
      @brief Get version description char string 
      @return Return version description char string, e.g. id：0x0123 The returned version decription char string is V1.2.3
    '''
  def set_port1(self, sku):
    '''!
      @brief Set SKU on Port1, which can be connected to analog & digital sensors. Select the sensor connected to Port1 by SKU
      @param sku  Parameter for port1. The supported SKU list can be viewed on the OLED or by getAnalogSensorSKU()/getDigitalSensorSKU()
      @n     "NULL"             Clear sensor settings for Port1 and configure mode as analog sensor mode
      @n     "Analog"           Select analog voltage data acquisition, unit mV 
      @n     Analog sensor SKU  Select the SKU of a analog sensor and configure mode as analog sensor mode
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
  
  def get_port1(self):
    '''!
      @brief Get the sensor mode on port1 and SKU config 
      @return List 
      @n      The zeroth element in the list: error code 
      @n      The first element in the list: sensor mode 
      @n      The second element in the list: sku config 
    '''
  
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
      @n      ERR_CODE_S_NO_SPACE   or 0x09  Insufficient memory of I2C peripheral
    '''

  def get_port2(self):
    '''!
      @brief Get the sensor mode on port2 and SKU config
      @return List
      @n      The zeroth element in the list: error code 
      @n      The first element in the list: sensor mode 
      @n      The second element in the list: sku config
    '''

  def set_port3(self, sku):
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
      @n      ERR_CODE_S_NO_SPACE   or 0x09  Insufficient memory of I2C peripheral
    '''

  def get_port3(self):
    '''!
      @brief Get the sensor mode on port3 and SKU config
      @return List
      @n      The zeroth element in the list: error code 
      @n      The first element in the list: sensor mode 
      @n      The second element in the list: sku config
    '''

  def set_recv_timeout(self,timeout = 2):
    '''!
      @brief Initalize the SCI Acquisition Module, mainly for initializing communication interface
      @param freq Set communication frequency
      @return int Init status
      @n       0      Init successful
      @n      others  Init failed
    '''
    
  def adjust_rtc_datetime(self):
    '''!
      @brief Set the date and time of the SCI Acquisition Module as the current time of Raspbbery Pi 
      @return  rror code
      @n      ERR_CODE_NONE         or 0x00  Setting succeed 
      @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
      @n      ERR_CODE_RES_PKT      or 0x02  Response package error 
      @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
      @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout 
      @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
    '''

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

  def get_rtc_time(self):
    '''!
      @brief @brief Get the year, month, day, week, hour, minute, second of the SCI Acquisition Module
      @return List with a length of 2 data 
      @n      The first data in the list: list year, month, day, week, hour, minute, second[year, month, day, week, hour, minute, second]
      @n      The second data in the list: char string, year/month/day week hour:minute/second e.g. 2022/08/09 2 09:08:00
    '''
  
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

  def get_refresh_rate(self):
    '''!
      @brief Get data refresh rate
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

  def get_refresh_rate_describe(self, rate):
    '''!
      @brief Get refresh rate description, unit s 
    '''
    
  def get_timestamp(self):
    '''!
      @brief Get time stamp, also the data refresh time of the SCI Acquisition Module
      @return Hour:Minute:Second(00:00:00) or Minute:Second. X%(0-99)second(00:00.00)
    '''

  def get_AD_sensor_mode_describe(self, mode):
    '''!
      @brief Get mode description of Aanlog & Digital sensor 
      @param mode Sensor mode 
      @n     eAnalogMode    Aanlog sensor mode
      @n     eDigitalMode   Digital sensor mode
      @return Sensor mode description char string 
      @n      "ANALOG"         Analog sensor mode 
      @n      "DIGITAL"        Digital sensor mode 
      @n      "UNKNOWN"        Unknown mode 
    '''

  def get_I2CUART_sensor_mode_describe(self, mode):
    '''!
      @brief Get mode description of I2C & UART sensor 
      @param mode Sensor mode 
      @n     eI2CMode    I2C sensor mode 
      @n     eUARTMode   UART sensor mode 
      @return Sensor mode description char string
      @n      "I2C"         I2C sensor mode 
      @n      "UART"        UART sensor mode 
      @n      "UNKNOWN"     Unknown
    '''
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

  def get_information(self, inf, timestamp = False):
    '''!
      @brief Get the attribute information(attribute: value unit) of all sensors connected to the designated one or more ports. Separate attributes using "," 
      @param inf Designate one or more ports
      @n     ePort1                                    Designate port1, get attributes of all sensors connected to port1 
      @n     ePort2                                    Designate port2, get attributes of all sensors connected to port2
      @n     ePort3                                    Designate port3, get attributes of all sensors connected to port3
      @n     eALL  or  (ePort1 | ePort2 | ePort3)      Designate port1, port2 and port3, get attributes of all sensors connected to all ports
      @return The attribute information of all sensors connected to the designated one or more ports of the SCI Acquisition Module
      @n For example, SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
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





