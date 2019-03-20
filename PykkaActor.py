import pykka
import RuleActor
import UDPSocket



deviceToActor = {}

class Greeter(pykka.ThreadingActor):
    def __init__(self):
        super(Greeter, self).__init__()
    
    def on_receive(self, message):
        print(message)
        #TODO 根据设备id查询规则，并下发
        if 'deviceData' in message:
            # UDPSocket.sendControlMessage('control switch', 'setstate', 'ce4e10', '01')
            deviceSAAndEP = message.get('deviceData').get("shortAddress")+message.get('deviceData').get('Endpoint')
            if deviceSAAndEP in deviceToActor.keys():
                for ruleActor in deviceToActor.get(deviceSAAndEP):
                    ruleActor.tell(message)

        if 'rule' in message:
            deviceSAAndEP =message.get("rule").get("shortAddress")+message.get("rule").get("Endpoint")
            actor_ref = RuleActor.RuleActor.start(message.get("rule"))
            deviceToActor.setdefault(deviceSAAndEP,[]).append(actor_ref)
            
            
    def on_start(self):
        print('启动pykka')
        
    def on_stop(self):
        print('停止pykka')
        

actor_ref = Greeter.start()


