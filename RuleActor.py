import pykka
import UDPSocket
import execjs

class RuleActor(pykka.ThreadingActor):
    def __init__(self, rule):
        super(RuleActor, self).__init__()
        self.rule = rule
    
    def on_receive(self, message):
        print()
        processData(message, self.rule)
        
    def on_failure(self, exception_type, exception_value, traceback):
        print(exception_type+":"+exception_value)


def processData(message, rule):
    deviceSAAndEP = message.get('deviceData').get("shortAddress") + message.get('deviceData').get('Endpoint')
    result = True
    
    for filterFunc in rule.get('filters'):
        tag = False
        
        for data in message.get('deviceData').get('data'):
            key = data.get('key')
            value = data.get('value')
            # loc = locals()
            try:
                eachresult = filterFunc.call("filter", deviceSAAndEP, key, value)
            except Exception as e:
                print(e)
            # result = loc['result']

            # print(result)
            tag = eachresult or tag
            if tag == True:
                break;
            
        result = result and tag
        if result == False:
            break
    
    if result == True:
        controlOrSendRequest(message, rule)
    
def controlOrSendRequest(message, rule):
     for transform in rule.get('transform'):
         if transform.get('name') == 'RestfulPlugin':
            body = transform.get('body')
            serviceName = body.get('serviceName')
            methodName = body.get('methodName')
            Endpoint = hex(int(body.get('Endpoint')))
            if Endpoint.__len__() == 4:
                deviceSAAndEP = body.get('shortAddress') + Endpoint[2:4]
            else:
                deviceSAAndEP = body.get('shortAddress') + '0' + Endpoint[2:4]
            state = body.get('status')
            UDPSocket.sendControlMessage(serviceName, methodName, deviceSAAndEP, state)