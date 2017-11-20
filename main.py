import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
 
GPIO.setmode(GPIO.BCM)
 
pipes = [[0x00, 0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00, 0x01], [0x00, 0x00, 0x00, 0x00, 0x02]]

 
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
 
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
 
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
 
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.printDetails()
