#!/usr/bin/env python

import json
import collect
import telegram
import coin
import property

myProperty = property.local_property()

class korbitRule1:

    def saveTriggerAmount(self, db, currency_pair, amount):
        db.insertTriggerAmount(currency_pair, amount)

    def getTriggerAmount(self, db, currency_pair):
        return db.getTriggerAmount(currency_pair)

    def buyCoin(self, msg, db, api, currencyPair, triggerAmount):
        coinInfo = coin.coinInfo()
        resp = api.buy(coinInfo.fitUnit(currencyPair, triggerAmount), coinInfo.getBuyingAmount(currencyPair),
                       currencyPair)
        if (resp.text != ""):
            jsonObj = json.loads(resp.text)
            if (jsonObj['status'] == 'success'):
                db.updateTriggerAmount(currencyPair, jsonObj['orderId'])
        msg.sendMsg(myProperty.getMyChatId(), "[룰1] 구입 결과! " + str(coinInfo.fitUnit(currencyPair, triggerAmount)) + ", 결과:" + resp.text)
        msg.sendMsg(myProperty.getMyChatId(), "[룰1] 구입 결과! " + str(coinInfo.fitUnit(currencyPair, triggerAmount)) + ", header:" + str(resp.headers))

    def sendBuyMsg(self, msg, db, currencyPair, triggerAmount, lastPrice):
        msg.sendMsgAll(db, "[룰1] 구입해서 오전에 파세요! 구입할것:" + currencyPair + ", 기준가격:" + str(triggerAmount) + ", 현재가격:" + str(lastPrice))

    def checkRule(self, msg, db, api, currencyPair):
        lastPrice = db.getLastPrice(currencyPair)
        triggerAmount = self.getTriggerAmount(db, currencyPair)
        if (triggerAmount != 0 and lastPrice > triggerAmount):
            print("matched! " + currencyPair + ", threashold:" + str(triggerAmount) + ", current:" + str(lastPrice))
            self.buyCoin(msg, db, api, currencyPair, triggerAmount)
            self.sendBuyMsg(msg, db, currencyPair, triggerAmount, lastPrice)
        else:
            print ("not matched! " + currencyPair + ", threashold:" + str(triggerAmount) + ", current:" + str(lastPrice))



