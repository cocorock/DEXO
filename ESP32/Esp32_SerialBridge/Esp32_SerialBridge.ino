#include <HardwareSerial.h>

HardwareSerial secondSerial(1); // Use second hardware serial (UART1)

void setup() {
  // Start communication with computer through USB (Serial Monitor)
  Serial.begin(115200);
  // Start communication with second hardware serial (UART1)
  secondSerial.begin(115200, SERIAL_8N1, 16, 17); // RX=16, TX=17
}

void loop() {
  // Read from USB serial (Serial Monitor) and write to second hardware serial (UART1)
  if (Serial.available()) {
    int receivedByte = Serial.read();
    secondSerial.write(receivedByte);
  }

  // Read from second hardware serial (UART1) and write to USB serial (Serial Monitor)
  if (secondSerial.available()) {
    int receivedByte = secondSerial.read();
    Serial.write(receivedByte);
  }
}
