/*!
 * @file DFRobot_RP2040_SCI.cpp
 * @brief This is an Arduino drive library for the DFRobot SCI Acquisition module. Users can read or set its config and data via I2C. The following demonstrates its detailed functions:
 * @n 1. Set or read the I2C address of the module as 0x21, 0x22 or 0x23, the factory default is 0x21, after the I2C address is changed, it will take effect after power-off and reboot;
 * @n 2. Set or read the config of Port1, Port2 or Port3:
 * @n    Port1: can be configured as analog or digital sensor mode, support NULL, Analog, and analog sensor SKU in analog sensor mode, and support digital sensor SKU in digital sensor mode
 * @n    Port2: can be configured as I2C or UART sensor mode, support NULL or I2C sensor in I2C sensor mode, in which I2C sensor will be automatically recognized by the module when powered on, and support UART sensor SKU in UART sensor mode
 * @n    Port3: can be configured as I2C or UART sensor mode, support NULL or I2C sensor in I2C sensor mode, in which I2C sensor will be automatically recognized by the module when powered on, and support UART sensor SKU in UART sensor mode
 * @n 3. Enable/disable data recording in CSV file
 * @n 4. Enable/disable OLED display
 * @n 5. Read the parameters of the sensors connected to the SCI Acquisition module：
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
#include <Arduino.h>
#include "DFRobot_RP2040_SCI.h"

 // #define RP2040_SUAB_DBG_ENABLE

#ifdef RP2040_SUAB_DBG_ENABLE
#define DEBUG_SERIAL  Serial
#define RP2040_SUAB_DBG(...) {DEBUG_SERIAL.print("["); DEBUG_SERIAL.print(__FUNCTION__); DEBUG_SERIAL.print("(): "); DEBUG_SERIAL.print(__LINE__); Serial.print(" ] "); DEBUG_SERIAL.println(__VA_ARGS__);}
#else
#define RP2040_SUAB_DBG(...)
#endif
#define IIC_MAX_TRANSFER     32     ///< Maximum transferred data via I2C
#define CMD_START            0x00
#define CMD_SET_IF0          0x00  ///< Set port 0 command, which can be used to configure the function and SKU on A&D ports
#define CMD_SET_IF1          0x01  ///< Set port 1 command, which can be used to configure the function and SKU on I2C1 & UART1 ports 
#define CMD_SET_IF2          0x02  ///< Set port 2 command, which can be used to configure the function and SKU on I2C2 & UART2 ports
#define CMD_READ_IF0         0x00  ///< Read the function and SKU on port 0
#define CMD_READ_IF1         0x01  ///< Read the function and SKU on port 1
#define CMD_READ_IF2         0x02  ///< Read the function and SKU on port 2

#define CMD_SET_ADDR         0x03  ///< Set I2C address (the command will take effect immediately when it's set successfully)
#define CMD_READ_ADDR        0x03  ///< Read I2C address (the command will take effect immediately when it's set successfully)
#define CMD_SET_TIME         0x04  ///< Set year, month, day, hour, minute, second 
#define CMD_GET_TIME         0x04  ///< Get year, month, day, hour, minute, second
#define CMD_RECORD_ON        0x05  ///< Switch on CSV recording
#define CMD_RECORD_OFF       0x06  ///< Switch off CSV recording

#define CMD_SCREEN_ON        0x07  ///< Switch on OLED display
#define CMD_SCREEN_OFF       0x08  ///< Switch on OLED display
#define CMD_GET_NAME         0x09  ///< Get sensor data name
#define CMD_GET_VALUE        0x0A  ///< Get sensor data value
#define CMD_GET_UNIT         0x0B  ///< Get sensor data unit
#define CMD_GET_SKU          0x0C  ///< Get sensor SKU, separate SKUs by a comma(,) 
#define CMD_GET_INFO         0x0D  ///< Get the sensor data name, value and unit name, separate value and unit name by space, and others by comma(,)

#define CMD_GET_KEY_VALUE0    0x0E  ///< Get the corresponding data value according to the data name
#define CMD_GET_KEY_VALUE1    0x0F  ///< Get the data value on the selected port according to the data name
#define CMD_GET_KEY_VALUE2    0x10  ///< Get the data value of the designated SKU on the selected port according to the data name
#define CMD_GET_KEY_UINT0     0x11  ///< Get the corresponding data unit according to the data name
#define CMD_GET_KEY_UINT1     0x12  ///< Get the data unit on the selected port according to the data name
#define CMD_GET_KEY_UINT2     0x13  ///< Get the data unit of the designated SKU on the selected port according to the data name
#define CMD_RESET             0x14  ///< Reset I2C peripheral(slave) transmitting cache
#define CMD_SKU_A             0x15  ///< Get the supported analog sensor SKU 
#define CMD_SKU_D             0x16  ///< Get the supported digital sensor SKU
#define CMD_SKU_IIC           0x17  ///< Get the supported I2C sensor SKU
#define CMD_SKU_UART          0x18  ///< Get the supported UART sensor SKU
#define CMD_GET_TIMESTAMP     0x19  ///< Get timestamp
#define CMD_SET_REFRESH_TIME  0x20  ///< Set refresh rate
#define CMD_GET_REFRESH_TIME  0x20  ///< Get refresh rate
#define CMD_GET_VERSION       0x21  ///< Get version number

#define CMD_END             CMD_GET_VERSION

#define STATUS_SUCCESS      0x53  ///< Status of successful response   
#define STATUS_FAILED       0x63  ///< Status of failed response 

#define DEBUG_TIMEOUT_MS    2000

#define ERR_CODE_NONE               0x00 ///< Normal communication 
#define ERR_CODE_CMD_INVAILED       0x01 ///< Invalid command
#define ERR_CODE_RES_PKT            0x02 ///< Response packet error
#define ERR_CODE_M_NO_SPACE         0x03 ///< Insufficient memory of I2C controller(master)
#define ERR_CODE_RES_TIMEOUT        0x04 ///< Response packet reception timeout
#define ERR_CODE_CMD_PKT            0x05 ///< Invalid command packet or unmatched command
#define ERR_CODE_SLAVE_BREAK        0x06 ///< Peripheral(slave) fault
#define ERR_CODE_ARGS               0x07 ///< Set wrong parameter
#define ERR_CODE_SKU                0x08 ///< The SKU is an invalid SKU, or unsupported by SCI Acquisition Module
#define ERR_CODE_S_NO_SPACE         0x09 ///< Insufficient memory of I2C peripheral(slave)
#define ERR_CODE_I2C_ADRESS         0x0A ///< Invalid I2C address
#if defined(ESP32)
#define I2C_ACHE_MAX_LEN            32//128
#else
#define I2C_ACHE_MAX_LEN            32
#endif

#define SKU_MAX_VAILD_LEN           7
typedef struct {
  uint8_t cmd;      /**< Command                     */
  uint8_t argsNumL; /**< Low byte of parameter number after the command    */
  uint8_t argsNumH; /**< High byte of parameter number after the command    */
  uint8_t args[0];  /**< The array with 0-data length, its size depends on the value of the previous variables argsNumL and argsNumH     */
}__attribute__((packed)) sCmdSendPkt_t, * pCmdSendPkt_t;

typedef struct {
  uint8_t status;   /**< Response packet status, 0x53, response succeeded, 0x63, response failed */
  uint8_t cmd;      /**< Response packet command */
  uint8_t lenL;     /**< Low byte of the buf array length excluding packet header */
  uint8_t lenH;     /**< High byte of the buf array length excluding packet header */
  uint8_t buf[0];   /**< The array with 0-data length, its size depends on the value of the previous variables lenL and lenH */
}__attribute__((packed)) sCmdRecvPkt_t, * pCmdRecvPkt_t;

DFRobot_RP2040_SCI::DFRobot_RP2040_SCI()
  :_timeout(DEBUG_TIMEOUT_MS)
{
}

DFRobot_RP2040_SCI::~DFRobot_RP2040_SCI() {}

int DFRobot_RP2040_SCI::begin(uint32_t freq)
{
  return init(freq);
}

uint16_t DFRobot_RP2040_SCI::getVersion()
{
  uint16_t version = 0;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return version;
  sendpkt->cmd = CMD_GET_VERSION;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_VERSION, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    if (length == 2) {
      version = (rcvpkt->buf[0] << 8) | rcvpkt->buf[1];
    }
  }
  if (rcvpkt) free(rcvpkt);
  return version;
}

String DFRobot_RP2040_SCI::getVersionDescription(uint16_t version)
{
  String verstr = "V";
  verstr += String((version >> 8) & 0xFF) + ".";
  verstr += String((version >> 4) & 0x0F) + ".";
  verstr += String(version & 0x0F);
  return verstr;
}


uint8_t DFRobot_RP2040_SCI::setPort1(char* sku)
{
  uint8_t errorCode;
  pCmdSendPkt_t sendpkt = NULL;
  uint16_t length = 0;
  //1. Determine if the sku pointer is null
  if (sku == NULL) {
    RP2040_SUAB_DBG("sku pointer is NULL");
    return ERR_CODE_ARGS;
  }
  //2. Determine sku length
  if (strlen(sku) > SKU_MAX_VAILD_LEN) {
    RP2040_SUAB_DBG("sku length is too long!");
    return ERR_CODE_ARGS;
  }

  //3. Send command
  length = (strlen(sku) > SKU_MAX_VAILD_LEN) ? SKU_MAX_VAILD_LEN : strlen(sku);
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_SET_IF0;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  memcpy(sendpkt->args, sku, length);
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SET_IF0, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

String DFRobot_RP2040_SCI::getPort1(ePort1IFMode_t* mode)
{
  String config;
  *mode = (ePort1IFMode_t)0;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_READ_IF0;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_READ_IF0, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    if (mode) *mode = (ePort1IFMode_t)rcvpkt->buf[0];
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length];
    memcpy(sku, rcvpkt->buf + 1, length - 1);
    sku[length - 1] = '\0';
    config = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return config;
}

uint8_t DFRobot_RP2040_SCI::setPort2(char* sku)
{
  uint8_t errorCode;
  pCmdSendPkt_t sendpkt = NULL;
  uint16_t length = 0;
  //1. Determine if the sku pointer is null
  if (sku == NULL) {
    RP2040_SUAB_DBG("sku pointer is NULL");
    return ERR_CODE_ARGS;
  }
  //2. Determine sku length
  if (strlen(sku) > SKU_MAX_VAILD_LEN) {
    RP2040_SUAB_DBG("sku length is too long!");
    return ERR_CODE_ARGS;
  }

  //3. Send command
  length = (strlen(sku) > SKU_MAX_VAILD_LEN) ? SKU_MAX_VAILD_LEN : strlen(sku);
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_SET_IF1;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  memcpy(sendpkt->args, sku, length);
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SET_IF1, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

String DFRobot_RP2040_SCI::getPort2(ePort23Mode_t* mode)
{
  String config;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_READ_IF1;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_READ_IF1, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    if (mode) *mode = (ePort23Mode_t)rcvpkt->buf[0];
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length];
    memcpy(sku, rcvpkt->buf + 1, length - 1);
    sku[length - 1] = '\0';
    config = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return config;
}

uint8_t DFRobot_RP2040_SCI::setPort3(char* sku)
{
  uint8_t errorCode;
  pCmdSendPkt_t sendpkt = NULL;
  uint16_t length = 0;
  //1. Determine if the sku pointer is null
  if (sku == NULL) {
    RP2040_SUAB_DBG("sku pointer is NULL");
    return ERR_CODE_ARGS;
  }
  //2. Determine sku length
  if (strlen(sku) > SKU_MAX_VAILD_LEN) {
    RP2040_SUAB_DBG("sku length is too long!");
    return ERR_CODE_ARGS;
  }

  //3. Send command
  length = (strlen(sku) > SKU_MAX_VAILD_LEN) ? SKU_MAX_VAILD_LEN : strlen(sku);
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_SET_IF2;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  memcpy(sendpkt->args, sku, length);
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SET_IF2, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

String DFRobot_RP2040_SCI::getPort3(ePort23Mode_t* mode)
{
  String config;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_READ_IF2;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_READ_IF2, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    if (mode) *mode = (ePort23Mode_t)rcvpkt->buf[0];
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length];
    memcpy(sku, rcvpkt->buf + 1, length - 1);
    sku[length - 1] = '\0';
    config = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return config;
}

void DFRobot_RP2040_SCI::setRecvTimeout(uint32_t timeout)
{
  _timeout = timeout;
}

uint8_t DFRobot_RP2040_SCI::adjustRtc(const __FlashStringHelper* date, const __FlashStringHelper* time)
{
  char buff[11];
  memcpy_P(buff, date, 11);
  uint16_t year = conv2d(buff + 9);
  uint8_t month = 0;
  // Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
  switch (buff[0]) {
  case 'J': month = buff[1] == 'a' ? 1 : buff[2] == 'n' ? 6 : 7; break;   // hyy - Delete the second "month = "
  case 'F': month = 2; break;
  case 'A': month = buff[2] == 'r' ? 4 : 8; break;
  case 'M': month = buff[2] == 'r' ? 3 : 5; break;
  case 'S': month = 9; break;
  case 'O': month = 10; break;
  case 'N': month = 11; break;
  case 'D': month = 12; break;
  }
  uint8_t day = conv2d(buff + 4);
  memcpy_P(buff, time, 8);
  uint8_t hour = conv2d(buff);
  uint8_t minute = conv2d(buff + 3);
  uint8_t second = conv2d(buff + 6);

  uint8_t week = dayOfTheWeek(year, month, day);
  return adjustRtc(year, month, day, week, hour, minute, second);
}

uint8_t DFRobot_RP2040_SCI::adjustRtc(uint16_t year, uint8_t month, uint8_t day, uint8_t week, uint8_t hour, uint8_t minute, uint8_t second)
{
  uint8_t errorCode;
  pCmdSendPkt_t sendpkt = NULL;
  uint16_t length = sizeof(year) + sizeof(month) + sizeof(day) + sizeof(week) + sizeof(hour) + sizeof(minute) + sizeof(second);
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_SET_TIME;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = second;
  sendpkt->args[1] = minute;
  sendpkt->args[2] = hour;
  sendpkt->args[3] = day;
  sendpkt->args[4] = week;
  sendpkt->args[5] = month;
  sendpkt->args[6] = year & 0xFF;
  sendpkt->args[7] = (year >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SET_TIME, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

uint8_t DFRobot_RP2040_SCI::getRtcTime(uint16_t* year, uint8_t* month, uint8_t* day, uint8_t* week, uint8_t* hour, uint8_t* minute, uint8_t* second)
{
  uint8_t errorCode;
  pCmdSendPkt_t sendpkt = NULL;
  uint16_t length = 0;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_GET_TIME;
  sendpkt->argsNumL = 0;
  sendpkt->argsNumH = 0;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_TIME, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    if (length == 8) {
      if (second) *second = rcvpkt->buf[0];
      if (minute) *minute = rcvpkt->buf[1];
      if (hour)   *hour = rcvpkt->buf[2];
      if (day)    *day = rcvpkt->buf[3];
      if (week)   *week = rcvpkt->buf[4];
      if (month)  *month = rcvpkt->buf[5];
      if (year)   *year = rcvpkt->buf[6] | (rcvpkt->buf[7] << 8);
    }
  }
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

String DFRobot_RP2040_SCI::getRtcTime()
{
  uint8_t errorCode;
  String time = "";
  pCmdSendPkt_t sendpkt = NULL;
  uint16_t length = 0;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return time;
  sendpkt->cmd = CMD_GET_TIME;
  sendpkt->argsNumL = 0;
  sendpkt->argsNumH = 0;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_TIME, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    if (length == 8) {
      String second = "", minute = "", hour = "", day = "", week = "", month = "", year = "";
      if (rcvpkt->buf[0] < 10) second = "0";
      second += String(rcvpkt->buf[0]);

      if (rcvpkt->buf[1] < 10) minute = "0";
      minute += String(rcvpkt->buf[1]);

      if (rcvpkt->buf[2] < 10) hour = "0";
      hour += String(rcvpkt->buf[2]);

      if (rcvpkt->buf[3] < 10) day = "0";
      day += String(rcvpkt->buf[3]);

      week = String(rcvpkt->buf[4]);

      if (rcvpkt->buf[5] < 10) month = "0";
      month += String(rcvpkt->buf[5]);

      year = String(rcvpkt->buf[6] | (rcvpkt->buf[7] << 8));

      time = year + '/' + month + '/' + day + ' ' + week + ' ' + hour + ':' + minute + ':' + second;
    }
  }
  if (rcvpkt) free(rcvpkt);
  return time;
}

uint8_t DFRobot_RP2040_SCI::setRefreshRate(eRefreshRate_t refreshRate)
{
  uint8_t errorCode;
  uint16_t length = 1;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + 1);
  if (sendpkt == NULL) return ERR_CODE_S_NO_SPACE;
  sendpkt->cmd = CMD_SET_REFRESH_TIME;
  sendpkt->argsNumL = 1;
  sendpkt->argsNumH = 0;
  sendpkt->args[0] = (uint8_t)refreshRate;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SET_REFRESH_TIME, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}
uint32_t DFRobot_RP2040_SCI::getRefreshRate(eRefreshRate_t* refreshRate)
{
  //
  uint8_t rate;
  uint8_t errorCode;
  uint16_t length = 0;
  uint32_t rateTime = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return 0;
  sendpkt->cmd = CMD_GET_REFRESH_TIME;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_REFRESH_TIME, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    if (length) {
      rate = rcvpkt->buf[0];
      if (refreshRate) *refreshRate = (eRefreshRate_t)rate;
      rateTime = getRefreshRate_ms(rate);
    }
  }
  if (rcvpkt) free(rcvpkt);
  return rateTime;
}

String DFRobot_RP2040_SCI::getTimeStamp()
{
  String timestamp;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_TIMESTAMP;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_TIMESTAMP, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char data[length + 1];
    memcpy(data, rcvpkt->buf, length);
    data[length] = '\0';
    timestamp = String(data);
  }
  if (rcvpkt) free(rcvpkt);
  return timestamp;

}

String DFRobot_RP2040_SCI::getSensorModeDescribe(ePort1IFMode_t mode)
{
  switch (mode) {
  case eAnalogMode:
    return "ANALOG";
  case eDigitalMode:
    return "DIGITAL";
  default:
    return "UNKNOWN";
  }
}

String DFRobot_RP2040_SCI::getSensorModeDescribe(ePort23Mode_t mode)
{
  switch (mode) {
  case eI2CMode:
    return "I2C";
  case eUARTMode:
    return "UART";
  default:
    return "UNKNOWN";
  }
}

uint8_t DFRobot_RP2040_SCI::enableRecord()
{
  String config;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_RECORD_ON;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_RECORD_ON, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;

}
uint8_t DFRobot_RP2040_SCI::disableRecord()
{
  String config;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_RECORD_OFF;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_RECORD_OFF, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

uint8_t DFRobot_RP2040_SCI::oledScreenOn()
{
  String config;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_SCREEN_ON;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SCREEN_ON, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

uint8_t DFRobot_RP2040_SCI::oledScreenOff()
{
  String config;

  uint8_t errorCode;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_SCREEN_OFF;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SCREEN_OFF, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return errorCode;
}

String DFRobot_RP2040_SCI::getInformation(eInterfaceList_t inf, bool timestamp)
{
  return getInformation((uint8_t)inf, timestamp);
}

String DFRobot_RP2040_SCI::getInformation(uint8_t inf, bool timestamp)
{
  String info = "";

  uint8_t errorCode;
  uint16_t length = 2;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_INFO;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = (uint8_t)inf;
  sendpkt->args[1] = (uint8_t)timestamp;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_INFO, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    info = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return info;
}

String DFRobot_RP2040_SCI::getSKU(eInterfaceList_t inf)
{
  return getSKU((uint8_t)inf);
}

String DFRobot_RP2040_SCI::getSKU(uint8_t inf)
{
  String skus = "";

  uint8_t errorCode;
  uint16_t length = 1;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_SKU;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_SKU, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    skus = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return skus;
}

String DFRobot_RP2040_SCI::getKeys(eInterfaceList_t inf)
{
  return getKeys((uint8_t)inf);
}

String DFRobot_RP2040_SCI::getKeys(uint8_t inf)
{
  String name = "";

  uint8_t errorCode;
  uint16_t length = 1;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_NAME;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_NAME, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    name = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return name;
}

String DFRobot_RP2040_SCI::getValues(eInterfaceList_t inf)
{
  return getValues((uint8_t)inf);
}

String DFRobot_RP2040_SCI::getValues(uint8_t inf)
{
  String values = "";

  uint8_t errorCode;
  uint16_t length = 1;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_VALUE;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_VALUE, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    values = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return values;
}

String DFRobot_RP2040_SCI::getUnits(eInterfaceList_t inf)
{
  return getUnits((uint8_t)inf);
}

String DFRobot_RP2040_SCI::getUnits(uint8_t inf)
{
  String unit = "";

  uint8_t errorCode;
  uint16_t length = 1;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_UNIT;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_UNIT, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    unit = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return unit;
}



String DFRobot_RP2040_SCI::getValue(char* keys)
{
  String values = "";

  uint8_t errorCode;
  uint16_t length = 0;
  if (keys == NULL) return values;
  length = strlen(keys);

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_KEY_VALUE0;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  memcpy(sendpkt->args, keys, strlen(keys));

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_KEY_VALUE0, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    values = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return values;
}

String DFRobot_RP2040_SCI::getValue(eInterfaceList_t inf, char* keys)
{
  return getValue((uint8_t)inf, keys);
}

String DFRobot_RP2040_SCI::getValue(uint8_t inf, char* keys)
{
  String values = "";

  uint8_t errorCode;
  uint16_t length = 0;
  if (keys == NULL) return values;
  length = strlen(keys) + 1;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_KEY_VALUE1;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  memcpy(sendpkt->args + 1, keys, strlen(keys));

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_KEY_VALUE1, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    values = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return values;
}

String DFRobot_RP2040_SCI::getValue(eInterfaceList_t inf, char sku[7], char* keys)
{
  return getValue((uint8_t)inf, sku, keys);
}

String DFRobot_RP2040_SCI::getValue(uint8_t inf, char sku[7], char* keys)
{
  String values = "";

  uint8_t errorCode;
  uint16_t length = 0;
  if (keys == NULL) return values;
  length = strlen(keys) + 7 + 1;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_KEY_VALUE2;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  memcpy(sendpkt->args + 1, sku, 7);
  memcpy(sendpkt->args + 8, keys, strlen(keys));

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_KEY_VALUE2, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    values = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return values;
}

String DFRobot_RP2040_SCI::getUnit(char* keys)
{
  String values = "";

  uint8_t errorCode;
  uint16_t length = 0;
  if (keys == NULL) return values;
  length = strlen(keys);

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_KEY_UINT0;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  memcpy(sendpkt->args, keys, strlen(keys));

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_KEY_UINT0, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    values = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return values;
}
String DFRobot_RP2040_SCI::getUnit(eInterfaceList_t inf, char* keys)
{
  return getUnit((uint8_t)inf, keys);
}

String DFRobot_RP2040_SCI::getUnit(uint8_t inf, char* keys)
{
  String values = "";

  uint8_t errorCode;
  uint16_t length = 0;
  if (keys == NULL) return values;
  length = strlen(keys) + 1;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_KEY_UINT1;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  memcpy(sendpkt->args + 1, keys, strlen(keys));

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_KEY_UINT1, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    values = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return values;
}


String DFRobot_RP2040_SCI::getUnit(eInterfaceList_t inf, char sku[7], char* keys)
{
  return getUnit((uint8_t)inf, sku, keys);
}

String DFRobot_RP2040_SCI::getUnit(uint8_t inf, char sku[7], char* keys)
{
  String values = "";

  uint8_t errorCode;
  uint16_t length = 0;
  if (keys == NULL) return values;
  length = strlen(keys) + 7 + 1;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_GET_KEY_UINT2;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = inf;
  memcpy(sendpkt->args + 1, sku, 7);
  memcpy(sendpkt->args + 8, keys, strlen(keys));

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_GET_KEY_UINT2, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char sku[length + 1];
    memcpy(sku, rcvpkt->buf, length);
    sku[length] = '\0';
    values = String(sku);
  }
  if (rcvpkt) free(rcvpkt);
  return values;
}

String DFRobot_RP2040_SCI::getAnalogSensorSKU()
{
  String sku = "";

  uint8_t errorCode;
  uint16_t length = 0;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_SKU_A;
  sendpkt->argsNumL = 0;
  sendpkt->argsNumH = 0;

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SKU_A, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char buf[length + 1];
    memcpy(buf, rcvpkt->buf, length);
    buf[length] = '\0';
    sku = String(buf);
  }
  if (rcvpkt) free(rcvpkt);
  return sku;
}

String DFRobot_RP2040_SCI::getDigitalSensorSKU()
{
  String sku = "";

  uint8_t errorCode;
  uint16_t length = 0;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_SKU_D;
  sendpkt->argsNumL = 0;
  sendpkt->argsNumH = 0;

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SKU_D, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char buf[length + 1];
    memcpy(buf, rcvpkt->buf, length);
    buf[length] = '\0';
    sku = String(buf);
  }
  if (rcvpkt) free(rcvpkt);
  return sku;
}

String DFRobot_RP2040_SCI::getI2CSensorSKU()
{
  String sku = "";

  uint8_t errorCode;
  uint16_t length = 0;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_SKU_IIC;
  sendpkt->argsNumL = 0;
  sendpkt->argsNumH = 0;

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SKU_IIC, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char buf[length + 1];
    memcpy(buf, rcvpkt->buf, length);
    buf[length] = '\0';
    sku = String(buf);
  }
  if (rcvpkt) free(rcvpkt);
  return sku;
}

String DFRobot_RP2040_SCI::getUARTSensorSKU()
{
  String sku = "";

  uint8_t errorCode;
  uint16_t length = 0;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return "";
  sendpkt->cmd = CMD_SKU_UART;
  sendpkt->argsNumL = 0;
  sendpkt->argsNumH = 0;

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SKU_UART, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) {
    length = (rcvpkt->lenH << 8) | rcvpkt->lenL;
    char buf[length + 1];
    memcpy(buf, rcvpkt->buf, length);
    buf[length] = '\0';
    sku = String(buf);
  }
  if (rcvpkt) free(rcvpkt);
  return sku;
}

void DFRobot_RP2040_SCI::reset(uint8_t cmd)
{
  uint16_t length = 1;
  if (cmd > CMD_RESET) return;

  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + 1);
  if (sendpkt == NULL) return;
  sendpkt->cmd = CMD_RESET;
  sendpkt->argsNumL = 1;
  sendpkt->argsNumH = 0;
  sendpkt->args[0] = cmd;

  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);
  delay(1000);
}

uint32_t DFRobot_RP2040_SCI::getRefreshRate_ms(uint8_t rate)
{
  switch (rate) {
  case eRefreshRateMs:
    return 0;
  case eRefreshRate1s:
    return 1000;
  case eRefreshRate3s:
    return 3000;
  case eRefreshRate5s:
    return 5000;
  case eRefreshRate10s:
    return 10000;
  case eRefreshRate30s:
    return 30000;
  case eRefreshRate1min:
    return 60000;
  case eRefreshRate5min:
    return 300000;
  case eRefreshRate10min:
    return 600000;

  }
  return 0;
}

void* DFRobot_RP2040_SCI::recvPacket(uint8_t cmd, uint8_t* errorCode)
{
  if (cmd > CMD_END) {
    RP2040_SUAB_DBG("cmd is error!");
    if (errorCode) *errorCode = ERR_CODE_CMD_INVAILED; //There is no this command
    return NULL;
  }

  sCmdRecvPkt_t recvPkt;
  pCmdRecvPkt_t recvPktPtr = NULL;
  uint16_t length = 0;
  uint32_t t = millis();
  while (millis() - t < _timeout/*time_ms*/) {
    recvData(&recvPkt.status, 1);
    switch (recvPkt.status) {
    case STATUS_SUCCESS:
    case STATUS_FAILED:
    {
      recvData(&recvPkt.cmd, 1);
      if (recvPkt.cmd != cmd) {
        reset(cmd);
        if (errorCode) *errorCode = ERR_CODE_RES_PKT; //Response packet error
        RP2040_SUAB_DBG("Response pkt is error!");
        return NULL;
      }
      recvData(&recvPkt.lenL, 2);
      length = (recvPkt.lenH << 8) | recvPkt.lenL;
      recvPktPtr = (pCmdRecvPkt_t)malloc(sizeof(sCmdRecvPkt_t) + length);
      if (recvPktPtr == NULL) {
        reset(cmd);
        if (errorCode) *errorCode = ERR_CODE_M_NO_SPACE; //Insufficient memory of I2C controller(master)
        return NULL;
      }
      memcpy(recvPktPtr, &recvPkt, sizeof(sCmdRecvPkt_t));
      if (length) recvData(recvPktPtr->buf, length);
      if (errorCode) *errorCode = ERR_CODE_NONE;
      RP2040_SUAB_DBG(millis() - t);
      return recvPktPtr;
    }
    }
    delay(50);
    yield();
  }
  reset(cmd);
  if (errorCode) *errorCode = ERR_CODE_RES_TIMEOUT; //Receive packet timeout
  RP2040_SUAB_DBG("Time out!");
  RP2040_SUAB_DBG(millis() - t);
  return NULL;
}

uint8_t DFRobot_RP2040_SCI::conv2d(const char* p)
{
  uint8_t v = 0;
  if ('0' <= *p && *p <= '9')
    v = *p - '0';
  return 10 * v + *++p - '0';
}



uint16_t DFRobot_RP2040_SCI::date2days(uint16_t year, uint8_t month, uint8_t day)
{
  if (year >= 2000)
    year -= 2000;
  uint16_t days = day;
  for (uint8_t i = 1; i < month; ++i) {
    switch (i) {
    case 2:
      days += 28;
      break;
    case 4:
    case 6:
    case 9:
    case 11:
      days += 30;
      break;
    case 1:
    case 3:
    case 5:
    case 7:
    case 8:
    case 10:
    case 12:
      days += 31;
      break;
    }
  }
  if (month > 2 && year % 4 == 0)
    ++days; //Leap year
  //Leap years are divided into common and century leap years
  //The rule to decide leap year: In the Gregorian calendar, a common leap year is a year that is exactly divisible by 4 but not divisible by 100; a century leap year is a year that is exactly divisible by 400.
  //Add a leap year every 4 years, skip one every 100 years except every 400
  //The year 2000 is a leap year, 2004 is a leap year, 2100 is not a leap year, and 2104 is a leap year
  return days + 365 * year + (year + 3) / 4 - 1;
}

uint8_t DFRobot_RP2040_SCI::dayOfTheWeek(uint16_t year, uint8_t month, uint8_t day)
{
  uint16_t days = date2days(year, month, day);
  return (days + 6) % 7; // Jan 1, 2000 is a Saturday, i.e. returns 6
}

DFRobot_RP2040_SCI_IIC::DFRobot_RP2040_SCI_IIC(uint8_t addr, TwoWire* pWire)
  :DFRobot_RP2040_SCI(), _pWire(pWire), _addr(addr)
{

}

DFRobot_RP2040_SCI_IIC::~DFRobot_RP2040_SCI_IIC() {}

int DFRobot_RP2040_SCI_IIC::init(uint32_t freq)
{
  if (_pWire == NULL) return -1;
  _pWire->begin();
  _pWire->setClock(freq);
  _pWire->beginTransmission(_addr);
  if (_pWire->endTransmission() != 0) return -2;

  reset(CMD_RESET);
  return 0;
}

uint8_t DFRobot_RP2040_SCI_IIC::setI2CAddress(uint8_t addr)
{

  uint8_t errorCode;
  uint16_t length = 1;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t) + length);
  if (sendpkt == NULL) return ERR_CODE_M_NO_SPACE;
  sendpkt->cmd = CMD_SET_ADDR;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  sendpkt->args[0] = addr;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_SET_ADDR, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  if (errorCode == ERR_CODE_NONE) _addr = addr;
  return errorCode;
}
uint8_t DFRobot_RP2040_SCI_IIC::getI2CAddress()
{
  uint8_t errorCode;
  uint8_t addr = 0;
  uint16_t length = 0;
  pCmdSendPkt_t sendpkt = NULL;
  sendpkt = (pCmdSendPkt_t)malloc(sizeof(sCmdSendPkt_t));
  if (sendpkt == NULL) return 0;
  sendpkt->cmd = CMD_READ_ADDR;
  sendpkt->argsNumL = length & 0xFF;
  sendpkt->argsNumH = (length >> 8) & 0xFF;
  length += sizeof(sCmdSendPkt_t);
  sendPacket(sendpkt, length, true);
  free(sendpkt);

  pCmdRecvPkt_t rcvpkt = (pCmdRecvPkt_t)recvPacket(CMD_READ_ADDR, &errorCode);
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_FAILED)) errorCode = rcvpkt->buf[0];
  if ((rcvpkt != NULL) && (rcvpkt->status == STATUS_SUCCESS)) addr = rcvpkt->buf[0];
  if (rcvpkt) free(rcvpkt);
  return addr;
}

void DFRobot_RP2040_SCI_IIC::sendPacket(void* pkt, int length, bool stop)
{
  uint8_t* pBuf = (uint8_t*)pkt;
  int remain = length;
  if ((pkt == NULL) || (length == 0)) return;
  _pWire->beginTransmission(_addr);
  while (remain) {
    length = (remain > IIC_MAX_TRANSFER) ? IIC_MAX_TRANSFER : remain;
    _pWire->write(pBuf, length);
    remain -= length;
    pBuf += length;
#if defined(ESP32)
    if (remain) _pWire->endTransmission(true);
#else
    if (remain) _pWire->endTransmission(false);
#endif
  }
  _pWire->endTransmission(stop);
}

int DFRobot_RP2040_SCI_IIC::recvData(void* data, int len)
{
  uint8_t* pBuf = (uint8_t*)data;
  int remain = len;
  int total = 0;
  if (pBuf == NULL) {
    RP2040_SUAB_DBG("pBuf ERROR!! : null pointer");
    return 0;
  }

  while (remain) {
    len = remain > I2C_ACHE_MAX_LEN ? I2C_ACHE_MAX_LEN : remain;
    remain -= len;
    if (remain) {
#if defined(ESP32)
      _pWire->requestFrom(_addr, (uint8_t)len, (uint8_t)true);
#else
      _pWire->requestFrom(_addr, (uint8_t)len, (uint8_t)false);
#endif
    } else {   // hyy - else _pWire->requestFrom(_addr, len, true);
#if defined(NRF5) || defined(NRF52833)
      _pWire->requestFrom(_addr, (uint8_t)len, (uint8_t)false);
// #elif defined(ESP32)
//       _pWire->requestFrom((uint16_t)_addr, (uint8_t)len, true);
#else
      _pWire->requestFrom(_addr, (uint8_t)len, (uint8_t)true);
#endif
    }

    for (int i = 0; i < len; i++) {
      pBuf[i] = _pWire->read();
      RP2040_SUAB_DBG(pBuf[i], HEX);
      yield();
    }
    pBuf += len;
    total += len;
  }
  return total;
}

void DFRobot_RP2040_SCI_IIC::recvFlush()
{
  while (_pWire->available()) {
    _pWire->read();
    yield();
  }
}

void DFRobot_RP2040_SCI_IIC::sendFlush()
{
  _pWire->flush();
}
