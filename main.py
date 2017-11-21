from communication.pubnub import Pubnub
from communication.radio import Radio
import time

radio = Radio()

c = Pubnub()
while(1):
    time.sleep(2)
    # reading sensor data and publishing it to webapp
    print('Sending sensor request...')
    if radio.sendSensorRequest("0") != 0:
        message = radio.getSensorData()
        if message is not None:
            print('Sending ' + message + ' to pubnub')
            c.publish(message, 'sen_res')

    print('--------------------')
    print(' ')

    # reading pubnub to change door status
    message = c.subscribe('act_get')
    if message is not None:
        if len(message[0]) > 0:
            print('Sending actuator request...')
            print(radio.sendActuatorRequest('0' + str(message[0][0])))

    print('--------------------')
    print(' ')
