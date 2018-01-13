#!/usr/bin/env python
import pymysql
import json
import property


myProperty = property.local_property()

class TradingDB:

    def queryCommit(self, query, data):
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(), db='crypto_db', charset='utf8')
        cursor = db.cursor()
        cursor.execute(query, data)
        db.commit()
        db.close()

    def querySelect(self, query, data):
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(),
                             db='crypto_db', charset='utf8')
        cursor = db.cursor()
        cursor.execute(query, data)
        rows = cursor.fetchall()
        db.close()
        return rows

    def getLastPrice(self, currencyPair):
        rows = self.querySelect("select last_price from ticker where currency_pair = %s order by timestamp desc", (currencyPair))
        return rows[0][0]

    # tickData -> json 임
    def insertTick(self, currencyPair, tickData):
        insertData = (currencyPair, int(tickData['timestamp']), int(tickData['last']), int(tickData['bid']), int(tickData['ask']), int(tickData['low']), int(tickData['high']), float(tickData['volume']))
        self.queryCommit("insert into ticker (currency_pair, timestamp, last_price, bid_high_buy, ask_low_sell, low_last24h, high_last24h, volume) values (%s, %s, %s, %s, %s, %s, %s, %s)", insertData)

    def getOrder(self, currencyPair):
        rows = self.querySelect(
            "select timestamp, current_price, currency_pair, ask_json, bid_json from ask_bid where currency_pair = %s order by datetime desc",
            (currencyPair))
        keyname = ('timestamp', 'current_price', 'currency_pair', 'ask_json', 'bid_json')
        map = []
        i = 0
        for value in rows[0]:
            map.append((keyname[i], value))
            i += 1
        return dict(map)

    def insertOrder(self, currencyPair, timestamp, lastPrice, asksOrderVolume, bidsOrderVolume):
        insertData = (timestamp, lastPrice, currencyPair, str(asksOrderVolume), str(bidsOrderVolume))
        self.queryCommit("insert into ask_bid (timestamp, current_price, currency_pair, ask_json, bid_json) values (%s, %s, %s, %s, %s)", insertData)

    def getBalance(self, currency):
        rows = self.querySelect("select currency, in_krw, total, available, trade_in_use, withdrawal_in_use from balances where currency = %s order by datetime desc", (currency))
        keyname = ('currency', 'in_krw', 'total', 'available', 'trade_in_use', 'withdrawal_in_use')
        map = []
        i=0
        for value in rows[0]:
            map.append((keyname[i], value))
            i += 1
        return dict(map)

    def insertBalance(self, currency, in_krw, total, available, trade_in_use, withdrawal_in_use):
        insertData = (currency, in_krw, total, available, trade_in_use, withdrawal_in_use)
        print("insert balance - " + str(insertData))
        self.queryCommit("insert into balances (currency, in_krw, total, available, trade_in_use, withdrawal_in_use) values (%s, %s, %s, %s, %s, %s)", insertData)

    def cancelWait(self):
        self.queryCommit("update rule1_trigger_amount set state='canceled' where state='wait'", None)

    def getLastNonce(self):
        ret = 0
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(),
                             db='crypto_db', charset='utf8')
        cursor = db.cursor()
        cursor.execute("select value from setting where name = 'nonce'")
        rows = cursor.fetchall()
        if (cursor.rowcount > 0):
            ret = rows[0][0]
        updateData = (ret+1)
        cursor.execute("update setting set value=%s where name = 'nonce'", updateData)
        db.commit()
        db.close()
        return ret

    def insertMsg(self, chat_id, msg):
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(),
                             db='crypto_db', charset='utf8')
        cursor = db.cursor()
        insertData = (chat_id, msg)
        cursor.execute("insert into scribe (memid, membername) values (%s, %s)", insertData)
        db.commit()
        db.close()

    def getMemberList(self):
        memberNameList = []
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(),
                             db='crypto_db', charset='utf8')
        cursor = db.cursor()
        cursor.execute("select membername from scribe", ())
        rows = cursor.fetchall()
        for row in rows:
            membername = row[0]
            memberNameList.append(membername)
        db.close()
        return memberNameList

    def getChatIdList(self):
        chatIdList = []
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(),
                             db='crypto_db', charset='utf8')
        cursor = db.cursor()
        cursor.execute("select memid from scribe where sliencemode!=1", ())
        rows = cursor.fetchall()
        for row in rows:
            chatId = row[0]
            chatIdList.append(chatId)
        db.close()
        return chatIdList

    def enableSlientMode(self, chatId):
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(),
                             db='crypto_db', charset='utf8')
        cursor = db.cursor()
        updateData = (chatId)
        cursor.execute("update scribe set sliencemode=1 where memid=%s", updateData)
        db.commit()
        db.close()

    def disableSlientMode(self, chatId):
        db = pymysql.connect(host='localhost', port=3306, user='tradingbot', passwd=myProperty.getMariaDbPw(),
                             db='crypto_db', charset='utf8')
        cursor = db.cursor()
        updateData = (chatId)
        cursor.execute("update scribe set sliencemode=0 where memid=%s", updateData)
        db.commit()
        db.close()
