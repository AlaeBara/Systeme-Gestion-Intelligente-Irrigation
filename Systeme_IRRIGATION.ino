#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN     D4       // capteur DHT11
#define DHTTYPE    DHT11

DHT_Unified dht(DHTPIN, DHTTYPE);

// Capteur de sol v1.2 sur A0
#define SOIL_PIN   A0       

// Relais pour pompe sur D6 (par exemple)
#define RELAY_PIN  D6       

// Seuil d’humidité en pourcentage
const int MOISTURE_THRESHOLD = 45;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Initialisation DHT
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("DHT11 + Soil v1.2 + Relais pompe"));
  Serial.print  (F("Capteur: ")); Serial.println(sensor.name);
  
  // Initialisation du relais
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // pompe OFF au démarrage
}

void loop() {
  // ——— Lecture DHT ———
  delay(2000);
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Erreur lecture temperature DHT!"));
  } else {
    Serial.print(F("Temp: ")); Serial.print(event.temperature); Serial.println(F(" °C"));
  }
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Erreur lecture humidite DHT!"));
  } else {
    Serial.print(F("Humidite: ")); Serial.print(event.relative_humidity); Serial.println(F(" %"));
  }

  // ——— Lecture capteur de sol ———
  int raw = analogRead(SOIL_PIN);              // 0 (imprégné) → 1023 (sec)
  int moisturePercent = map(raw, 1023, 0, 0, 100);
  moisturePercent = constrain(moisturePercent, 0, 100);
  Serial.print(F("Humidité sol: "));
  Serial.print(moisturePercent);
  Serial.print(F(" % (raw="));
  Serial.print(raw);
  Serial.println(F(")"));

  // ——— Condition pompe ———
  if (moisturePercent > MOISTURE_THRESHOLD) {
    digitalWrite(RELAY_PIN, HIGH);  // active le relais → pompe ON
    Serial.println(F(">> Pompe ON"));
  } else {

    
    digitalWrite(RELAY_PIN, LOW);   // relais inactif → pompe OFF
    Serial.println(F(">> Pompe OFF"));
  }

  Serial.println();
}
