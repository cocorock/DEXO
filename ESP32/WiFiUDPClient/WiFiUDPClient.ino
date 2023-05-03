/*
 *  This sketch sends random data over UDP on a ESP32 device
 *
 */
#include <WiFi.h>
#include <WiFiUdp.h>
// Pin definitions
const byte BUTTON_PIN = 12;
const byte OUTPUT_PIN = 5;

// Flag to indicate button press
volatile bool button_pressed = false;

// Interrupt service routine for button press
void button_isr() {
  button_pressed = true;
}
// WiFi network name and password:
const char * networkName = "2G_Panic_at_the_Cisco";
const char * networkPswd = "Socorro!";

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.0.166";
const int udpPort = 3333;

//Are we currently connected?
boolean connected = false;

//The udp library class
WiFiUDP udp;

void setup(){
  // Initilize hardware serial:
  Serial.begin(115200);
  // Configure pin modes
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(OUTPUT_PIN, OUTPUT);
  // Attach interrupt to button pin
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), button_isr, FALLING);
  // Set initial output pin state
  digitalWrite(OUTPUT_PIN, LOW);
  //Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);
}

void loop(){
  //only send data when connected
  if(connected){
    //Send a packet
    udp.beginPacket(udpAddress,udpPort);
    udp.printf("%lu, %d\n", millis()/1000, button_pressed);
    udp.endPacket();
  }
  if (button_pressed) {
    // Toggle output pin state
    digitalWrite(OUTPUT_PIN, !digitalRead(OUTPUT_PIN));
    // Clear button press flag
    button_pressed = false;
  }
  //Wait for 1 second
  delay(1000);
}

void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case ARDUINO_EVENT_WIFI_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          connected = true;
          break;
      case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
      default: break;
    }
}
