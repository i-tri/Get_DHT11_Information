#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <DHT.h>
#include <WiFiUdp.h>
#include <NTPClient.h>

// WiFi settings
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// DHT settings
#define DHTPIN D2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// NTP settings
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 12 * 3600); // New Zealand (UTC+12)

// Web server
ESP8266WebServer server(80);

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Print the IP address
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize DHT sensor
  dht.begin();

  // Initialize NTP Client
  timeClient.begin();
  
  // Start server
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
  
  // Refresh every 5 seconds
  static unsigned long lastRefreshTime = 0;
  if (millis() - lastRefreshTime > 5000) {
    lastRefreshTime = millis();
    
    // Read sensor data
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    timeClient.update();
    String formattedTime = timeClient.getFormattedTime();

    // Print data to serial monitor
    String data = "Temperature: " + String(t) + " *C, Humidity: " + String(h) + " %, Time: " + formattedTime;
    Serial.println(data);
  }
}

void handleRoot() {
  // Read sensor data
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  timeClient.update();
  String formattedTime = timeClient.getFormattedTime();

  // Format data for response
  String data = "Temperature: " + String(t) + " *C, Humidity: " + String(h) + " %, Time: " + formattedTime;

  // Send data to web client
  server.send(200, "text/plain", data);
}
