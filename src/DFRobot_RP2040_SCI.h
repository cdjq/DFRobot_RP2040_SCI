/*!
 * @file DFRobot_RP2040_SCI.h
 * @brief 这是基于Arduino平台的一个SCI采集模块(SCI Acquisition Module)驱动库，用户可以通过I2C接口读取或设置SCI采集模块的相关配置和数据，具体功能如下所述：
 * @n 1. 设置或读取SCI采集模块的I2C通信地址为0x21、0x22或0x23，出厂默认为0x21，I2C地址修改后，掉电重启后生效；
 * @n 2. 设置或读取Port1、Port2或Port3接口的配置：
 * @n    Port1: 可配置为模拟传感器模式或数字传感器模式，模拟传感器模式下，支持NULL、Analog、模拟传感器SKU，数字传感器模式下，支持数字传感器SKU
 * @n    Port2: 可配置为I2C传感器模式或UART传感器模式，I2C传感器模式下：支持NULL或I2C传感器，在此模式下，I2C传感器上电将被模块自动识别，UART传感器模式下，支持UART传感器SKU
 * @n    Port3: 可配置为I2C传感器模式或UART传感器模式，I2C传感器模式下：支持NULL或I2C传感器，在此模式下，I2C传感器上电将被模块自动识别，UART传感器模式下，支持UART传感器SKU
 * @n 3. 开启/关闭数据CSV文件记录
 * @n 4. 开启/关闭OLED屏显示
 * @n 5. 读取适配器板上各传感器的参数：
 * @n      a. 获取传感器数据的"名称"，各名称之间用逗号(,)隔开;;
 * @n      b. 获取传感器数据的"值"，各值之间用逗号(,)隔开;
 * @n      c. 获取传感器数据值的单位，各单位之间用逗号(,)隔开;；
 * @n      d. 获取接入传感器的SKU；
 * @n      e. 以名称:值 单位的方式获取完整的传感器信息，各信息之间用逗号（,）隔开
 * @n 6.设置和读取数据刷新时间
 * @n 7.获取数据刷新时间戳
 *
 * @copyright   Copyright (c) 2022 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Arya](xue.peng@dfrobot.com)
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


/* SCI支持的I2C地址 */
#define RP2040_SCI_ADDR_0X21      0x21 ///< 转换板默认I2C地址
#define RP2040_SCI_ADDR_0X22      0x22
#define RP2040_SCI_ADDR_0X23      0x23

class DFRobot_SCI{
public:
  /**
   * @enum eInterfaceList_t
   * @brief 将要设置或者读取的接口
   */
  typedef enum{
    ePort1         = 1 << 0, /**< Port1接口，模拟或数字传感器接口*/
    ePort2         = 1 << 1, /**< Port2接口，I2C或UART传感器接口*/
    ePort3         = 1 << 2, /**< Port3接口，I2C或UART传感器接口*/
    eALL           = 0x07    /**< Port1，Port2，Port3接口*/
  }eInterfaceList_t;

  /**
   * @enum ePort1IFMode_t
   * @brief Port1接口模式选择
   */
  typedef enum{
    eAnalogMode = 0,  /**< 模拟传感器模式*/
    eDigitalMode      /**< 数字传感器模式*/
  }ePort1IFMode_t;

  /**
   * @enum ePort23Mode_t
   * @brief Port2或Port3接口模式选择
   */
  typedef enum{
    eI2CMode  = 0,   /**< I2C传感器模式*/
    eUARTMode        /**< UART传感器模式*/
  }ePort23Mode_t;

  typedef enum{
    eRefreshRateMs = 0,  /**< ms级刷新率，按数据的实际刷新率刷新*/
    eRefreshRate1s,      /**< 刷新率1s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
    eRefreshRate3s,      /**< 刷新率3s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
    eRefreshRate5s,      /**< 刷新率5s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
    eRefreshRate10s,     /**< 刷新率10s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
    eRefreshRate30s,     /**< 刷新率30s，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
    eRefreshRate1min,    /**< 刷新率1min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
    eRefreshRate5min,    /**< 刷新率5min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
    eRefreshRate10min    /**< 刷新率10min，如果数据实际刷新时间小于此值，则按此值刷新，若大于此值，则按数据实际刷新率刷新*/
  }eRefreshRate_t;

  /**
   * @fn DFRobot_RP2040_SCI
   * @brief DFRobot_RP2040_SCI类的构造函数.
   */
  DFRobot_SCI();

  /**
   * @fn  ~DFRobot_RP2040_SCI
   * @brief DFRobot_RP2040_SCI类的析构函数. 
   */
  ~DFRobot_SCI();
  
  /**
   * @fn begin
   * @brief SCI采集模块(SCI Acquisition Module)初始化，旨在初始化通信接口
   * 
   * @param freq 设置通信频率,不能超过100kHz
   * @return int 初始化状态
   * @n       0  初始化成功
   * @n      -1  通信接口类对象未传入
   * @n      -2  请检测硬件连接是否正确
   */
  int begin(uint32_t freq = 100000);

  /**
   * @fn setPort1(char *sku)
   * @brief 设置Port1的SKU，此接口可连接模拟传感器和数字传感器，通过SKU选择Port1上连接的传感器
   * 
   * @param sku  Port1接口的参数，支持的SKU列表可以通过OLED显示或者 getAnalogSensorSKU()/getDigitalSensorSKU()查看
   * @n     "NULL"       表示清除Port1接口的传感器设置,并将传感器模式配置为模拟传感器配置
   * @n     "Analog"     表示选择Analog电压数据采集，单位mV
   * @n     模拟传感器SKU 表示选择了某个模拟传感器的SKU，并将模式配置为模拟传感器模式
   * @n     数字传感器SKU 表示选择了某个数字传感器的SKU，并将模式配置为数字传感器模式
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
  uint8_t setPort1(char *sku);

  /**
   * @fn getPort1(ePort1IFMode_t mode)
   * @brief 获取Port1接口的传感器模式，及SKU配置
   * 
   * @param mode  eADIFMode_t枚举变量指针
   * @n     eAnalogMode    模拟传感器模式
   * @n     eDigitalMode   数字传感器模式
   * @return 接口0连接的传感器的SKU
   * @n      "NULL"        表示Port1接口没有配置或连接传感器
   * @n      "Analog"      表示Port1接口被配置为读取Port1接口两端的电压数据
   * @n      7位SKU        表示Port1接口被配置为读数字或模拟传感器的数据
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

protected:
  uint32_t getRefreshRate_ms(uint8_t rate);
  /**
   * @fn recvPacket
   * @brief 接收并解析响应的数据包
   * 
   * @param cmd       要接收包的命令
   * @param errorCode 接收错误代码
   * @return 指针数组
   * @n      NULL    表示接收包失败
   * @n      非NULL  响应包指针
   */
  void *recvPacket(uint8_t cmd, uint8_t *errorCode);
  /**
   * @fn init
   * @brief 纯虚函数，接口初始化
   * 
   * @param freq     通信频率
   * @return 初始化状态
   * @n       0    初始化成功
   * @n      -1    接口对象为空指针
   * @n      -2    设备不存在
   */
  virtual int init(uint32_t freq) = 0;
  /**
   * @fn sendPacket
   * @brief I2C接口初始化
   * 
   * @param pkt    设置I2C通信频率
   * @param length 设置I2C通信频率
   * @param stop   
   * @n     true   停止
   * @n     false  不停止
   */
  virtual void sendPacket(void *pkt, int length, bool stop) = 0;
  /**
   * @fn recvData
   * @brief I2C接口初始化
   * 
   * @param data    存放接收的数据缓存
   * @param len     要读取得字节数
   * @return 实际读取得字节数   
   */
  virtual int recvData(void *data, int len) = 0;
  /**
   * @fn recvFlush
   * @brief 清空接收缓存
   */
  virtual void recvFlush() = 0;
  /**
   * @fn sendFlush
   * @brief 清空发送缓存
   */
  virtual void sendFlush() = 0;
  /**
   * @fn dayOfTheWeek
   * @brief 根据年/月/日计算星期数
   * 
   * @param year   年
   * @param month  月
   * @param day    日
   * @return uint8_t 0~6星期数
   * @n 0   星期天
   * @n 1   星期一
   * @n 2   星期二
   * @n 3   星期三
   * @n 4   星期四
   * @n 5   星期五
   * @n 6   星期六
   */
  uint8_t dayOfTheWeek(uint16_t year, uint8_t month, uint8_t day);
 	/**
   * @fn date2days
   * @brief 计算当前年月日距2000年1月1日相差的天数
   * 
   * @param year   年
   * @param month  月
   * @param day    日
   * @return uint16_t 天数，当前年月日距离2000年1月1日的天数
   * @note 只能保证2000年到2099年的计算是准确的
   */
  uint16_t date2days(uint16_t y, uint8_t m, uint8_t d);
  /**
   * @fn conv2d
   * @brief 将字符转换为2位10进制数据
   * 
   * @param p 指向数组的指针
   * @return uint8_t 返回2位十进制数据
   */
	uint8_t conv2d(const char* p);
  /**
   * @fn reset
   * @brief 复位SCI采集模块(SCI Acquisition Module)的发送缓存
   * 
   * @param cmd 通信命令
   */
  void reset(uint8_t cmd);

private:
  uint32_t _timeout; ///< 接收超时时间
};

class DFRobot_RP2040_SCI_IIC: public DFRobot_SCI{
public:
  /**
   * @fn DFRobot_RP2040_SCI_IIC
   * @brief DFRobot_RP2040_SCI_IIC 类的构造函数.
   * @param addr:  7位I2C地址，支持以下地址设置
   * @n RP2040_SCI_ADDR_0X21      0x21 转换板默认I2C地址
   * @n RP2040_SCI_ADDR_0X22      0x22
   * @n RP2040_SCI_ADDR_0X23      0x23
   * @n 或通过板子的OLED屏的初始页查看I2C地址，出厂默认I2C地址为0x01
   * @param pWire:   TwoWire类对象指针.
   */
  DFRobot_RP2040_SCI_IIC(uint8_t addr = RP2040_SCI_ADDR_0X21, TwoWire *pWire = &Wire);
  ~DFRobot_RP2040_SCI_IIC();
  /**
   * @fn setI2CAddress
   * @brief 设置SCI采集模块(SCI Acquisition Module)的I2C通信地址
   * 
   * @param addr    SCI采集模块(SCI Acquisition Module)的I2C通信地址，支持以下地址设置
   * @n RP2040_SCI_ADDR_0X21      0x21 转换板默认I2C地址
   * @n RP2040_SCI_ADDR_0X22      0x22
   * @n RP2040_SCI_ADDR_0X23      0x23
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
   * @brief 获取SCI采集模块(SCI Acquisition Module)的I2C通信地址
   * @return I2C通信地址
   */
  uint8_t getI2CAddress();

protected:
  /**
   * @fn init
   * @brief I2C接口初始化
   * 
   * @param freq 设置I2C通信频率
   * @return int 初始化状态
   * @n       0  初始化成功
   * @n      -1  通信接口类对象未传入
   * @n      -2  请检测硬件连接是否正确
   */
  int init(uint32_t freq);
  /**
   * @fn sendPacket
   * @brief 发送数据
   * 
   * @param pkt    数据指针
   * @param length 要发送的数据的长度
   * @param stop   是否发送停止条件
   * @n     true   停止
   * @n     false  不停止
   */
  void sendPacket(void *pkt, int length, bool stop = true);
  /**
   * @fn recvData
   * @brief I2C读取字节
   * 
   * @param data    存放接收的数据缓存
   * @param len     要读取得字节数
   * @return 实际读取得字节数   
   */
  int recvData(void *data, int len);
  /**
   * @fn recvFlush
   * @brief 清空接收缓存
   */
  void recvFlush();
  /**
   * @fn sendFlush
   * @brief 清空发送缓存
   */
  void sendFlush();
private:
  TwoWire *_pWire;
  uint8_t _addr;
};
#endif
