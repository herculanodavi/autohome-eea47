import urllib.request
import json

class Communicator:
    pub = 'pub-c-71ef04a5-cf0e-48a0-9566-05d391a1794f'
    sub = 'sub-c-d0ba7b56-c25b-11e7-83f0-6e80f1f24680'
    channel = 'eea'
    server = 'http://pubsub.pubnub.com'
    timetoken = '0'

    # http://pubsub.pubnub.com
    #/publish
    #/pub-key
    #/sub-key
    #/signature
    #/channel
    #/callback
    #/message
    def makePublish(self, message):
        return self.server + '/publish' + '/' + self.pub + '/' + self.sub + '/0/' + self.channel + '/0/' + message

    #http://pubsub.pubnub.com
    #/subscribe
    #/sub-key
    #/timetoken
    #/channel
    #/callback
    def makeSubscribe(self, timetoken):
        return self.server + '/subscribe' + '/' + self.sub + '/' + self.channel + '/0/' + str(self.timetoken)

    def publish(self, message):
        message = urllib.parse.quote_plus('\"' + message + '\"')
        return json.loads(urllib.request.urlopen(self.makePublish(message)).read())

    def subscribe(self, timetoken = None):
        if timetoken is None:
            timetoken = self.timetoken
        try:
            result = json.loads(urllib.request.urlopen(self.makeSubscribe(timetoken), timeout=1).read())
            self.timetoken = result[1]
            return result
        except Exception as e:
            return None


if __name__ == "__main__":
    comm = Communicator()
    a = comm.subscribe()
    comm.publish('test succeded')
    b = comm.subscribe()
    print(b)
