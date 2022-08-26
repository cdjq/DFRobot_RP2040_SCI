/*!
 * @file DFRobot_RP2040_SUAB.h
 * @brief 这是一个传感器通用适配器板(Sensor Universal Adapter Board)，旨在配置适配器板参数，以及读取适配器板上各传感器的参数，具体功能如下所示：
 * @n 配置适配器板参数：
 * @n      1. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的I2C地址，范围1~5；
 * @n      2. 读取/设置传感器通用适配器板(Sensor Universal Adapter Board)的年，月，日，时，分，秒的时间；
 * @n      3. 开启/关闭数据记录，开启数据记录后，会将传感器通用适配器板(Sensor Universal Adapter Board)上各传感器的数据以CSV格式的文件记录下来保存到FLASH中，
 * @n  用户可以通过U盘拷贝或查看该CSV记录文件，CSV文件的名字是以开启记录那刻时的年_月_日_时_分_秒的时间命名的。
 * @n      4. 开启/关闭OLED屏显示，（开启显示，是进入初始化页面还是进入关闭前的页面）
 * @n      5. 读取/设置 对应A/D，I2C1/UART1，I2C2/UART2等接口所对应的功能，及传感器的SKU, 默认配置为(A, NULL),(I2C1, NULL),(I2C2, NULL), NULL表示对应的接口上没有传感器
 * @n 读取适配器板上各传感器的参数：
 * @n      1. 获取传感器数据的"名称"，各名称之间用逗号(,)隔开;;
 * @n      2. 获取传感器数据的"值"，各值之间用逗号(,)隔开;
 * @n      3. 获取传感器数据值的单位，各单位之间用逗号(,)隔开;；
 * @n      4. 获取接入传感器的SKU；
 * @n      5. 以名称:值 单位的方式获取完整的传感器信息，各信息之间用逗号（,）隔开
 *
 * @copyright   Copyright (c) 2022 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Arya](xue.peng@dfrobot.com)
 * @version  V1.0
 * @date  2022-07-20
 * @url https://github.com/DFRobot/DFRobot_RP2040_SUAB
 */
#ifndef DFROBOT_RP2040_SUAB_H
#define DFROBOT_RP2040_SUAB_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include <Wire.h>

#define RP2040_SUAB_DEF_I2C_ADDR   0x05 ///< 转换板默认I2C地址

class DFRobot_SUAB{
public:
  /**
   * @enum eInterfaceList_t
   * @brief 将要设置或者读取的接口
   */
  typedef enum{
    eAD         = 1 << 0, /**< 设置或读取A&D接口*/
    eI2C_UART1  = 1 << 1, /**< 设置或读取I2C&UART1接口*/
    eI2C_UART2  = 1 << 2, /**< 设置或读取I2C&UART2接口*/
    eALL        = 0x07    /**< 设置或读取A&D，I2C&UART1或I2C&UART2接口*/
  }eInterfaceList_t;

  /**
   * @enum eADIFMode_t
   * @brief A&D接口模式选择
   */
  typedef enum{
    eAnalogMode = 0,  /**< 模拟传感器模式*/
    eDigitalMode      /**< 数字传感器模式*/
  }eADIFMode_t;

  /**
   * @enum eI2CUARTMode_t
   * @brief I2C&UART接口模式选择
   */
  typedef enum{
    eI2CMode  = 0,   /**< I2C传感器模式*/
    eUARTMode        /**< UART传感器模式*/
  }eI2CUARTMode_t;

  /**
   * @fn DFRobot_RP2040_SUAB
   * @brief DFRobot_RP2040_SUAB类的构造函数.
   * @note SUAB: 是传感器通用适配器板(Sensor Universal Adapter Board)的缩写
   */
  DFRobot_SUAB();

  /**
   * @fn  ~DFRobot_RP2040_SUAB
   * @brief DFRobot_RP2040_SUAB类的析构函数. 
   * @note SUAB: 是传感器通用适配器板(Sensor Universal Adapter Board)的缩写
   */
  ~DFRobot_SUAB();
  
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

protected:
  /**
   * @fn valid
   * @brief 判断SKU是否有效或为NULL
   * 
   * @param sku  NULL或SKU
   * @return true    有效返回true
   * @return false   无效返回false
   */
  bool valid(char *sku);
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
   * @brief 复位传感器通用适配器板(Sensor Universal Adapter Board)的发送缓存
   * 
   * @param cmd 通信命令
   */
  void reset(uint8_t cmd);

private:
  uint32_t _timeout; ///< 接收超时时间
};

class DFRobot_RP2040_SUAB_IIC: public DFRobot_SUAB{
public:
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
