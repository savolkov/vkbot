# Ping plugin

import random

class Plugin:
    api = None
    f = None

    def __init__(self, api, f):
        self.api = api
        self.f = f
        print('Random')

    def getkeys(self):
        keys = ['рандом']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        lower = 1
        higher = 100
        words = msg[5].split()
        words[0] = words[0][1:len(words[0])]

        if (len(words) == 2):
            try:
                higher = int(words[1])
            except:
                pass

        if (len (words) == 3):
            try:
              higher = int(words[2])
              lower = int(words[1])
            except:
                pass
        if (lower > higher):
            t = lower
            lower = higher
            higher = t

        rand = random.randint(lower, higher)
        self.f.replyToMessage(
            api=self.api, msg=msg, text=str(rand), attachment='')
        
