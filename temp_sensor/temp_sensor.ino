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

// config values
#define CYCLE_WIDTH 5
#define CYCLE_LENGTH 80
#define BASE_TEMPERATURE 30
//#define DELAY 0
float thermo_sensor_values[3];
int unsigned steps = 0;
String output_string_cycle = "";

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    thermo_sensors[i].begin(MAX31865_4WIRE);  // set to 2WIRE or 4WIRE as necessary
  }
  pinMode(2, OUTPUT);
  digitalWrite (2, LOW);
}


void loop() {
  for (int i = 0; i < 3; i++) { 
    thermo_sensor_values[i] = thermo_sensors[i].temperature(RNOMINAL, RREF);
  }
  output_string_cycle += createCsvLine(thermo_sensor_values);
  if (steps%CYCLE_LENGTH == 0) {
    Serial.print(output_string_cycle);
    output_string_cycle = "";
  }
    
  // heating reversed: HIGH cools, LOW heats
  // heat if thermo_sensor_values[0] is smaller than sin
  float sinValue = CYCLE_WIDTH*sin((steps/CYCLE_LENGTH)*2*PI)+BASE_TEMPERATURE;
  if (thermo_sensor_values[0] > sinValue) {
    digitalWrite(2, HIGH);
  }
  if (thermo_sensor_values[0] < sinValue) {
    digitalWrite(2, LOW);
  }
  steps++;
  //delay(DELAY);
}

String createCsvLine(float threeValues[]) {
  String measureString = "";
  for (int j = 0; j < 3; j++) {
    measureString += String(threeValues[j]) + ";";
  }
  return measureString + String(millis()) + "\r\n";
}