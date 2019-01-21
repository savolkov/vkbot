# Memes plugin
import random

class Plugin:
    api = None
    f = None
    catDomains = ['loaf_cat', 'catsandsynths', 'murmewmur', 'the.kot.world']


    def __init__(self, api, f):
        self.api = api
        self.f = f
        print('Cats')

    def getkeys(self):
        keys = ['мяу']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        attachment = self.f.getRandomWallPostAttachment(
            self.api, random.choice(self.catDomains))
        self.f.replyToMessage(
            api=self.api, msg=msg, text='', attachment=attachment)
        
