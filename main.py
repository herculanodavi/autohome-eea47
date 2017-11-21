from communication.pubnub import Pubnub
from communication.radio import Radio
import time

radio = Radio()

c = Pubnub()

while(1):
    time.sleep(2)
    print('Sending sensor request...')
    if radio.sendSensorRequest("0") != 0:
        message = radio.getSensorData()
        if message is not None:
            print('Sending ' + message + ' to pubnub')
            c.publish(message, 'sen_res')

    print('--------------------')
    print(' ')
