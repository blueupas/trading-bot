#-*- coding:utf-8 -*-
#!/usr/bin/env python

import sys
import time
import telegram
import telepot
import collect




from telepot.loop import MessageLoop

msgmgr = telegram.message()
db = collect.TradingDB()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if content_type == 'text':
        if str(msg['text']).startswith('등록'):
            splitedstr = str(msg['text']).split(" ")
            msgmgr.sendMsg(chat_id, splitedstr[1] + "님 환영합니다")
            db.insertMsg(chat_id, splitedstr[1])
            return None
        if msg['text'] == '멤버보기':
            memberList = db.getMemberList()
            for memberName in memberList:
                msgmgr.sendMsg(chat_id, memberName)
            return None
        if msg['text'] == '조용해':
            db.enableSlientMode(chat_id)
            msgmgr.sendMsg(chat_id, "쉿~!")
            return None
        if msg['text'] == '알려줘':
            db.disableSlientMode(chat_id)
            msgmgr.sendMsg(chat_id, "이제부터 알림 활성화!")
            return None
        print("msg:" + msg['text'])
    else:
        db.insertMsg(chat_id, '?')
    msgmgr.sendMsg(chat_id, " - 명령어 - \n > 멤버보기 \n > 등록 [사용자이름] \n > 조용해 \n > 알려줘")


MessageLoop(msgmgr.getBot(), handle).run_as_thread()

print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)