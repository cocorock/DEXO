#include <WiFi.h>
#include <WiFiUdp.h>

// WiFi network credentials
const char* ssid = "2G_Panic_at_the_Cisco";
const char* password = "Socorro!";

// UDP port number
const uint16_t udp_port = 3333;

// Create a UDP object
WiFiUDP udp;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  // Print the local IP address
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());

  // Begin UDP communication
  if (!udp.begin(udp_port)) {
    Serial.println("Failed to begin UDP communication");
    while (1) {
      delay(1000);
    }
  }
  Serial.println("UDP server started");
}

void loop() {
  // Check if there's data available to read
  int packet_size = udp.parsePacket();
  if (packet_size) {
    // Read the data into a buffer
    char buffer[packet_size];
    udp.read(buffer, packet_size);

    // Print the received data to the serial monitor
    Serial.write(buffer, packet_size);

    // Send the data back to the client
    // udp.beginPacket("192.168.0.180", udp_port);
    // udp.write(buffer, packet_size);
    // udp.endPacket();
  }
}
