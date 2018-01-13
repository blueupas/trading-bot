#-*- coding:utf-8 -*-
#!/usr/bin/env python


import ast

# 50 이상일땐 순간적으로 가격 떨어질 가능성 높음.
# 0.02 이하일땐 순간적으로 가격 오를 가능성 높음
def getSellPower(db, currencyPair):
    sellPower = 0
    buyPower = 0

    data = db.getOrder(currencyPair)
    currentPrice = data['current_price']
    asksdata = ast.literal_eval(data['ask_json'])

    for i in range(0, 10):
        price = asksdata[i][0]
        amount = asksdata[i][1]
        if (price - currentPrice > 0):
            sellPower += (1 / (price - currentPrice) * amount) * currentPrice

    bidsdata = ast.literal_eval(data['bid_json'])
    for i in range(0, 10):
        price = bidsdata[i][0]
        amount = bidsdata[i][1]
        if (currentPrice - price > 0):
            buyPower += (1 / (currentPrice - price) * amount) * currentPrice

    print ("pair : " + currencyPair + ", sell/buy ratio : " + format(sellPower / buyPower, ">-02.2f") + ", current price : " + str(currentPrice) + ", sell power : " + str(sellPower) + ", buyPower : " + str(buyPower))
    return sellPower / buyPower