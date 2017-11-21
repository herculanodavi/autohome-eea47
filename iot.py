from communication.pubnub import Pubnub
from communication.radio import Radio

radio = Radio()

while(1):
    time.sleep(3)
    print(radio.sendSensorRequest("0"))
    # print(getSensorData(radio))
