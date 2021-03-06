import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from pubnub.communicator import Communicator

def sendSensorRequest(string, radio, sensorWritingPipe):
    radio.openWritingPipe(sensorWritingPipe)
    radio.write(string)

def getSensorData(radio):
    radio.startListening()
    time.sleep(0.5)
    start = time.time()
    status = True
    while not radio.available(0):
        time.sleep(1/100)
        if time.time() - start >= 2:
            print("Can't get sensor data.")
            status = False
            break
    if status is True:
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        string = ""
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)
    radio.stopListening()
    return string


c = Communicator()

GPIO.setmode(GPIO.BCM)
 
pipes = [[0xAB, 0xCD, 0xAB, 0xCD, 0x71], [0xA8, 0xA8, 0xE1, 0xF0, 0xC6], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
# ABCDABCD71LL
# A8A8E1F0C6
sensorWritingPipe = pipes[0]

actuatorWritingPipe = pipes[1]

readingPipe = pipes[2]
 
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
 
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
 
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload() 

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()




while(1):
    time.sleep(3)
    sendSensorRequest("0", radio, sensorWritingPipe)
    # print(getSensorData(radio))



# sensor = list("0")
# actuator = list("1123")
# while len(sensor) < 32:
#     sensor.append(0)
#
# c.subscribe('act_get')
# while(1):
#     start = time.time()
#
#     radio.write(sensor)
#     radio.startListening()
#     while not radio.available(0):
#         time.sleep(1/100)
#         status = 1
#         if time.time() - start >= 2:
#             print("Timed out.")
#             status = 0
#             break
#         if status == 1:
#             receivedMessage = []
#             radio.read(receivedMessage, radio.getDynamicPayloadSize())
#             string = ""
#             for n in receivedMessage:
#                 if (n >= 32 and n <= 126):
#                     string += chr(n)
#             sensorValue = int(string)
#             c.publish(string, 'sen_res')
#             print("Valor convertido = ",sensorValue)
#         radio.stopListening()
#
#     message = c.subscribe(channel = 'act_get')
#
#     if message is not None:
#         status = 1
#         actuator = "1" + str(message[0][0]).zfill(3)
#         radio.write(actuador)
#         radio.starListening()
#         while not radio.available(0):
#             time.sleep(1/100)
#             status = 1
#             if time.time() - start >= 2:
#                 print("Timed out.")
#                 status = 0
#                 break
#         if status == 1:
#             receivedMessage = []
#             radio.read(receivedMessage, radio.getDynamicPayloadSize())
#             string = ""
#             for n in receivedMessage:
#                 if (n >= 32 and n <= 126):
#                     string += chr(n)
#             sensorValue = int(string)
#             c.publish("Door toggled!", 'act_res')
#             print("Posicao do servo = ", sensorValue)
#         radio.stopListening()
#
#     time.sleep(1)
