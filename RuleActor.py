import pykka

class RuleActor(pykka.ThreadingActor):
    def __init__(self):
        super(RuleActor, self).__init__()
    
    def on_receive(self, message):
        print()