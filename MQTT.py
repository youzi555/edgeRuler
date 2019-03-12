import paho.mqtt.client as mqtt
import time
import json
import PykkaActor

MQTTHOST = "47.105.120.203"
MQTTPORT = 30011
#mqttClient = mqtt.Client()

def mqtt_connect(mqttClient, token):
    mqttClient.username_pw_set(token)
    mqttClient.on_connect = on_connect
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_forever()
    

def on_connect(mqttClient, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt_subscribe(mqttClient)
    

def mqtt_subscribe(mqttClient):
    mqttClient.subscribe('v1/devices/me/rpc/request/+', 1)
    mqttClient.on_message = on_message_come
   
 
def on_message_come(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))
    #TODO 存入数据库
    jsonMsg = json.loads(msg.payload.decode("utf-8"))
    PykkaActor.actor_ref.tell(jsonMsg)
    


def mqtt_start(token):
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    mqttClient = mqtt.Client(client_id)
    mqtt_connect(mqttClient, token)
    while True:
         pass


