#include <Arduino.h>
#include <math.h>

// Constants
const float L1 = 400;
const float L2 = 450;

// Function prototypes
void IK(float x, float y, float &alpha1, float &alpha2);
void set_Angle(uint8_t ID, int32_t angle);
String readSerialCommand();

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize the servo motors or actuators
  // Add your initialization code here
}

void loop() {
  // Define path points
  float path[][2] = {
    {750, 0},
    {750, 100},
    {700, 50},
    {700, -50},
    {750, -100}
  };

  int numPoints = sizeof(path) / sizeof(path[0]);

  // Wait for the "GO!" command
  while (readSerialCommand() != "GO!") {
    delay(100);
  }

  // Follow the path for both arms
  for (int i = 0; i < numPoints; i++) {
    String command = readSerialCommand();
    if (command == "STP") {
      break;
    } else if (command == "BNG") {
      // Set angles to the first position of the path
      float alpha1, alpha2;
      IK(path[0][0], path[0][1], alpha1, alpha2);
      set_Angle(1, alpha1);
      set_Angle(2, alpha2);
      set_Angle(3, alpha1);
      set_Angle(4, alpha2);

      // Wait for the "GO!" command to resume
      while (readSerialCommand() != "GO!") {
        delay(100);
      }
    }

    float x = path[i][0];
    float y = path[i][1];

    // Calculate joint angles for both arms
    float alpha1, alpha2;
    IK(x, y, alpha1, alpha2);

    // Set joint angles for both arms
    // set_Angle(1, alpha1);
    // set_Angle(2, alpha2);
    // set_Angle(3, alpha1);
    // set_Angle(4, alpha2);

    delay(500);
  }
}

void IK(float x, float y, float &alpha1, float &alpha2) {
  float c2 = (pow(x, 2) + pow(y, 2) - pow(L1, 2) - pow(L2, 2)) / (2 * L1 * L2);
  alpha2 = atan2(sqrt(1 - pow(c2, 2)), c2);

  float c1 = ((x * (L1 + L2 * cos(alpha2))) + (y * L2 * sin(alpha2))) / (pow(x, 2) + pow(y, 2));
  float s1 = ((y * (L1 + L2 * cos(alpha2))) - (x * L2 * sin(alpha2))) / (pow(x, 2) + pow(y, 2));
  alpha1 = atan2(s1, c1);

  // Convert radians to degrees
  alpha1 = alpha1 * (180.0 / 3.14159265359);
  alpha2 = alpha2 * (180.0 /
