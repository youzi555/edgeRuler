import HTTPRequest
import PykkaActor

def resolution(data):
    if data[0:2] == '15':
        hexGatewayName = data[22:42].rstrip('0')
        bytesGatewayName = bytes.fromhex(hexGatewayName)
        GatewayName = 'Gateway_'+str(bytesGatewayName, encoding='utf-8')
        HTTPRequest.getGateway(GatewayName)

    if data[0:2] == '70':
        PykkaActor.actor_ref.tell({'deviceData': '进入actor'})