#!/usr/bin/env python

import json
import collect
import telegram
import coin
import property
import korbit_status
import market_calc

myProperty = property.local_property()

class korbitRule1:

    def isMatched(self, db, currencyPair):
        market_calc.getSellPower(db, currencyPair)
        ## TODO 기존 룰 없애고 새로운 룰 넣기 
        return False

    def sellCoin(self, db, api):
        # TODO 판매한 뒤 balance table 갱신해주기
        korbit_status.updateLastBalance(api, db)

    def buyCoin(self, msg, db, api, currencyPair, triggerAmount):
        coinInfo = coin.coinInfo()
        resp = api.buy(coinInfo.fitUnit(currencyPair, triggerAmount), coinInfo.getBuyingAmount(currencyPair), currencyPair)
        korbit_status.updateLastBalance(api, db)
        if (resp.text != ""):
            jsonObj = json.loads(resp.text)
            if (jsonObj['status'] == 'success'):
                db.updateTriggerAmount(currencyPair, jsonObj['orderId'])
        msg.sendMsg(myProperty.getMyChatId(), "[룰1] 구입 결과! " + str(coinInfo.fitUnit(currencyPair, triggerAmount)) + ", 결과:" + resp.text)
        msg.sendMsg(myProperty.getMyChatId(), "[룰1] 구입 결과! " + str(coinInfo.fitUnit(currencyPair, triggerAmount)) + ", header:" + str(resp.headers))

    def sendBuyMsg(self, msg, db, currencyPair, triggerAmount, lastPrice):
        msg.sendMsgAll(db, "[룰1] 구입해서 적당한 시점에 파세요! 구입할것:" + currencyPair + ", 기준가격:" + str(triggerAmount) + ", 현재가격:" + str(lastPrice))

    def checkRule(self, msg, db, api, currencyPair):
        if (self.isMatched(db, currencyPair)):
            #self.buyCoin(msg, db, api, currencyPair, triggerAmount)
            self.sendBuyMsg(msg, db, currencyPair, 0, 0)



