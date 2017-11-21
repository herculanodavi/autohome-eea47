from communication.pubnub import Pubnub
from communication.radio import Radio
import time

radio = Radio()

c = Pubnub()

while(1):
    time.sleep(3)
    if radio.sendSensorRequest("0") != 0:
        message = radio.getSensorData(radio)
        print(message)
    c.publish(message, 'sen_res')
