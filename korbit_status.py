#-*- coding:utf-8 -*-
#!/usr/bin/env python

import json
import coin


coinInfo = coin.coinInfo()
currency_pair_list = coinInfo.getCurrentPairList()

def convertKrw(db, currency, amount):
    if currency == 'krw':
        return amount
    currencyPair = currency + "_krw"
    price = db.getLastPrice(currencyPair)
    return amount * price


# 끝나지 않은 order 가 있는 경우 balance 가 변동될 수 있는 상태라서 완료가 될 때까지 trading bot 에서 balance 를 지속적으로 갱신해줌.
def hasOrderNotFinished(db):
    for currency in ['krw', 'btc', 'bch', 'eth', 'xrp']:
        data = db.getBalance(currency)
        if (float(data['trade_in_use']) > 0):
            return True
    return False

def updateLastBalance(api, db):
    resp = api.getBalance()
    jsonData = json.loads(resp)
    for currency in ['krw', 'btc', 'bch', 'eth', 'xrp']:
        jsonData[currency]['total'] = float(jsonData[currency]['available']) + float(jsonData[currency]['trade_in_use'])
        jsonData[currency]['in_krw'] = convertKrw(db, currency, jsonData[currency]['total'])
        db.insertBalance(currency, jsonData[currency]['in_krw'], jsonData[currency]['total'], jsonData[currency]['available'], jsonData[currency]['trade_in_use'], jsonData[currency]['withdrawal_in_use'])


def getMsgStrForBalance(db):
    msg = ""
    for currency in ['krw', 'btc', 'bch', 'eth', 'xrp']:
        data = db.getBalance(currency)
        msg += data['currency'] + " : " + format(data['in_krw'], "_>-012,.0f")
        if currency == 'krw':
            msg += "\n"
        else :
            msg +=  "  (=" + format(data['total'], "_>-012,.6f") + ")" + "\n"
    return msg


def getMsgStrForLastPrice(db):
    msg = ""
    for i, currencyPair in enumerate(currency_pair_list):
        lastPrice = db.getLastPrice(currencyPair)
        msg += currencyPair + " : " + format(lastPrice, "_>-012,.0f") + "\n"
    return msg