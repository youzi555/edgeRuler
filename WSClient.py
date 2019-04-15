import websocket

def on_message(ws, message):
    print(message)
    
def on_error(ws, error):
    print(error)

def on_close(ws):
    print('websocket is closed')

def on_open(ws):
    print('websocket is opening')

def start_websocket(gatewayId):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://47.105.120.203:30080/api/v1/smartruler/"+gatewayId,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

