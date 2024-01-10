// DHT (Temperature / Humidity) & Brighness Sensor data retrieval

// Depends on the following Arduino libraries:
// - Adafruit Unified Sensor Library: https://github.com/adafruit/Adafruit_Sensor
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <math.h>

#define DHTPIN 12
#define LIGHTSENSOR_PIN A2
#define DHTTYPE DHT11

DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;

// This function is used to read the resistance value of the light sensor.
float getRes(){
    int sensorValue = analogRead(LIGHTSENSOR_PIN);
    float Rsensor;
    Rsensor = (float)(1023 - sensorValue) * 10 / sensorValue;
    return Rsensor;
}
// This function is used to send the sensor data to the Python MQTT application.
void sendSensorData(float temperature, int humidity, int brightness) {
    Serial.print("temperature:");
    Serial.print(temperature);
    Serial.print(",humidity:");
    Serial.print(humidity);
    Serial.print(",brightness:");
    Serial.println(brightness);
}

// This function is used to initialize the sensors.
void setup()
{
    Serial.begin(9600);
    dht.begin();
    pinMode(LIGHTSENSOR_PIN, INPUT);
    sensor_t sensor;
    dht.temperature().getSensor(&sensor);
    delayMS = sensor.min_delay / 1000;
}

void loop()
{
    delay(delayMS);
    sensors_event_t temp_event, humidity_event;

    // Read temperature sensor data
    dht.temperature().getEvent(&temp_event);
    // Read humidity sensor data
    dht.humidity().getEvent(&humidity_event);
    // Read Light sensor data
    float Rsensor = getRes();

    // Calculate luminance
    float lux;
    lux = 325 * pow(Rsensor, -1.4);

    if (isnan(temp_event.temperature) || isnan(humidity_event.relative_humidity) || isnan(lux))
    {
        Serial.println("Failed to read sensor values!");
    }
    else
    {
        sendSensorData(temp_event.temperature, int(humidity_event.relative_humidity), int(lux));
    }
    delay(1000);
}
