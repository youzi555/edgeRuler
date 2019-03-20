import startThread
from flask import Flask,render_template,request,url_for
import PykkaActor
import json

app = Flask(__name__,template_folder='templates')


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
        newFilters.append(newFilter)
        
    del requestbody.get('rule')['filters']
    requestbody.get('rule').update({'filters':newFilters})
    
    PykkaActor.actor_ref.tell(requestbody)
    
    return "success"
    
    
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, port=8080)

