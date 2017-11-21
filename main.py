from communication.pubnub import Pubnub
from communication.radio import Radio
import time

radio = Radio()

c = Pubnub()
while(1):
    # reading sensor data and publishing it to webapp
    print('Sending sensor request...')
    req = radio.sendSensorRequest('0')
    print('Message protocol returned ' + str(req))
    if req != 0:
        message = radio.getSensorData()
        if message is not None:
            print('Sending ' + message + ' to pubnub')
            c.publish(message, 'sen_res')

    print('--------------------')
    print(' ')

    # reading actuator data and publishing it to webapp
    print('Sending actuator request...')
    req = radio.sendActuatorRequest('12')
    print('Message protocol returned ' + str(req))
    if radio.sendActuatorRequest("12") != 0:
        message = radio.getActuatorData()
        if message is not None:
            print('Sending ' + message + ' to pubnub')
            c.publish(message, 'act_res')

    print('--------------------')
    print(' ')

    # reading pubnub to change door status
    message = c.subscribe('act_get')
    if message is not None:
        if len(message[0]) > 0:
            print('Sending actuator action request...')
            print('Message is ' + str(message))
            print('Request returned ' + str(radio.sendActuatorRequest('1' + str(message[0][0]))))

    print('--------------------')
    print(' ')
