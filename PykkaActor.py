import pykka
import RuleActor
import UDPSocket
import RuleSql
import FilterSql
import TransformSql
import execjs
import json



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
            
        if 'stop' in message:
            deviceSAAndEP = message.get("stop").get("shortAddress") + message.get("stop").get("Endpoint")
            if deviceSAAndEP in deviceToActor.keys():
                for ruleActor in deviceToActor.get(deviceSAAndEP):
                    if ruleActor.rule.get('ruleId') == message.get('stop').get('ruleId'):
                        deviceToActor.get(deviceSAAndEP).remove(ruleActor)
                        ruleActor.stop()
                        break
            
            return True
            
    def on_start(self):
        print('启动pykka')
        rule_dicts = RuleSql.selectAllRules()
        
        for rule_dict in rule_dicts:
            filter_dicts = FilterSql.selectFilters(rule_dict.get('ruleId'))
            filters = []
            for filter_dict in filter_dicts:
                newFilter = execjs.compile(filter_dict.get('filterCode'))
                filters.append(newFilter)
                
            rule_dict["filters"] = filters
            
            transform_dicts = TransformSql.selectTransforms(rule_dict.get('ruleId'))
            for transform_dict in transform_dicts:
                strBody = transform_dict.get('body').replace("\'", "\"")
                body = json.loads(strBody)
                del transform_dict['body']
                transform_dict['body'] = body
                del transform_dict['ruleId']
            
            rule_dict['transform'] = transform_dicts

            deviceSAAndEP = rule_dict.get("shortAddress") + rule_dict.get("Endpoint")
            actor_ref = RuleActor.RuleActor.start(rule_dict)
            deviceToActor.setdefault(deviceSAAndEP, []).append(actor_ref)
        
    def on_stop(self):
        print('停止pykka')
        

actor_ref = Greeter.start()


