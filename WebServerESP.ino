#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <ESPAsyncWebServer.h>

#define LED1 D1
#define LED2 D2
#define LED3 D5
#define LED4 D7
#define LED5 D8

char webpage[] PROGMEM = R"=====(
<!DOCTYPE html>
<html>
<body>

<center>
<h1>Gesture Controlled LEDS</h1>

<h3> LED 1 </h3>
<button onclick="window.location = 'http://'+location.hostname+'/led1/On'"> On </button><button onclick="window.location = 'http://'+location.hostname+'/led1/Off'"> Off </button>
<h3> LED 2 </h3>
<button onclick="window.location = 'http://'+location.hostname+'/led2/On'"> On </button><button onclick="window.location = 'http://'+location.hostname+'/led2/Off'"> Off </button>
<h3> LED 3 </h3>
<button onclick="window.location = 'http://'+location.hostname+'/led3/On'"> On </button><button onclick="window.location = 'http://'+location.hostname+'/led3/Off'"> Off </button>
<h3> LED 4 </h3>
<button onclick="window.location = 'http://'+location.hostname+'/led4/On'"> On </button><button onclick="window.location = 'http://'+location.hostname+'/led4/Off'"> Off </button>
<h3> LED 5 </h3>
<button onclick="window.location = 'http://'+location.hostname+'/led5/On'"> On </button><button onclick="window.location = 'http://'+location.hostname+'/led5/Off'"> Off </button>
</center>

</body>
</html>




)=====";
//ipaddress/led1/on
//ipaddress/led1/off

//ipaddress/led2/on
//ipaddress/led2/off

AsyncWebServer server(80); //server port 80

void notFound(AsyncWebServerRequest *request)
{
  request->send(404, "text/plain", "Not Found");
}


void setup(void) 
{    
  Serial.begin(9600);
  pinMode(LED1,OUTPUT);
  pinMode(LED2,OUTPUT);
  pinMode(LED3,OUTPUT);
  pinMode(LED4,OUTPUT);
  pinMode(LED5,OUTPUT);

  WiFi.softAP("ESP_WEBSrv", "");    //defines access point name and password
  Serial.println("softap");
  Serial.println("");
  Serial.println(WiFi.softAPIP());  //print IP of access point to serial monitor 
  
  if (MDNS.begin("ESP")){ //esp.local/
    Serial.println("MDNS responder started");
  }
//Main page
  server.on("/", [](AsyncWebServerRequest *request)
  {
    request->send_P(200, "text/html", webpage);
  });

//LED1 on/off
  server.on("/led1/On", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED1,HIGH);
    request->send(200, "text/html", webpage);
  });
  server.on("/led1/Off", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED1,LOW);
    request->send(200, "text/html", webpage);
  });

  //LED2 on/off
  server.on("/led2/On", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED2,HIGH);
    request->send(200, "text/html", webpage);
  });
  server.on("/led2/Off", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED2,LOW);
    request->send(200, "text/html", webpage);
  });

  //LED3 on/off
  server.on("/led3/On", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED3,HIGH);
    request->send(200, "text/html", webpage);
  });
  server.on("/led3/Off", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED3,LOW);
    request->send(200, "text/html", webpage);
  });

//LED4 on/off
  server.on("/led4/On", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED4,HIGH);
    request->send(200, "text/html", webpage);
  });
  server.on("/led4/Off", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED4,LOW);
    request->send(200, "text/html", webpage);
  });

  //LED5 on/off
  server.on("/led5/On", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED5,HIGH);
    request->send(200, "text/html", webpage);
  });
  server.on("/led5/Off", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(LED5,LOW);
    request->send(200, "text/html", webpage);
  });


  server.onNotFound(notFound);
  server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:

}
