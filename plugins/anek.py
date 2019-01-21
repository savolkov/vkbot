# Memes plugin
import random

class Plugin:
    api = None
    f = None
    anecDomains = ['jumoreski', 'baneks', 'baneksbest']


    def __init__(self, api, f):
        self.api = api
        self.f = f
        print('Anek')

    def getkeys(self):
        keys = ['анек']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        text = self.f.getRandomWallPostText(
            self.api, random.choice(self.anecDomains))
        self.f.replyToMessage(
            api=self.api, msg=msg, text=text, attachment='')
        
