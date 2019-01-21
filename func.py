import random
import config
import requests
import vk
import time
import sys
import os

def checkCommand(msg, cooldowns, cmds):
    if (len(msg[5]) > 0):
        if(msg[5][0] == '!'):
            cmd = msg[5].lower()
            words = cmd.split()
            words[0] = words[0][1:len(words[0])]
            if (checkCooldown(msg, cooldowns) and (words[0] in cmds)):
                return words
    return False


def getNewMsgs(params):
    getMessagesUrl = 'https://%(server)s?act=a_check&key=%(key)s&ts=%(ts)s&wait=25&mode=2&version=2' % params
    reply = requests.get(getMessagesUrl)
    return reply.json()

def registerPlugins(plugins):
    cmds = {}
    for plugin in plugins.values():
        for key, value in plugin.getkeys().items():
            cmds[key] = value
    return cmds

def loadPlugins(api, func):
    plugins = {}
    sys.path.insert(0, config.plPath)
    for f in os.listdir(config.plPath):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            mod = __import__(fname)
            plugins[fname] = mod.Plugin(api, func)
    sys.path.pop(0)
    return plugins

def getLongpollApiParams(api):
    """Returns params required for VK Longpoll API"""
    gotParams = False
    while (not gotParams):
        try:
            api = getApi(config)
            params = api.messages.getLongPollServer()
            print('INFO: Got longpoll params success')
            gotParams = True
        except:
            print('WARN: Error getting longpoll params. Sleeping.')
            print("EXC:", sys.exc_info()[0])    
            time.sleep(config.reconnectTimeout)
            gotParams = False
    return params

def getApi(config):
    """Authorizes user specificated in `config`, returns `api`"""
    session = vk.AuthSession(app_id=config.APPID,
    user_login=config.USERNAME,
    user_password=config.PWD,
    scope='messages')
    print('INFO: Auth success')
    api = vk.API(session, v=config.V, lang='ru')
    return api

def isMessage(event):
    if (event[0] == 4):
        return True
    else:
        return False


def isVoiceMessage(msg):
    if (len(msg) < 6):
        return False
    if('attach1_kind' in msg[6]):
        if(msg[6]['attach1_kind'] == 'audiomsg'):
            return True
    return False


def replyToMessage(api, msg, text, attachment):
    api.messages.send(peer_id=msg[3],
                      reply_to=msg[1],
                      attachment=attachment,
                      message=text,
                      random_id=random.randint(1, 1000000000))
    print('INFO: Reply')

def sendMessage(api, where, text, attachment):
    api.messages.send(peer_id=where,
                      message=text,
                      random_id=random.randint(1, 1000000000),
                      attachment=attachment)
    print('INFO: SentMSG')

# returns peer_id or -1
def wasAddedToDialogue(event):
    if (event[0] == 52):
        if (str(event[1]) == '6' and str(event[3]) == config.ID_SELF):
            return event[2]
    return -1

def getPostsCount(api, domain):
    res = api.wall.get(domain=domain, offset=0, count=1)
    return res['count']

def getRandomWallPostAttachment(api, domain):
    post = api.wall.get(domain=domain, offset=random.randint(0, getPostsCount(api, domain)), count=1)
    randomAttachment = random.choice(post['items'][0]['attachments'])
    t = randomAttachment['type']
    ret = randomAttachment['type'] + \
        str(randomAttachment[t]['owner_id']) + '_' + \
        str(randomAttachment[t]['id']) + '_' + randomAttachment[t]['access_key']
    return ret

def getRandomWallPostText(api, domain):
    post = api.wall.get(domain=domain, offset=random.randint(
        0, getPostsCount(api, domain)), count=1)
    return post['items'][0]['text']

def countChatMembers(api, peerId):
    ret = api.messages.getConversationMembers(peer_id=peerId)
    return ret['count']

def isAdmin (user):
    return (str(user) in config.adminList)

def isWhitelisted(user):
    return ((str(user) in config.whiteList) or isAdmin(user))

def checkCooldown(msg, cooldowns):
    if (not 'from' in msg[6]):
        return True
    user = str(msg[6]['from'])
    if (isWhitelisted(user)):
        return True
    if (user in cooldowns):
        if (time.time() - cooldowns[user] > config.cooldown):
            cooldowns[user] = time.time()
            return True
        else:
            return False
    else:
        cooldowns[user] = time.time()
        return True

def checkNSFW(api, msg):
    if (countChatMembers(api, msg[3]) > config.nsfwCount):
        replyToMessage(api=api, msg=msg, text=random.choice(
            config.nsfwMessages), attachment='')
        return False
    else:
        return True
