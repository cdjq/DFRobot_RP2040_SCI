/*!
 * @file getConfigAndData.ino
 * @brief Get config of SCI Acquisition Module and the uploaded sensor data on each port
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

  sci.setPort1("Analog");
  //sci.setPort1("NULL");
  //sci.setPort1("SEN0161");
  sci.setPort2("NULL");
  sci.setPort3("NULL");
  
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
   * @param inf    Port select
   * @n     ePort1                                           Select Port1
   * @n     ePort2                                           Select Port2
   * @n     ePort3                                           Select Port3
   * @n     eALL  or  (ePort1 | ePort2 | ePort3)             Select Port1, Port2 and Port3
   */
  String sku0  = "SKU-"  + sci.getSKU(sci.ePort1);
  String sku1  = "SKU-"  + sci.getSKU(sci.ePort2);
  String sku2  = "SKU-"  + sci.getSKU(sci.ePort3);
  String if0   = "DATA-" + sci.getInformation(sci.ePort1);
  String if1   = "DATA-" + sci.getInformation(sci.ePort2);
  String if2   = "DATA-" + sci.getInformation(sci.ePort3);
  Serial.println("IF0: "+ sku0 + " " + if0);
  Serial.println("IF1: "+ sku1 + " " + if1);
  Serial.println("IF2: "+ sku2 + " " + if2);
  Serial.println();
  delay(1000);
}


