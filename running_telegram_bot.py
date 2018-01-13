#-*- coding:utf-8 -*-
#!/usr/bin/env python

import sys
import time
import telegram
import telepot
import collect
import coin
import property
import korbit_status
from telepot.loop import MessageLoop


myProperty = property.local_property()

msgmgr = telegram.message()
db = collect.TradingDB()

coinInfo = coin.coinInfo()
currency_pair_list = coinInfo.getCurrentPairList()

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
        if msg['text'] == '알람off':
            db.enableSlientMode(chat_id)
            msgmgr.sendMsg(chat_id, "쉿~!")
            return None
        if msg['text'] == '알람on':
            db.disableSlientMode(chat_id)
            msgmgr.sendMsg(chat_id, "이제부터 알림 활성화!")
            return None
        if msg['text'] == '현재가' or msg['text'].startswith('현'):
            msgmgr.sendMsg(chat_id, korbit_status.getMsgStrForLastPrice(db))
            return None
        if msg['text'] == '보유현황' or msg['text'].startswith('보'):
            if (chat_id == myProperty.getMyChatId()):
                msgmgr.sendMsg(chat_id, korbit_status.getMsgStrForBalance(db))
            else :
                msgmgr.sendMsg(chat_id, "KEY 를 등록한 사용자만 볼 수 있습니다.")
            return None
        print("msg:" + msg['text'])
    else:
        db.insertMsg(chat_id, '?')
    msgmgr.sendMsg(chat_id, " - 명령어 - \n > 멤버보기 \n > 등록 [사용자이름] \n > 알람off \n > 알람on \n > (현)재가 \n > (보)유현황")


MessageLoop(msgmgr.getBot(), handle).run_as_thread()

print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)