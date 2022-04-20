//IMU unit testing
//Tested with E3K

///////////-----IMU
#include <Wire.h>
#include "SparkFun_BNO080_Arduino_Library.h"
BNO080 myIMU;
boolean isIMU = false;

///////////-----Button and LEDs
int led1 = 4, led2 = 15;
int but1 = 12, but2 = 13;

void setup() {
  Serial.begin(115200);
  Serial.println("The device started");

  ///////////-----Button and LEDs
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(but1, INPUT);
  pinMode(but2, INPUT);

  ///////////-----IMU
  
  Wire.begin();
  isIMU = myIMU.begin();
  if(isIMU == false){
    Serial.println("BNO080 not detected at default I2C address. IMU not connected or check your jumpers and the hookup guide.");
    Serial.println("Continuing....");
  }else{
    Wire.setClock(400000); //Increase I2C data rate to 400kHz
    myIMU.enableRotationVector(50); //Send data update every 50ms
    Serial.println(F("IMU enabled"));
    Serial.println(F("Rotation vector enabled"));
    Serial.println(F("Output in form i, j, k, real, accuracy"));
  }
}

void loop() {

  ///////////-----IMU
  if(isIMU == true){
    //Look for reports from the IMU
    if(myIMU.dataAvailable()){
        float roll = (myIMU.getRoll()) * 180.0 / PI; // Convert roll to degrees
        float pitch = (myIMU.getPitch()) * 180.0 / PI; // Convert pitch to degrees
        float yaw = (myIMU.getYaw()) * 180.0 / PI; // Convert yaw / heading to degrees

        Serial.print(roll, 1);
        Serial.print(F(","));
        Serial.print(pitch, 1);
        Serial.print(F(","));
        Serial.print(yaw, 1);
    
        Serial.println();

        digitalWrite(led1, pitch > 50);
        digitalWrite(led2, pitch < -50);
    }
  }
  
  delay(10);
}
