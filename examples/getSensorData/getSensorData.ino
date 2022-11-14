/*!
 * @file getSensorData.ino
 * @brief 获取传感器数据
 *
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Arya](xue.peng@dfrobot.com)
 * @version  V1.0
 * @date  2021-08-11
 * @url https://github.com/DFRobot/DFRobot_RP2040_SCI
 */
#include "DFRobot_RP2040_SCI.h"

DFRobot_RP2040_SCI_IIC sci(/*addr=*/RP2040_SCI_ADDR_0X21, &Wire);

void setup() {
  Serial.begin(115200);
  while(!Serial){                                                     //Waiting for USB Serial COM port to open.
  }
  
  Serial.print("Initialization SCI Acquisition Module...");
  while(sci.begin() != 0){
      Serial.println("failed. Please check whether the hardware connection is wrong.");
      delay(1000);
      Serial.print("Initialization SCI Acquisition Module...");
  }
  Serial.println("done.");

  sci.setRefreshRate(sci.eRefreshRate1s);
  Serial.print("Refresh rate: ");Serial.println(sci.getRefreshRate());Serial.print("ms");
  
  DFRobot_RP2040_SCI_IIC::ePort1IFMode_t mode0;
  DFRobot_RP2040_SCI_IIC::ePort23Mode_t mode1, mode2;
  String skuIF0, skuIF1, skuIF2;
  skuIF0 = sci.getPort1(&mode0);
  skuIF1 = sci.getPort2(&mode1);
  skuIF2 = sci.getPort3(&mode2);

  Serial.println("Configuration: ");
  Serial.print("IF0: "); Serial.print("TYPE-" + sci.getSensorModeDescribe(mode0) + ' ');Serial.println(" SKU-" + skuIF0);
  Serial.print("IF1: "); Serial.print("TYPE-" + sci.getSensorModeDescribe(mode1) + ' ');Serial.println(" SKU-" + skuIF1);
  Serial.print("IF2: "); Serial.print("TYPE-" + sci.getSensorModeDescribe(mode2) + ' ');Serial.println(" SKU-" + skuIF2);
  Serial.println();
}

void loop() {
  /**
   * @fn getSKU/getInformation
   * 
   * @param inf    接口选择
   * @n     ePort1                                           选中Port1接口
   * @n     ePort2                                           选中Port2接口
   * @n     ePort3                                           选中Port3接口
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             选中Port1, Port2和Port3接口
   */
  String sku   = sci.getSKU(sci.eALL);
  String ifAll = sci.getInformation(sci.eALL, true);
  Serial.println("SKU: "+ sku);
  Serial.println("IF : "+ ifAll);
  Serial.println();
  delay(1000);
}
