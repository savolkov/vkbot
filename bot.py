import func
import vk
import requests
import time
import sys
import random
import sqlite3
import os

import config

def main():
    # vk.logger.setLevel('DEBUG')
    print('INFO: Bot started')
    cooldowns = {} # cooldowns dictionary

    # conn = sqlite3.connect('db.db')
    # print('INFO: Db connected')
    api = func.getApi(config)
    params = func.getLongpollApiParams(api)

    cmds = {} # commands dictionary
    plugins = {} # plugins dictionary


    print('INFO: Loading plugins')
    # Подгружаем плагины
    plugins = func.loadPlugins(api, func)
    # Регистрируем плагины
    cmds = func.registerPlugins(plugins)

    while True:
        time.sleep(1)
        msgs = func.getNewMsgs(params)
        if ('failed' in msgs):
            if (msgs['failed'] == 2 or msgs['failed'] == 3 or msgs['failed'] == 1):
                params = func.getLongpollApiParams(api)
                print('WARN: key/ts expired: requested new')
                continue
        try:
            for msg in msgs['updates']:
                params['ts'] = msgs['ts']
                # проверим на сообщение
                if (func.isMessage(msg)):
                    print('INFO: new msg:' + msg[5])
                    #  если голосовое
                    if (func.isVoiceMessage(msg)):
                        func.replyToMessage(
                            api=api, msg=msg, text=random.choice(config.voiceWarns), attachment='')
                        api.messages.markAsRead(peer_id=msg[3])
                    # если команда
                    try:
                        words = func.checkCommand(msg, cooldowns, cmds)
                        if (words != False):
                            cmds[words[0]].call(msg)
                    except:
                        func.replyToMessage(api=api,
                        msg=msg,
                        text=random.choice(config.errorMsgs),
                        attachment='')

                # проверим на добавление в конфу
                pId = func.wasAddedToDialogue(msg)
                if (pId != -1):
                    func.sendMessage(api=api,
                                    where=pId,
                                    text=random.choice(config.helloMsgs),
                                    attachment='')
                    api.messages.markAsRead(peer_id=pId)
                    
        except:
           print("EXC:", sys.exc_info()[0])

if __name__ == '__main__':
    main()
