# Ping plugin

class Plugin:
    api = None
    f = None

    def __init__(self, api, f):
        self.api = api
        self.f = f
        print('Help')

    def getkeys(self):
        keys = ['помощь']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        text = 'Команды: !анек\n!мем\n!рандом (можно указать границы, например, "!рандом 1 5")\n!пинг\n!сиськи\n!мем\n!погода (укажите город, например "!погода Москва")'
        self.f.replyToMessage(
            api=self.api, msg=msg, text=text, attachment='')
        
