from communication.pubnub import Pubnub
from communication.radio import Radio
import time

radio = Radio()

while(1):
    time.sleep(3)
    if radio.sendSensorRequest("0") != 0:
        print(radio.getSensorData(radio))
