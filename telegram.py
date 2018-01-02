import sys
import time
import telepot

import property

myProperty = property.local_property()

class message:
    token = myProperty.getTelegramToken()
    bot = None

    def __init__(self):
        self.bot = telepot.Bot(self.token)

    def getBot(self):
        return self.bot

    def sendMsg(self, chat_id, msg):
        self.bot.sendMessage(chat_id, msg)

    def sendMsgAll(self, db, msg):
        chatIdList = db.getChatIdList()
        for chatId in chatIdList:
            self.bot.sendMessage(chatId, msg)


