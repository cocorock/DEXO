// Echo Serial Data

void setup() {
  // Initialize the serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Check if there's data available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming data
    char incomingData = Serial.read();

    // Echo the data back through the TX pin
    //Serial.write(">");
    Serial.write(incomingData);
  }
}