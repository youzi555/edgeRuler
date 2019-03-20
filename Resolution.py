import HTTPRequest
import PykkaActor

def resolution(data):
    if data[0:2] == '15':
        hexGatewayName = data[22:42].rstrip('0')
        bytesGatewayName = bytes.fromhex(hexGatewayName)
        GatewayName = 'Gateway_'+str(bytesGatewayName, encoding='utf-8')
        HTTPRequest.getGateway(GatewayName)

    if data[0:2] == '70':
        deviceData = {}
        deviceData.update({'shortAddress': data[4:8]})
        deviceData.update({"Endpoint": data[8:10]})
        deviceData.update({'data': []})
        
        if data[10:14] == '0005':
            for i in range(0,int(data[14:16])):
                if data[16+i*10:20+i*10]=='8000' and data[20+i*10:22+i*10]=='21':
                    alarm = int(data[24+i*10:26+i*10]+data[22+i*10:24+i*10], 16)
                    j = 4
                    k = 3
                    for i in range(0,8):
                        if i == 0:
                            if alarm & k != 0:
                                deviceData.get('data').append({'key': 'alarm', 'value': 1})
                            else:
                                deviceData.get('data').append({'key': 'alarm', 'value': 0})
                            
                            i=i+1
                            continue
                                
                        if i == 2:
                            if alarm & j != 0:
                                deviceData.get('data').append({'key': 'temper', 'value': 1})
                            else:
                                deviceData.get('data').append({'key': 'temper', 'value': 0})
                                
                        if i == 3:
                            if alarm & j != 0:
                                deviceData.get('data').append({'key': 'battery', 'value': 1})
                            else:
                                deviceData.get('data').append({'key': 'battery', 'value': 0})
                                
                        if i == 4:
                            if alarm & j != 0:
                                deviceData.get('data').append({'key': 'supervision', 'value': 1})
                            else:
                                deviceData.get('data').append({'key': 'supervision', 'value': 0})
                                
                        if i == 5:
                            if alarm & j != 0:
                                deviceData.get('data').append({'key': 'restore', 'value': 1})
                            else:
                                deviceData.get('data').append({'key': 'restore', 'value': 0})
                                
                        if i == 6:
                            if alarm & j != 0:
                                deviceData.get('data').append({'key': 'trouble', 'value': 1})
                            else:
                                deviceData.get('data').append({'key': 'trouble', 'value': 0})
                                
                        if i == 7:
                            if alarm & j != 0:
                                deviceData.get('data').append({'key': 'ac', 'value': 1})
                            else:
                                deviceData.get('data').append({'key': 'ac', 'value': 0})
                                
                        j = j << 1
        if deviceData.get('data')!=[]:
            PykkaActor.actor_ref.tell({'deviceData':deviceData})
