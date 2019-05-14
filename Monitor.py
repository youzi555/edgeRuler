import psutil
import sched
import time
import threading
import RuleSql
import PykkaActor
import app

def getMemoryUse():
    mem = psutil.virtual_memory()
    return mem.percent

def getCPUUse():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

def scheduleMonitor():
    memUse = getMemoryUse()
    cpuUse = getCPUUse()
    if memUse > 80 or cpuUse > 90:
        tag = resourceOffload(11)
        
    if memUse <= 70 and cpuUse <= 75:
        #TODO 向云端发送请求下发规则的消息
        print()
    
    threading.Timer(300, scheduleMonitor).start()
    
def resourceOffload(level):
    tag = False
    while not tag:
        rule_list = RuleSql.searchLowPriorityRule(level)
    
        for rule_dict in rule_list:
            # TODO 向云端发送规则激活的命令
        
            stop_dict = {}
            stop_dict.update({'stop': rule_dict})
            res = PykkaActor.actor_ref.ask(stop_dict)
        
            RuleSql.updateRuleState('CLOUD', rule_dict.get('ruleId'))
        
            if res:
                tag = checkResource()
        
            if tag:
                return tag
        
        if len(rule_list) == 0:
            return tag
    
    return False


def checkResource():
    cpu = getCPUUse()
    mem = getMemoryUse()
    
    if cpu <= 90 and mem <= 80:
        return True
    else:
        return False


threading.Timer(300, scheduleMonitor).start()
