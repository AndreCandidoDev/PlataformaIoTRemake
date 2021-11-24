#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
//#include "DHT.h"

//#define DHTTYPE DHT11
//#define dht_dpin D3
//DHT dht11(dht_dpin, DHTTYPE);

//#define DHT22TYPE DHT22
//#define dht22_dpin D2
//DHT dht22(dht22_dpin, DHT22TYPE);

//int Pin_a0 = A0;
//int Nivel_sensor_CO2 = 400;

//area de dados para o termistor
const double VCC = 3.3;             // NodeMCU on board 3.3v vcc
const double R2 = 10000;            // 10k ohm series resistor
const double adc_resolution = 1023; // 10-bit adc
const double A = 0.001129148;   // thermistor equation parameters
const double B = 0.000234125;
const double C = 0.0000000876741; 

// pinos digitais
String gpio5_state = "Off";
String gpio2_state = "Off";
String gpio12_state = "Off";
String gpio0_state = "Off";
String gpio3_state = "Off";
String gpio4_state = "Off";
String gpio10_state = "Off";
String gpio13_state = "Off";
String gpio14_state = "Off";
String gpio15_state = "Off";
String gpio16_state = "Off";
int gpio5_pin = 5;
int gpio2_pin = 2;
int gpio12_pin = 12;
int gpio0_pin = 0;
int gpio3_pin = 3;
int gpio4_pin = 4;
int gpio10_pin = 10;
int gpio13_pin = 13;
int gpio14_pin = 14;
int gpio15_pin = 15;
int gpio16_pin = 16;

//usar sua rede wifi ----- sera passado na plataforma, o gerador de código irá mudar automaticamente
const char* ssid = "WiFi name";
const char* password = "WiFi password";

ESP8266WebServer server(8080); 

void setup() {
//  dht11.begin();
//  dht22.begin();
  Serial.begin(115200); 
  delay(10);
  pinMode(gpio5_pin, OUTPUT);
  digitalWrite(gpio5_pin, LOW);
  pinMode(gpio2_pin, OUTPUT);
  digitalWrite(gpio2_pin, LOW);
  pinMode(gpio12_pin, OUTPUT);
  digitalWrite(gpio12_pin, LOW);
  pinMode(gpio0_pin, OUTPUT);
  digitalWrite(gpio0_pin, LOW);
  pinMode(gpio3_pin, OUTPUT);
  digitalWrite(gpio3_pin, LOW);
  pinMode(gpio4_pin, OUTPUT);
  digitalWrite(gpio4_pin, LOW);
  pinMode(gpio10_pin, OUTPUT);
  digitalWrite(gpio10_pin, LOW);
  pinMode(gpio13_pin, OUTPUT);
  digitalWrite(gpio13_pin, LOW);
  pinMode(gpio14_pin, OUTPUT);
  digitalWrite(gpio14_pin, LOW);
  pinMode(gpio15_pin, OUTPUT);
  digitalWrite(gpio15_pin, LOW);
  pinMode(gpio16_pin, OUTPUT);
  digitalWrite(gpio16_pin, LOW);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  IPAddress ip = WiFi.localIP();
  IPAddress gateway = WiFi.gatewayIP();
  IPAddress subnet = WiFi.subnetMask();

  Serial.println("Parametros de rede");
  Serial.println("IP:");
  Serial.println(ip);
  Serial.println("Gateway:");
  Serial.println(gateway);
  Serial.println("subnet:");
  Serial.println(subnet);
  
  Serial.print("Configurando IP fixo para : ");
  Serial.println(ip);
  Serial.println("");
  Serial.println("Connectado");
  Serial.print ("IP: ");
  Serial.println(WiFi.localIP());
// obs: para requisições HTTP utilizar apenas lowercase
  server.on("/analogic/termistor", HTTP_GET, getTemperature);
//  obs: para evitar problemas no python retirei o /ldr/
  server.on("/analogic/luminosity", HTTP_GET, getLuminosity);
//  server.on("/analogic/dht11/umidity", HTTP_GET, dht11Umidity);
//  server.on("/analogic/dht22/umidity", HTTP_GET, dht22Umidity);
//  server.on("/analogic/dht11/temperature", HTTP_GET, dht11Temperature);
//  server.on("/analogic/dht22/temperature", HTTP_GET, dht22Temperature);
//  server.on("/analogic/mq135/co2concentration", HTTP_GET, CO2Concentration);
  server.on("/gpio5on", HTTP_GET, getgpio5on);
  server.on("/gpio5off", HTTP_GET, getgpio5off);
  server.on("/gpio2on", HTTP_GET, getgpio2on);
  server.on("/gpio2off", HTTP_GET, getgpio2off);
  server.on("/gpio12on", HTTP_GET, getgpio12on);
  server.on("/gpio12off", HTTP_GET, getgpio12off);
  server.on("/gpio0on", HTTP_GET, getgpio0on);
  server.on("/gpio0off", HTTP_GET, getgpio0off);
  server.on("/gpio3on", HTTP_GET, getgpio3on);
  server.on("/gpio3off", HTTP_GET, getgpio3off);
  server.on("/gpio4on", HTTP_GET, getgpio4on);
  server.on("/gpio4off", HTTP_GET, getgpio4off);
  server.on("/gpio10on", HTTP_GET, getgpio10on);
  server.on("/gpio10off", HTTP_GET, getgpio10off);
  server.on("/gpio13on", HTTP_GET, getgpio13on);
  server.on("/gpio13off", HTTP_GET, getgpio13off);
  server.on("/gpio14on", HTTP_GET, getgpio14on);
  server.on("/gpio14off", HTTP_GET, getgpio14off);
  server.on("/gpio15on", HTTP_GET, getgpio15on);
  server.on("/gpio15off", HTTP_GET, getgpio15off);
  server.on("/gpio16on", HTTP_GET, getgpio16on);
  server.on("/gpio16off", HTTP_GET, getgpio16off);
  server.on("/getstates", HTTP_GET, getstates);
  server.on("/test", HTTP_GET, test);
  server.on("/board", HTTP_GET, board);
  server.onNotFound(onNotFound);
  server.begin();
  Serial.println("Servidor HTTP iniciado");

}

void loop() {
  server.handleClient();
}

void onNotFound(){
  server.send(404, "text/plain", "Not Found" );
}

void test(){
  String json = "nodemcu is conected";
  server.send (200, "application/json", json);  
}

void board(){
  String json = "esp8266";
  server.send(200, "application/json", json);
}

void getTemperature(){
  double Vout, Rth, temperature, adc_value; 
  adc_value = analogRead(A0);
  Serial.println(adc_value);
  Vout = (adc_value * VCC) / adc_resolution;
  Rth = (VCC * R2 / Vout) - R2;
  temperature = (1 / (A + (B * log(Rth)) + (C * pow((log(Rth)),3))));   // Temperature in kelvin
  temperature = temperature - 273.15;
  Serial.println(temperature);
  String json = "{\"temperature\":"+String(temperature)+"}";
  server.send (200, "application/json", json);
}

void getLuminosity(){
    int sensorValue = analogRead(A0);   // Ler o pino Analógico A0 onde está o LDR
    float voltage = sensorValue * (3.3 / 1024.0);   // Converter a leitura analógica (que vai de 0 - 1023) para uma voltagem (0 - 3.3V), quanto de acordo com a intensidade de luz no LDR a voltagem diminui.
    Serial.println(voltage);   // Mostrar valor da voltagem no monitor serial
    String json = "{\"voltage\":"+String(voltage)+"}";
    server.send (200, "text/plain", json);
    delay(2000);
}


//void dht11Umidity () {
//    float h = dht11.readHumidity();
//
//    Serial.print("Umidade = ");
//    Serial.print(h);
//    Serial.print("%  ");
//  
//    String json = "{\"Umidade\":" +String(h)+ "}";
//    server.send (200, "text/plain", json);
//    delay(1000);
//}

//void dht22Umidity () {
//    float h = dht22.readHumidity();
//
//    Serial.print("Umidade = ");
//    Serial.print(h);
//    Serial.print("%  ");
//  
//    String json = "{\"Umidade\":" +String(h)+ "}";
//    server.send (200, "text/plain", json);
//    delay(1000);
//}

//void dht11Temperature () {
//    float t = dht11.readTemperature();
//  
//    Serial.print("Temperatura = ");
//    Serial.print(t);
//    Serial.print("°C,  ");
//  
//    String json = "{\"Temperatura\":" +String(t)+ "}";
//    server.send (200, "text/plain", json);
//    delay(1000);
//}

//void dht22Temperature () {
//    float t = dht22.readTemperature();
//  
//    Serial.print("Temperatura = ");
//    Serial.print(t);
//    Serial.print("°C,  ");
//  
//    String json = "{\"Temperatura\":" +String(t)+ "}";
//    server.send (200, "text/plain", json);
//    delay(1000);
//}


//void CO2Concentration () {
//  int Valor_analogico = analogRead(Pin_a0);
//
//  Serial.print("Concentração de CO2 =  ");
//  Serial.print(Valor_analogico);
//  Serial.println("ppm  ");
//  String json = "{\"CO2\":" +String(Valor_analogico)+ "}";
//  server.send (200, "text/plain", json);
//  delay(1000);
//}


void getstates(){
    String json = "{estado_gpio0:"+String(gpio0_state)+" estado gpio2:" + String(gpio2_state)+
    " estado gpio3:" + String(gpio3_state) + " estado gpio4:" + String(gpio4_state) + " estado; gpio5:" + String(gpio5_state)+
    " estado gpio10:" + String(gpio10_state)+ " estado gpio12:" + String(gpio12_state)+
    " estado gpio13:" + String(gpio13_state) + " estado gpio14:" + String(gpio14_state) + " estado gpio15:" + String(gpio15_state)+
    " estado gpio16:" + String(gpio16_state) + "}";
    server.send(200, "application/json", json);
  }

void getgpio5on(){
   gpio5_state = "On";
   digitalWrite(gpio5_pin, HIGH);
   String json =  "{\"estado gpio5:\":"+String(gpio5_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio5off(){
   gpio5_state = "Off";
   digitalWrite(gpio5_pin, LOW);
   String json =  "{\"estado gpio5:\":"+String(gpio5_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio2on(){
   gpio2_state = "On";
   digitalWrite(gpio2_pin, HIGH);
   String json =  "{\"estado gpio2:\":"+String(gpio2_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio2off(){
   gpio2_state = "Off";
   digitalWrite(gpio2_pin, LOW);
   String json =  "{\"estado gpio2:\":"+String(gpio2_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio12on(){
   gpio12_state = "On";
   digitalWrite(gpio12_pin, HIGH);
   String json =  "{\"estado gpio12:\":"+String(gpio12_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio12off(){
   gpio12_state = "Off";
   digitalWrite(gpio12_pin, LOW);
   String json =  "{\"estado gpio12:\":"+String(gpio12_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio0on(){
   gpio0_state = "On";
   digitalWrite(gpio0_pin, HIGH);
   String json =  "{\"estado gpio0:\":"+String(gpio0_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio0off(){
   gpio0_state = "Off";
   digitalWrite(gpio0_pin, LOW);
   String json =  "{\"estado gpio0:\":"+String(gpio0_state)+"}";
   server.send (200, "application/json", json);
}

//gpio1 ----- não funciona como pino digital 

void getgpio3on(){
   gpio3_state = "On";
   digitalWrite(gpio3_pin, HIGH);
   String json =  "{\"estado gpio3:\":"+String(gpio3_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio3off(){
   gpio3_state = "Off";
   digitalWrite(gpio3_pin, LOW);
   String json =  "{\"estado gpio3:\":"+String(gpio3_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio4on(){
   gpio4_state = "On";
   digitalWrite(gpio4_pin, HIGH);
   String json =  "{\"estado gpio4:\":"+String(gpio4_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio4off(){
   gpio4_state = "Off";
   digitalWrite(gpio4_pin, LOW);
   String json =  "{\"estado gpio4:\":"+String(gpio4_state)+"}";
   server.send (200, "application/json", json);
}

//gpio9 ----- nao funciona e causa erro estranho 

void getgpio10on(){
   gpio10_state = "On";
   digitalWrite(gpio10_pin, HIGH);
   String json =  "{\"estado gpio10:\":"+String(gpio10_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio10off(){
   gpio10_state = "Off";
   digitalWrite(gpio10_pin, LOW);
   String json =  "{\"estado gpio10:\":"+String(gpio10_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio13on(){
   gpio13_state = "On";
   digitalWrite(gpio13_pin, HIGH);
   String json =  "{\"estado gpio13:\":"+String(gpio13_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio13off(){
   gpio13_state = "Off";
   digitalWrite(gpio13_pin, LOW);
   String json =  "{\"estado gpio13:\":"+String(gpio13_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio14on(){
   gpio14_state = "On";
   digitalWrite(gpio14_pin, HIGH);
   String json =  "{\"estado gpio14:\":"+String(gpio14_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio14off(){
   gpio14_state = "Off";
   digitalWrite(gpio14_pin, LOW);
   String json =  "{\"estado gpio14:\":"+String(gpio14_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio15on(){
   gpio15_state = "On";
   digitalWrite(gpio15_pin, HIGH);
   String json =  "{\"estado gpio15:\":"+String(gpio15_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio15off(){
   gpio15_state = "Off";
   digitalWrite(gpio15_pin, LOW);
   String json =  "{\"estado gpio15:\":"+String(gpio15_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio16on(){
   gpio16_state = "On";
   digitalWrite(gpio16_pin, HIGH);
   String json =  "{\"estado gpio16:\":"+String(gpio16_state)+"}";
   server.send (200, "application/json", json);
}

void getgpio16off(){
   gpio16_state = "Off";
   digitalWrite(gpio16_pin, LOW);
   String json =  "{\"estado gpio16:\":"+String(gpio16_state)+"}";
   server.send (200, "application/json", json);
}
