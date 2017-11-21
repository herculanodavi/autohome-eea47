/*
* Arduino Wireless Communication Tutorial
*     Example 2 - Receiver Code
*                
* by Dejan Nedelkovski, www.HowToMechatronics.com
* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/
#include <SPI.h>
#include <string.h>
//#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

RF24 radio(7, 8); // CE, CSN
Servo myServo;

void setup() {
  while(!Serial);
  Serial.begin(9600);
  
  myServo.attach(6);

  radio.begin();
  radio.setPALevel(RF24_PA_HIGH);
  radio.setChannel(0x76);
  radio.openWritingPipe(0x0000000001LL);
  const uint64_t pipe = (0x0000000000LL);
  radio.openReadingPipe(1, pipe);

  radio.enableDynamicPayloads();
  radio.powerUp();
}

void loop() {
  // Entrando no modo escuta: Esperando mensagem.
  radio.startListening();
  delay(100);
  char message[32] = {0};
  int angle = 0;
  // Caso chegue mensagem
  if(radio.available())
  {
    radio.read(message, sizeof(message));
    Serial.println(message); // Debug 
    // Verificando protocolo: Código do sensor '1'.
    // Mensagem esperada '1AAA', sendo AAA o ângulo desejado para o servo;
    if (message[0] = '1')
    {
      // Convertendo para int, modificando valor do ângulo do atuador.
      angle = int(100*(message[1]-'0') + 10*(message[2]-'0') + message[3] -'0');
      myServo.write(angle);

      // Enviando devolutiva. Mensagem esperada: 'Valor do angulo no servo: AAA'
      radio.stopListening();
      char valor = char(angle);
      
      Serial.println(valor); // Debug 
      radio.write(valor, sizeof(valor));
    }
  }
}
