/*!
 * @file DFRobot_RP2040_SCI.h
 * @brief This is an Arduino drive library for the DFRobot SCI Acquisition module. Users can read or set its config and data via I2C. The following demonstrates its detailed functions:
 * @n 1. Set or read the I2C address of the module as 0x21, 0x22 or 0x23, the factory default is 0x21, 
 * @n after the I2C address is changed, it will take effect after power-off and reboot;
 * @n 2. Set or read the config of Port1, Port2 or Port3:
 * @n    Port1: can be configured as analog or digital sensor mode, support NULL, Analog, and analog sensor SKU in analog sensor mode, and support digital sensor SKU in digital sensor mode
 * @n    Port2: can be configured as I2C or UART sensor mode, support NULL or I2C sensor in I2C sensor mode, 
 * @n    in which I2C sensor will be automatically recognized by the module when powered on, and support UART sensor SKU in UART sensor mode
 * @n    Port3: can be configured as I2C or UART sensor mode, support NULL or I2C sensor in I2C sensor mode, 
 * @n    in which I2C sensor will be automatically recognized by the module when powered on, and support UART sensor SKU in UART sensor mode
 * @n 3. Enable/disable data record of CSV file
 * @n 4. Enable/disable OLED display
 * @n 5. Read the parameters of the sensors connected to the SCI Acquisition module:
 * @n      a. Get sensor data "name", separate names by a comma(,);
 * @n      b. Get sensor data "value", separate values by a comma(,);
 * @n      c. Get sensor data unit, separate units by a comma(,);
 * @n      d. Get the SKU of the connected sensor;
 * @n      e. Get the complete sensor information in the format of name:value unit, separate multiple pieces of information by a comma (,)
 * @n 6. Set and read the data refresh rate
 * @n 7. Get data refresh timestamp
 *
 * @copyright   Copyright (c) 2022 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Arya](xue.peng@dfrobot.com)
 * @maintainer [qsjhyy](yihuan.huang@dfrobot.com)
 * @version  V1.0
 * @date  2022-07-20
 * @url https://github.com/DFRobot/DFRobot_RP2040_SCI
 */
#ifndef DFROBOT_RP2040_SCI_H
#define DFROBOT_RP2040_SCI_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include <Wire.h>


/* I2C address supported by SCI Acquisition Module */
#define RP2040_SCI_ADDR_0X21      0x21 ///< default I2C address
#define RP2040_SCI_ADDR_0X22      0x22
#define RP2040_SCI_ADDR_0X23      0x23

class DFRobot_RP2040_SCI{
public:
  /**
   * @enum eInterfaceList_t
   * @brief The port to be set or read
   */
  typedef enum{
    ePort1         = 1 << 0, /**< Port1, analog or digital sensor port*/
    ePort2         = 1 << 1, /**< Port2, I2C or UART sensor port*/
    ePort3         = 1 << 2, /**< Port3, I2C or UART sensor port*/
    eALL           = 0x07    /**< Port1, Port2, and Port3*/
  }eInterfaceList_t;

  /**
   * @enum ePort1IFMode_t
   * @brief Port1 mode select
   */
  typedef enum{
    eAnalogMode = 0,  /**< Analog sensor mode*/
    eDigitalMode      /**< Digital sensor mode*/
  }ePort1IFMode_t;

  /**
   * @enum ePort23Mode_t
   * @brief Port2 or Port3 mode select
   */
  typedef enum{
    eI2CMode  = 0,   /**< I2C sensor mode*/
    eUARTMode        /**< UART sensor mode*/
  }ePort23Mode_t;

  typedef enum{
    eRefreshRateMs = 0,  /**< ms-level, refresh at the actual refresh rate*/
    eRefreshRate1s,      /**< 1s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/ 
    eRefreshRate3s,      /**< 3s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/
    eRefreshRate5s,      /**< 5s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/
    eRefreshRate10s,     /**< 10s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/
    eRefreshRate30s,     /**< 30s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/
    eRefreshRate1min,    /**< 1min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/
    eRefreshRate5min,    /**< 5min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/
    eRefreshRate10min    /**< 10min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate*/
  }eRefreshRate_t;

  /**
   * @fn DFRobot_RP2040_SCI
   * @brief DFRobot_RP2040_SCI Class Constructor.
   */
  DFRobot_RP2040_SCI();

  /**
   * @fn ~DFRobot_RP2040_SCI
   * @brief DFRobot_RP2040_SCI Class Destructor. 
   */
  ~DFRobot_RP2040_SCI();
  
  /**
   * @fn begin
   * @brief Initalize the SCI Acquisition Module, mainly for initializing communication interface
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
   * @n The version number is 16-bit data, the high 8bits(b15-b9) represent the leftmost number
   * @n The middle 4bits (b8-b4) represent the middle number
   * @n The low 4bits represent the rightmost number 
   * @n For example, 0x0123 corresponds to V1.2.3
   * 
   * @return 16-bit version number
   */
  uint16_t getVersion();
  /**
   * @fn getVersionDescription
   * @brief Get version description char string
   * 
   * @return Return version description char string, e.g. id：0x0123 The returned version decription char string is V1.2.3
   */
  String getVersionDescription(uint16_t version);

  /**
   * @fn setPort1(char *sku)
   * @brief SKU on Port1, which can be connected to analog & digital sensors, select the sensor connected to Port1 by SKU
   * 
   * @param sku  Parameters for Port1, the supported SKU list can be viewed on OLED display or by getAnalogSensorSKU()/getDigitalSensorSKU()
   * @n     "NULL"       Clear sensor settings for Port1 and configure mode as analog sensor mode
   * @n     "Analog"     Select analog voltage data acquisition, unit mV
   * @n     Analog sensor SKU  Select the SKU of an analog sensor and configure mode as analog sensor mode
   * @n     Digital sensor SKU Select the SKU of a digital sensor and configure mode as digital sensor mode
   * @return uint8_t Error Code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller(master)
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  Peripheral(slave) fault
   * @n      ERR_CODE_ARGS         or 0x07  Set wrong parameters 
   */
  uint8_t setPort1(char *sku);

  /**
   * @fn getPort1(ePort1IFMode_t mode)
   * @brief Get the sensor mode on port1 and SKU config
   * 
   * @param mode  eADIFMode_t enum variable pointer
   * @n     eAnalogMode    Analog sensor mode
   * @n     eDigitalMode   Digital sensor mode
   * @return SKU of the sensor connected to port1
   * @n      "NULL"        Port1 is configured or connected to no sensor 
   * @n      "Analog"      Port1 is configured as reading its voltage data
   * @n       7-bit SKU        Port1 is configured as reading data from a digital or analog sensor
   */
  String getPort1(ePort1IFMode_t *mode);

  /**
   * @fn setPort2(char *sku)
   * @brief Set SKU on Port2, which can be connected to I2C & UART sensors. I2C sensors can be auto selected when connected, 
     @ you just need to configure the mode as I2C mode for port2. But for UART sensors, please select by SKU. 
   * 
   * @param sku  Parameters for Port2, the supported SKU list can be viewed on the OLED display or by getUARTSensorSKU()
   * @n     "NULL"       Configure Port2 as I2C mode and clear the config related to UART sensor on Port2
   * @n     UART sensor SKU indicates a UART sensor SKU is selected and the mode is configured as UART sensor mode
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  Peripheral fault
   * @n      ERR_CODE_ARGS         or 0x07  Set wrong parameters 
   * @n      ERR_CODE_SKU          or 0x08  The SKU is an invalid SKU, or unsupported by SCI Acquisition Module
   * @n      ERR_CODE_S_NO_SPACE   or 0x09  Insufficient memory of I2C peripheral(slave)
   */
  uint8_t setPort2(char *sku);

  /**
   * @fn getPort2(ePort23Mode_t mode)
   * @brief Get the sensor mode on port2 and SKU config
   * 
   * @param mode  eI2CUARTMode_t enum variable pointer
   * @n     eI2CMode    I2C sensor mode
   * @n     eUARTMode   UART sensor mode
   * @return SKU of the sensor connected to Port2
   * @n      "NULL"        Port2 is configured or connected to no sensor
   * @n      7-bit SKU set     The SKU corresponding to I2C or UART sensor
   */
  String getPort2(ePort23Mode_t *mode);

  /**
   * @fn setPort3(char *sku)
   * @brief Set SKU on Port3, which can be connected to I2C & UART sensors. I2C sensors can be auto selected when connected,
     @ you just need to configure the mode as I2C mode for port2. But for UART sensors, please select by SKU.
   * 
   * @param sku  Parameters for Port3, the supported SKU list can be viewed on the OLED display or by getUARTSensorSKU()
   * @n     "NULL"       Configure Port3 as I2C mode and clear the config related to UART sensors on Port3
   * @n     UART sensor SKU indicates a UART sensor SKU is selected and the mode is configured as UART sensor mode
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
   * @n      ERR_CODE_SLAVE_BREAK  or 0x06  Peripheral fault
   * @n      ERR_CODE_ARGS         or 0x07  Set wrong parameters 
   */
  uint8_t setPort3(char *sku);

  /**
   * @fn getPort3(ePort23Mode_t mode)
   * @brief Get the sensor mode on port3 and SKU config
   * 
   * @param mode  eI2CUARTMode_t enum variable pointer
   * @n     eI2CMode    I2C sensor mode
   * @n     eUARTMode   UART sensor mode
   * @return SKU of the sensor connected to Port3
   * @n      "NULL"        Port3 is configured or connected to no sensor 
   * @n      7-bit SKU set     The SKU corresponding to I2C or UART sensor
   */
  String getPort3(ePort23Mode_t *mode);

  /**
   * @fn setRecvTimeout
   * @brief Set receive timeout
   * 
   * @param timeout When there are many sensors connected to SCI Acquisition Module, you need to increase the receive timeout value appropriately when reading a large amount of data, default is 2s
   */
  void setRecvTimeout(uint32_t timeout = 2000);
  /**
   * @fn adjustRtc(const __FlashStringHelper* date, const __FlashStringHelper* time)
   * @brief Set time of SCI Acquisition Module
   * 
   * @param date Year, month & day
   * @param time Hour, minute & second
   * @return Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed 
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error 
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout 
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command 
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
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed 
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command 
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error 
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout 
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   */
  uint8_t adjustRtc(uint16_t year, uint8_t month, uint8_t day, uint8_t week, uint8_t hour, uint8_t minute, uint8_t second);
  /**
   * @fn getRtcTime(uint16_t *year, uint8_t *month, uint8_t *day, uint8_t *week, uint8_t *hour, uint8_t *minute, uint8_t *second)
   * @brief Get year, month, day, week, hour, minute, second of SCI Acquisition Module
   * 
   * @param year   Year
   * @param month  Month
   * @param day    Day
   * @param week   Week
   * @param hour   Hour
   * @param minute Minute
   * @param second Second
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed 
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command 
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error 
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout 
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   */
  uint8_t getRtcTime(uint16_t *year, uint8_t *month, uint8_t *day, uint8_t *week, uint8_t *hour, uint8_t *minute, uint8_t *second);
  /**
   * @fn getRtcTime()
   * @brief Get the year, month, day, week, hour, minute, second of the SCI Acquisition Module
   * 
   * @return The char string for year/month/day week hour:minute:second, for example, 2022/08/09 2 09:08:00 represents Tuesday, August 9, 2022, at 9:08:0 
   */
  String getRtcTime();
  /**
   * @fn setRefreshRate
   * @brief Set data refresh rate
   * 
   * @param refreshRate eRefreshRate_t enum variable
   * @n eRefreshRateMs     ms-level, refresh at the actual refresh rate
   * @n eRefreshRate1s     1s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate3s     3s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate5s     5s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate10s    10s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate30s    30s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate1min   1min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate5min   5min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate10min  10min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   */
  uint8_t setRefreshRate(eRefreshRate_t refreshRate);
  /**
   * @fn getRefreshRate
   * @brief Get the set refresh rate, which may not be the actual rate, the relationship between them is: the set refresh rate <= the actual refresh rate
   * 
   * @param refreshRate eRefreshRate_t enum variable, get the level
   * @n eRefreshRateMs     ms-level, refresh at the actual refresh rate
   * @n eRefreshRate1s     1s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate 
   * @n eRefreshRate3s     3s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate5s     5s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate10s    10s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate30s    30s, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate1min   1min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate5min   5min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
   * @n eRefreshRate10min  10min, if the actual data refresh rate is less than this value, refresh at this rate, if greater than it, refresh at actual rate
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
   * @brief Get time stamp, also the data refresh time of SCI Acquisition Module
   * 
   * @return Hour:Minute:Second(00:00:00) or Minute:Second. X%(0-99)second(00:00.00)
   */
  String getTimeStamp();
  
  /**
   * @fn getSensorModeDescribe(ePort1IFMode_t mode)
   * @brief Get sensor mode description
   * 
   * @param mode  ePort1IFMode_t enum variable
   * @n     eAnalogMode    Analog sensor mode
   * @n     eDigitalMode   Digital sensor mode
   * @return Sensor mode description char string
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
   * @return Sensor mode description char string
   * @n      "I2C"         I2C sensor mode
   * @n      "UART"        UART sensor mode
   * @n      "UNKNOWN"     Unknown Mode
   */
  String getSensorModeDescribe(ePort23Mode_t mode);
  
  /**
   * @fn enableRecord
   * @brief Enable data recording in CSV file. When enabled, the sensor data will be recorded in the csv file named by date year, month, day, hour, minute, and second.
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   */
  uint8_t enableRecord();
  /**
   * @fn disableRecord
   * @brief Disable data recording in CSV file. When disabled, data recording stops
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   */
  uint8_t disableRecord();
  
  /**
   * @fn oledScreenOn
   * @brief Switch on SCI Acquisition Module Screen
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   */
  uint8_t oledScreenOn();
  /**
   * @fn oledScreenOff
   * @brief Switch off SCI Acquisition Module Screen
   * 
   * @return uint8_t Error code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response package error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response package receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command package or unmatched command
   */
  uint8_t oledScreenOff();
  
  /**
   * @fn getInformation
   * @brief Get information of the sensor connected to one or more ports of SCI Acquisition Module, name: value unit.
   * @n Separate multiple pieces of information using ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @param timestamp Whether the acquired information is timestamped or not
   * @n     false  Not timestamped
   * @n     ture   Timestamped   
   * @return Attributes of the sensor connected to the selected port, each one is in the format of name:value unit, separate attributes using "," and separate unit and value using a space
   * @n Not timestamped e.g. SEN0334:  Temp_Air:28.65 C,Humi_Air:30.12 %RH
   * @n Timestamped   e.g.SEN0334:  Minute:Second. X%(0-99)second Temp_Air:28.65 C,Humi_Air:30.12 %RH or Hour:Minute:Second Temp_Air:28.65 C,Humi_Air:30.12 %RH
   */
  String getInformation(eInterfaceList_t inf = eALL, bool timestamp = false);
  String getInformation(uint8_t inf, bool timestamp = false);

  /**
   * @fn getSKU
   * @brief Get the SKUs of the sensor connected to one or more ports of SCI Acquisition Module, separate SKUs using ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The SKUs of the sensor connected to the selected port, separate SKUs using ","
   * @n For example:  SEN0161,SEN0334
   */
  String getSKU(eInterfaceList_t inf = eALL);
  String getSKU(uint8_t inf);

  /**
   * @fn getKeys
   * @brief Get the name of the sensor connected to one or more ports, separate names using ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The name of the sensor connected to the selected port, separate names using ","
   * @n For example:  Temp_Air,Humi_Air
   */
  String getKeys(eInterfaceList_t inf = eALL);
  String getKeys(uint8_t inf);
  /**
   * @fn getValues
   * @brief Get attribute values of the sensor connected to one or more ports, separate attribute values using ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The attribute values of the sensor connected to the selected port, separate attribute values using ","
   * @n For example:  28.65,30.12
   */
  String getValues(eInterfaceList_t inf = eALL);
  String getValues(uint8_t inf);
  /**
   * @fn getUnits
   * @brief Get the value unit of the sensor connected to one or more ports, separate units using ","
   * 
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   * @return The value unit of the sensor connected to the selected port, separate units using ","
   * @n For example:  C,%RH
   */
  String getUnits(eInterfaceList_t inf = eALL);
  String getUnits(uint8_t inf);

  /**
   * @fn getValue(char *keys)
   * @brief Get data values of the attribute named keys from sensors connected to all ports. Separate attribute values using "," 
   * @param keys  Sensor attribute name
   * @return Data values of the attribute named keys from sensors connected to all ports. Separate attribute values using ","
   * @n For example, Temp_Air:  28.65,28.65
   */
  String getValue(char *keys);
  /**
   * @fn getValue(eInterfaceList_t inf, char *keys)
   * @brief Get data values of the attribute named keys from sensors connected to the designated port. Separate attribute values using ","
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select Port1, and search data values of the attribute named keys from sensors connected to A&D ports
   * @n     ePort2                                          Select Port2, and search data values of the attribute named keys from sensors connected to I2C&UART1 ports
   * @n     ePort3                                          Select Port3, and search data values of the attribute named keys from sensors connected to I2C&UART2 ports
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)            Select ePort1, ePort2 & ePort3, and search data values of the attribute named keys from sensors connected to all ports
   * @param keys  Sensor attribute name
   * @return The data values of the attribute named keys from sensors connected to the designated port. Separate attribute values using ","
   * @n For example, Temp_Air:  28.65,28.65
   */
  String getValue(eInterfaceList_t inf, char *keys);
  String getValue(uint8_t inf, char *keys);
  /**
   * @fn getValue(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data values of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port.
   * @ Separate attribute values using ","
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select port1, search get the sensor whose SKU is sku from port1, and read data values of the attribute named keys
   * @n     ePort2                                          Select port2, search get the sensor whose SKU is sku from port2, and read data values of the attribute named keys
   * @n     ePort3                                          Select port3, search get the sensor whose SKU is sku from port3, and read data values of the attribute named keys
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)            Select ePort1, ePort2 and ePort3, search sensors whose SKU is sku from all ports, 
   * @                                                      and read data values of the attribute named keys
   * @param sku Sensor SKU
   * @param keys  Sensor attribute name
   * @return The data values of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port. 
   * @ Separate attribute values using ","
   * @n For example, Temp_Air:  28.65,28.65
   */
  String getValue(eInterfaceList_t inf, char sku[7], char *keys);
  String getValue(uint8_t inf, char sku[7], char *keys);

  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data units of the attribute named keys from sensors connected to all ports. Separate attribute units using ","
   * 
   * @param keys  Sensor attribute name
   * @return  Data units of the attribute named keys from sensors connected to all ports. Separate attribute units using ","
   * @n For example, Temp_Air:  C,C
   */
  String getUnit(char *keys);
  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data units of the attribute named keys from sensors connected to the designated port. Separate attribute units using ","
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select Port1, and search data units of the attribute named keys from sensors connected to port1
   * @n     ePort2                                          Select Port2, and search data units of the attribute named keys from sensors connected to port2
   * @n     ePort3                                          Select Port3, and search data units of the attribute named keys from sensors connected to port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select Port1, Port2 and Port3, and search data units of the attribute named keys from sensors connected to all ports 
   * @param keys  Sensor attribute name
   * @return The data units of the attribute named keys from sensors connected to the designated port. Separate attribute units using ","
   * @n For example, Temp_Air:  C,C
   */
  String getUnit(eInterfaceList_t inf, char *keys);
  String getUnit(uint8_t inf, char *keys);
  /**
   * @fn getUnit(eInterfaceList_t inf, char sku[7], char *keys)
   * @brief Get data units of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port.
   * @ Separate attribute units using ","
   * @param inf    Port select, and parameter search range
   * @n     ePort1                                          Select Port1, search the sensor whose SKU is sku from port1, and read data units of the attribute named keys
   * @n     ePort2                                          Select Port2, search the sensor whose SKU is sku from port2, and read data units of the attribute named keys
   * @n     ePort3                                          Select Port3, search the sensor whose SKU is sku from port3, and read data units of the attribute named keys
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)      Select Port1, Port2 and Port3, search sensors whose SKU is sku from all ports, 
   * @n                                               and read data units of the attribute named keys
   * @param sku Sensor SKU
   * @param keys  Sensor attribute name
   * @return The data units of the attribute named keys from the sensor with a specific sku among sensors connected to the designated port.
   * @n      Separate attribute units using ","
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

protected:
  uint32_t getRefreshRate_ms(uint8_t rate);
  /**
   * @fn recvPacket
   * @brief Receive and parse the response data packet
   * 
   * @param cmd       Command to receive packet
   * @param errorCode Receive error code
   * @return Pointer array
   * @n      NULL    indicates receiving packet failed
   * @n      Non-NULL  response packet pointer
   */
  void *recvPacket(uint8_t cmd, uint8_t *errorCode);
  /**
   * @fn init
   * @brief Pure virtual function, interface init
   * 
   * @param freq     Communication frequency
   * @return Init status
   * @n       0    Init succeeded
   * @n      -1    Interface object is null pointer
   * @n      -2    Device does not exist
   */
  virtual int init(uint32_t freq) = 0;
  /**
   * @fn sendPacket
   * @brief I2C interface init
   * 
   * @param pkt    Set I2C communication frequency
   * @param length Set I2C communication frequency
   * @param stop   
   * @n     true   Stop
   * @n     false  Not stop
   */
  virtual void sendPacket(void *pkt, int length, bool stop) = 0;
  /**
   * @fn recvData
   * @brief I2C interface init
   * 
   * @param data    Store the received data cache
   * @param len     Length of byte to be read
   * @return Actually read byte length    
   */
  virtual int recvData(void *data, int len) = 0;
  /**
   * @fn recvFlush
   * @brief Clear receive cache
   */
  virtual void recvFlush() = 0;
  /**
   * @fn sendFlush
   * @brief Clear send cache
   */
  virtual void sendFlush() = 0;
  /**
   * @fn dayOfTheWeek
   * @brief Calculate the day of the week according to year/month/day
   * 
   * @param year   Year
   * @param month  Month
   * @param day    Day
   * @return uint8_t Day of the week(0-6)
   * @n 0   Sunday
   * @n 1   Monday
   * @n 2   Tuesday
   * @n 3   Wednesday
   * @n 4   Thursday
   * @n 5   Friday
   * @n 6   Saturday
   */
  uint8_t dayOfTheWeek(uint16_t year, uint8_t month, uint8_t day);
 	/**
   * @fn date2days
   * @brief Calculate the number of days between the current date year/month/day and January 1, 2000
   * 
   * @param y   Year
   * @param m   Month
   * @param d   Day
   * @return uint16_t The number of days between the current date year/month/day and January 1, 2000
   * @note Only calculations from 2000 to 2099 are guaranteed to be accurate
   */
  uint16_t date2days(uint16_t y, uint8_t m, uint8_t d);
  /**
   * @fn conv2d
   * @brief Convert characters to 2-bit decimal data
   * 
   * @param p Pointer to array
   * @return uint8_t Return 2-bit decimal data
   */
	uint8_t conv2d(const char* p);
  /**
   * @fn reset
   * @brief Reset the cache sending of SCI Acquisition Module
   * 
   * @param cmd Communication command
   */
  void reset(uint8_t cmd);

private:
  uint32_t _timeout; ///< Time of receive timeout
};

class DFRobot_RP2040_SCI_IIC: public DFRobot_RP2040_SCI{
public:
  /**
   * @fn DFRobot_RP2040_SCI_IIC
   * @brief Constructor for DFRobot_RP2040_SCI_IIC class.
   * @param addr:  7-bit I2C address, support the following address settings
   * @n RP2040_SCI_ADDR_0X21      0x21 default I2C address
   * @n RP2040_SCI_ADDR_0X22      0x22
   * @n RP2040_SCI_ADDR_0X23      0x23
   * @n Or view I2C address on the initial page of the onboard OLED display, the factory default I2C address is 0x01
   * @param pWire:   TwoWire class & object pointer.
   */
  DFRobot_RP2040_SCI_IIC(uint8_t addr = RP2040_SCI_ADDR_0X21, TwoWire *pWire = &Wire);
  ~DFRobot_RP2040_SCI_IIC();
  /**
   * @fn setI2CAddress
   * @brief Set I2C address of SCI Acquisition Module
   * 
   * @param addr    I2C address of SCI Acquisition Module, support the following address settings
   * @n RP2040_SCI_ADDR_0X21      0x21 default I2C address
   * @n RP2040_SCI_ADDR_0X22      0x22
   * @n RP2040_SCI_ADDR_0X23      0x23
   * @return uint8_t Error Code
   * @n      ERR_CODE_NONE         or 0x00  Setting succeed
   * @n      ERR_CODE_CMD_INVAILED or 0x01  Invalid command
   * @n      ERR_CODE_RES_PKT      or 0x02  Response packet error
   * @n      ERR_CODE_M_NO_SPACE   or 0x03  Insufficient memory of I2C controller(master) 
   * @n      ERR_CODE_RES_TIMEOUT  or 0x04  Response packet receive timeout
   * @n      ERR_CODE_CMD_PKT      or 0x05  Invalid command packet or unmatched command 
   * @n      ERR_CODE_I2C_ADRESS   or 0x0A  Invalid I2C address
   */
  uint8_t setI2CAddress(uint8_t addr);
  /**
   * @fn getI2CAddress
   * @brief Get the I2C address of SCI Acquisition Module
   * @return I2C address
   */
  uint8_t getI2CAddress();

protected:
  /**
   * @fn init
   * @brief Initalize I2C interface
   * 
   * @param freq Set I2C communication frequency
   * @return int Init status
   * @n       0  Init successful
   * @n      -1  The communication interface class & object are not passed in
   * @n      -2  Check if the hardware connection is correct
   */
  int init(uint32_t freq);
  /**
   * @fn sendPacket
   * @brief Send data
   * 
   * @param pkt    Data pointer
   * @param length Length of the data to be sent
   * @param stop   Whether to send stop condition
   * @n     true   Stop
   * @n     false  Not stop
   */
  void sendPacket(void *pkt, int length, bool stop = true);
  /**
   * @fn recvData
   * @brief I2C read byte
   * 
   * @param data    Received and stored data cache
   * @param len     Length of byte to be read
   * @return Actually read byte length   
   */
  int recvData(void *data, int len);
  /**
   * @fn recvFlush
   * @brief Clear receive cache
   */
  void recvFlush();
  /**
   * @fn sendFlush
   * @brief Clear send cache
   */
  void sendFlush();
private:
  TwoWire *_pWire;
  uint8_t _addr;
};
#endif
