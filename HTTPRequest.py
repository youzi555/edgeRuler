from urllib import parse, request
import json
import threading
import MQTT

def getGateway(gatewayName):
    textmod = {'limit': '20', 'textSearch': gatewayName}
    textmod = parse.urlencode(textmod)
    print(textmod)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    url = 'http://47.105.120.203:30080/api/v1/deviceaccess/tenant/devices/2'
    
    req = request.Request(url='%s%s%s' % (url, '?', textmod), headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    
    #print(res.decode(encoding='utf-8'))
    
    gatewayDict = json.loads(res.decode(encoding='utf-8'))
    id = gatewayDict.get("data")[0].get("id")
    
    print(id)
    getCredentialbyid(id)
   
def getCredentialbyid(id) :
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    url = 'http://47.105.120.203:30080/api/v1/deviceaccess/credentialbyid/'+id

    req = request.Request(url=url, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    
    credentialFullMessage = json.loads(res.decode(encoding='utf-8'))
    token = credentialFullMessage.get("deviceToken")
    print(token)
    
    mqttThread = MQTTThread(token)
    mqttThread.start()
    


class MQTTThread(threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.token = token

    def run(self):
        MQTT.mqtt_start(token=self.token)
