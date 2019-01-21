# Ping plugin

class Plugin:
    api = None
    f = None

    def __init__(self, api, f):
        self.api = api
        self.f = f
        print('Ping')

    def getkeys(self):
        keys = ['пинг', 'тест']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        self.f.replyToMessage(
            api=self.api, msg=msg, text='Понг', attachment='')
        
