//SendReceive.ino
 
#include<SPI.h>
#include<RF24.h>
#include<string.h>
 
// CE, CSN pins
RF24 radio(7, 8);


char receivedMessage[32] = {0};
const uint64_t readingPipe = (0xABCDABCD71LL);
const uint64_t writingPipe = (0xF0F0F0F0E1LL);

void initRadio(){
  radio.begin();
  
  radio.setPALevel(RF24_PA_HIGH);
    
  radio.setChannel(0x76);
  
  radio.openWritingPipe(writingPipe);
  radio.openReadingPipe(1, readingPipe);
  
  radio.setAutoAck(true);
  radio.enableDynamicPayloads();
  radio.enableAckPayload();

  radio.powerUp();
}

void getData(){
  radio.setRxMode();
  radio.startListening();
  delay(250);
  int i = 1;
  while(!radio.available()){
    delay(10);
    i++;
    if(i>=100){
      Serial.println("getData timed out");
      return;
    }
  }
  radio.read(receivedMessage, sizeof(receivedMessage));
  Serial.print("Received message: ");
  Serial.println(receivedMessage);
  radio.stopListening();
}
/*
int sendData(char string[]){
  Serial.println("Sending data");
  
  Serial.println(a);
  return a;
}*/
  

void setup(void){
  while(!Serial);
  Serial.begin(9600);
  initRadio();
}
 
void loop(void){
  getData();
  int b;
  char text[] = "1234";
  //String text = "1234";
  if(receivedMessage[0] == '0'){
    radio.setTxMode();
    b = radio.write(text, sizeof(text));
    Serial.println(b);
  }
}
