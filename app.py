import startThread
import copy
from flask import Flask,render_template,request,url_for
import PykkaActor
import json
import execjs
import RuleSql
import FilterSql
import TransformSql
import Monitor

app = Flask(__name__,template_folder='templates')

@app.route('/getRule', methods=['GET'])
def getRule():
    rd = RuleSql.selectAllRules()
    return str(rd)

@app.route('/test', methods=['POST'])
def test():
    data = request.get_data()
    print(data)
    requestbody = json.loads(data.decode('utf-8'))
    newFilters = []
    Endpoint = hex(int(requestbody.get('rule').get('Endpoint')))
    if Endpoint.__len__() == 4:
        deviceSAAndEP = requestbody.get('rule').get('shortAddress')+Endpoint[2:4]
    else:
        deviceSAAndEP = requestbody.get('rule').get('shortAddress') + '0' + Endpoint[2:4]
    
    for filter in requestbody.get("rule").get('filters'):
        newFilter = "function filter(deviceSAAndEP, key, value){" \
                        "if (deviceSAAndEP=='"+deviceSAAndEP+"' && key == '"+filter.get('key')+"' && value"+filter.get('value')+"){" \
                        "   return true;}" \
                        "else{" \
                        "   return false;}}"
        newFilter = newFilter.replace("\\", "")
        
        filter.update({'filterCode': newFilter})
        del filter['key']
        del filter['value']
        
        compileFilter = execjs.compile(newFilter)
        newFilters.append(compileFilter)

    savebody = copy.deepcopy(requestbody)
    saveRule(savebody.get('rule'))
    del requestbody.get('rule')['filters']
    requestbody.get('rule').update({'filters': newFilters})
    
    # check resource
    tag = Monitor.checkResource()
    if tag == False:
        tag = Monitor.resourceOffload(requestbody.get('rule').get('level'))

    if not tag:
        # TODO 向云端发送激活当前下发任务的指令
        if requestbody.get('rule').get('level') == 10:
            RuleSql.updateRuleLevel(8, requestbody.get('rule').get('ruleId'))
    
        RuleSql.updateRuleState('CLOUD', requestbody.get('rule').get('ruleId'))
        return "error: out of resources"
        
    PykkaActor.actor_ref.tell(requestbody)
    return "success"
    
    
@app.route('/')
def hello_world():
    return 'Hello World!'


def saveRule(dict):
    rule_dict = {}
    rule_dict.update({'ruleId': dict.get("ruleId"),
                      'state': dict.get("state"),
                      'shortAddress': dict.get("shortAddress"),
                      'level':dict.get('level'),
                      'Endpoint': dict.get("Endpoint")})
    RuleSql.insertRule(rule_dict)
    
    filter_dicts = []
    filter_dict = {}
    
    for filter in dict.get('filters'):
        filter_dict['filterId'] = filter.get('filterId')
        filter_dict['ruleId'] = dict.get('ruleId')
        filter_dict['filterCode'] = filter.get('filterCode')
        filter_dicts.append(filter_dict)
    
    FilterSql.insertManyFilter(filter_dicts)
    
    transforms = []
    transform = {}
    for transform_dict in dict.get('transform'):
        transform['transformId'] = transform_dict.get('transformId')
        transform['ruleId'] = dict.get('ruleId')
        transform['name'] = transform_dict.get('name')
        transform['url'] = transform_dict.get('url')
        transform['method'] = transform_dict.get('method')
        transform['body'] = str(transform_dict.get('body'))
        
        transforms.append(transform)
    
    TransformSql.insertManyTransform(transforms)

    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

