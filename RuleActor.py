import pykka

class RuleActor(pykka.ThreadingActor):
    def __init__(self, rule):
        super(RuleActor, self).__init__()
        self.rule = rule
    
    def on_receive(self, message):
        print()
        processData(message, self.rule)


def processData(message, rule):
    deviceSAAndEP = message.get('deviceData').get("shortAddress") + message.get('deviceData').get('Endpoint')
    result = True
    
    for filterFunc in rule.get('filters'):
        tag = True
        
        for data in message.get('deviceData').get(data):
            key = data.get('key')
            value = data.get('value')
            exec(filterFunc)
            tag = filterData(deviceSAAndEP, key, value) or tag
            
        result = result and tag
        if result == False:
            break
    
    controlOrSendRequest(message,rule)
        
# def controlOrSendRequest(message, rule):
#     for transform in rule.get('transform'):
#         if transform.get('name') == 'RestfulPlugin':
        