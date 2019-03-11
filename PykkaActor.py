import pykka
import RuleActor

deviceToActor = {}

class Greeter(pykka.ThreadingActor):
    def __init__(self):
        super(Greeter, self).__init__()
        
    def on_receive(self, message):
        print(message)
        
    def on_start(self):
        print()
        
        
actor_ref = Greeter.start()
