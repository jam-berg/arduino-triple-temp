/*************************************************** 
  This is a library for the Adafruit PT100/P1000 RTD Sensor w/MAX31865

  Designed specifically to work with the Adafruit RTD Sensor
  ----> https://www.adafruit.com/products/3328

  This sensor uses SPI to communicate, 4 pins are required to  
  interface
  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Adafruit_MAX31865.h>

Adafruit_MAX31865 thermo_sensors[3] = {
    Adafruit_MAX31865(10, 11, 12, 13),
    Adafruit_MAX31865(7, 8, 9, 13),
    Adafruit_MAX31865(4, 5, 6, 13)
  };
// Use software SPI: CS, DI, DO, CLK
// use hardware SPI, just pass in the CS pin
//Adafruit_MAX31865 thermo1 = Adafruit_MAX31865(10);

// The value of the Rref resistor. Use 430.0 for PT100 and 4300.0 for PT1000
#define RREF      430.0
// The 'nominal' 0-degrees-C resistance of the sensor
// 100.0 for PT100, 1000.0 for PT1000
#define RNOMINAL  100.0
#define PI 3.1415926535897932384626433832795

// config values
#define CYCLE_WIDTH 5
#define CYCLE_LENGTH 200
#define BASE_TEMPERATURE 30
int unsigned steps = 0;

void setup() {
  Serial.begin(9600);
  //Serial.println("Adafruit MAX31865 PT100 Sensor Test!");

  for (int i = 0; i < 3; i++) {
    thermo_sensors[i].begin(MAX31865_4WIRE);  // set to 2WIRE or 4WIRE as necessary
  }
  pinMode(2, OUTPUT);
  digitalWrite (2, LOW);
}


void loop() {
  delay(CYCLE_LENGTH);
  float thermo_sensor_values[3];
  for (int i = 0; i < 3; i++) { 
    uint16_t rtd = thermo_sensors[i].readRTD();
    //Serial.print("Sensor Number: "); Serial.println(i);

    //Serial.print("RTD value: "); Serial.println(rtd);
    float ratio = rtd;
    ratio /= 32768;
    //Serial.print("Ratio = "); Serial.println(ratio,8);
    //Serial.print("Resistance = "); Serial.println(RREF*ratio,8);
    //Serial.print("Temperature = "); Serial.println(thermo_sensors[i].temperature(RNOMINAL, RREF));
    thermo_sensor_values[i] = thermo_sensors[i].temperature(RNOMINAL, RREF);
    
    // Check and print any faults
    uint8_t fault = thermo_sensors[i].readFault();
    if (fault) {
      Serial.print("Fault 0x"); Serial.println(fault, HEX);
      if (fault & MAX31865_FAULT_HIGHTHRESH) {
        Serial.println("RTD High Threshold"); 
      }
      if (fault & MAX31865_FAULT_LOWTHRESH) {
        Serial.println("RTD Low Threshold"); 
      }
      if (fault & MAX31865_FAULT_REFINLOW) {
        Serial.println("REFIN- > 0.85 x Bias"); 
      }
      if (fault & MAX31865_FAULT_REFINHIGH) {
        Serial.println("REFIN- < 0.85 x Bias - FORCE- open"); 
      }
      if (fault & MAX31865_FAULT_RTDINLOW) {
        Serial.println("RTDIN- < 0.85 x Bias - FORCE- open"); 
      }
      if (fault & MAX31865_FAULT_OVUV) {
        Serial.println("Under/Over voltage"); 
      }
      thermo_sensors[i].clearFault();
    }
  }
  createCsvLine(thermo_sensor_values);

  // heating reversed with relais
  // if (thermo_sensor_values[0] > 35) {
  //   digitalWrite(2, HIGH);
  // }
  // if (thermo_sensor_values[0] < 25) {
  //   digitalWrite(2, LOW);

  // heat if thermo_sensor_values[0] is smaller than sin
  float sinValue = CYCLE_WIDTH*sin((steps/CYCLE_LENGTH)*2*PI)+BASE_TEMPERATURE;
  if (thermo_sensor_values[0] > sinValue) {
    digitalWrite(2, HIGH);
  }
  if (thermo_sensor_values[0] < sinValue) {
    digitalWrite(2, LOW);
  
  }
  steps++;
}

void createCsvLine(float threeValues[]) {
  String measureString = "";
  int k = 0;
  for (int j = 0; j < 3; j++) {
    measureString += threeValues[j];
    if (k++ < 2) {
       measureString += ";";
    }
  }
  Serial.println(measureString);
}
