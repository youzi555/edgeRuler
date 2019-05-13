import stomper
from websocket import create_connection

def connection(gatewayId):
    ws = create_connection("ws://47.105.120.203:30080/api/v1/smartruler/edge/"+gatewayId)
    
