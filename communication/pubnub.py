import urllib.request
import json

class Pubnub:
    pub = 'pub-c-71ef04a5-cf0e-48a0-9566-05d391a1794f'
    sub = 'sub-c-d0ba7b56-c25b-11e7-83f0-6e80f1f24680'
    server = 'http://pubsub.pubnub.com'
    timetoken = {'eea':'0', 'act_get':'0', 'act_res':'0', 'sen_get':'0', 'sen_res':'0'}


    def makePublish(self, message, channel):
        return self.server + '/publish' + '/' + self.pub + '/' + self.sub + '/0/' + channel + '/0/' + message

    def makeSubscribe(self, timetoken, channel):
        return self.server + '/subscribe' + '/' + self.sub + '/' + channel + '/0/' + str(timetoken)

    def publish(self, message, channel = 'eea'):
        # set message to url format and publish
        message = urllib.parse.quote_plus('\"' + message + '\"')
        return json.loads(urllib.request.urlopen(self.makePublish(message, channel)).read().decode("utf-8"))

    def getToken(self, channel):
        try:
            timetoken = self.timetoken[channel]
            #print('channel ' + channel + ' has timetoken ' + timetoken)
            return timetoken
        except:
            timetoken = '0'
            self.timetoken[channel] = timetoken
            #print('new channel ' + channel + ' has timetoken ' + timetoken)
            return timetoken

    def subscribe(self, channel = 'eea', timetoken = None):
        if timetoken is None:
            timetoken = self.getToken(channel)

        try:
            #print('channel ' + channel + ' has currently timetoken ' + timetoken)
            result = json.loads(urllib.request.urlopen(self.makeSubscribe(timetoken, channel), timeout=5).read().decode("utf-8"))
            #print('assigning ' + str(result[1]) + ' to ' + channel + ' timetoken')
            self.timetoken[channel] = result[1]
            return result
        except Exception as e:
            #print(e )
            return None

if __name__ == "__main__":
    comm = Pubnub()
    comm.subscribe()
    comm.subscribe('a')
    print(comm.subscribe())
    print(comm.timetoken)
