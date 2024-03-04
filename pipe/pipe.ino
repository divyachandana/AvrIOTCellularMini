#include <mcp9808.h>
#include <Arduino.h>
#include <http_client.h>
#include <ArduinoJson.h>
#include <led_ctrl.h>
#include <log.h>
#include <lte.h>


const char* serverPath = "/log";
const char* serverDomain = "<Your Server address>";
const int serverPort = 5000;

const byte flowSensorPin = 13;
const float flowCalibrationFactor = 0.2;
volatile byte flowPulseCount = 0;
float flowRate = 0.0;
unsigned long oldTime = 0;

void flowPulseCounter() {
  flowPulseCount++;
}


void sendDataToServer(float temperature, float flowRate) {

    if (!HttpClient.configure(serverDomain, serverPort, false)) {
        Log.error("Failed to configure HTTP client");
        return;
    }

    JsonDocument doc;
    doc["Temperature"] = temperature;
    doc["Water Flow"] = flowRate;
    
    String json;
    serializeJson(doc, json);
    

    HttpResponse response = HttpClient.post(serverPath, json.c_str());

    if (response.status_code > 0) {
        Log.infof("POST - status code: %u, data size: %u\r\n", response.status_code, response.data_size);
    } else {
        Log.error("Error on sending POST");
    }
}

void setup() {
    Serial.begin(115200);
    Log.begin(115200);
    LedCtrl.begin();
    LedCtrl.startupCycle();

    const int8_t error = Mcp9808.begin(); 
    if (error) {
        Serial.println("Error: could not start MCP9808 library");
    }


    if (!Lte.begin()) {
        Log.error("Failed to connect to the operator");
        return;
    }

    pinMode(flowSensorPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(flowSensorPin), flowPulseCounter, FALLING);
  
    Log.info("Flow sensor measurement started");

    Log.infof("Connected to operator: %s\r\n", Lte.getOperator().c_str());

}

float readFlowRate() {
  float flowRateLPM = 0.0;
  if ((millis() - oldTime) > 900) {
    detachInterrupt(digitalPinToInterrupt(flowSensorPin));
    
    flowRateLPM = (flowPulseCount / flowCalibrationFactor) / ((millis() - oldTime) / 60000.0);
    
    oldTime = millis();
    flowPulseCount = 0;
    
    attachInterrupt(digitalPinToInterrupt(flowSensorPin), flowPulseCounter, FALLING);
  }
  return flowRateLPM;
}


void loop() {
  const float temperature = Mcp9808.readTempC();
  flowRate = readFlowRate();
  Serial.printf("Temperature (*C): %f\r\n", (double)temperature);

  sendDataToServer(temperature, flowRate);
  delay(600000);

}
