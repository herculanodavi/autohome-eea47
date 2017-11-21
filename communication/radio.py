import RPi.GPIO as GPIO
from .lib_nrf24 import NRF24
import spidev
import time

class Radio:
    sensorWritingPipe = [0xAB, 0xCD, 0xAB, 0xCD, 0x71]
    actuatorWritingPipe = [0xA8, 0xA8, 0xE1, 0xF0, 0xC6]
    readingPipe = [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(0, 17)

        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x76)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_MAX)

        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()

        self.radio.openWritingPipe(self.sensorWritingPipe)
        self.radio.openReadingPipe(1, self.actuatorWritingPipe)
        self.radio.printDetails()

    # Send message through pipe
    def send(self, pipe, message):
        self.radio.openWritingPipe(pipe)
        return self.radio.write(message)

    # Request sensor reading
    def sendSensorRequest(self, message):
        return self.send(self.sensorWritingPipe, message)

    # Request actuator reading
    def sendActuatorRequest(self, message):
        return self.send(self.actuatorWritingPipe, message)

    # Read sensor result after request
    def getSensorData(self):
        self.radio.startListening()
        time.sleep(0.5)
        start = time.time()

        while not self.radio.available(0):
            time.sleep(1/100)
            if time.time() - start >= 3:
                print("getSensorData timed out.")
                return None

        receivedMessage = []
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())

        string = ""
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)

        self.radio.stopListening()
        return string

#---------------------------#
#      Module Testing       #
#---------------------------#
if __name__ == '__main__':
    r = Radio()
    r.sendSensorRequest('0')
    print(getSensorData())
