#include <Servo.h>

#define NUM_SERVOS 5

Servo servos[NUM_SERVOS];

// Pin connections for the servos (D2, D3, D4, D5, D6)
const int servoPins[NUM_SERVOS] = {2, 3, 4, 5, 6};

float servoAngles[NUM_SERVOS] = {45.0, 45.0, 90.0, 90.0, 90.0};

// Controls the speed of movement.
const float stepSize = 0.5;

void setup() {
  // Set the baud rate to 115200 for faster communication
  Serial.begin(115200);
  
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(int(servoAngles[i]));
  }
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    float speeds[NUM_SERVOS];
    int lastIndex = 0;
    
    for (int i = 0; i < NUM_SERVOS; i++) {
      int separatorIndex = data.indexOf(',', lastIndex);
      if (separatorIndex == -1) {
        separatorIndex = data.length();
      }
      String speedString = data.substring(lastIndex, separatorIndex);
      speeds[i] = speedString.toFloat();
      lastIndex = separatorIndex + 1;
    }
    
    // Update angles based on the speeds received
    for (int i = 0; i < NUM_SERVOS; i++) {
      servoAngles[i] += speeds[i] * stepSize;
    }
    
    // Constrain the angles based on the motor's operating range
    servoAngles[0] = constrain(servoAngles[0], 0.0, 90.0);
    servoAngles[1] = constrain(servoAngles[1], 0.0, 90.0);
    servoAngles[2] = constrain(servoAngles[2], 0.0, 180.0);
    servoAngles[3] = constrain(servoAngles[3], 0.0, 180.0);
    servoAngles[4] = constrain(servoAngles[4], 0.0, 180.0);

    // Write the new angles to the servos
    for (int i = 0; i < NUM_SERVOS; i++) {
      servos[i].write(int(servoAngles[i]));
    }
  }
}