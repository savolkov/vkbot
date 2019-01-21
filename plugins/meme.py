# Memes plugin
import random

class Plugin:
    api = None
    f = None
    memeDomains = ['rjekich', 'shitpostmeme', 'cursed_images',
                   'eternalclassic', 'ebebob', 'depressive_memes', 'aggressivememes']


    def __init__(self, api, f):
        self.api = api
        self.f = f
        print('Memes')

    def getkeys(self):
        keys = ['мем']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        attachment = self.f.getRandomWallPostAttachment(
            self.api, random.choice(self.memeDomains))
        self.f.replyToMessage(api=self.api, msg=msg,
                            text='', attachment=attachment)
        
