#-*- coding:utf-8 -*-
#!/usr/bin/env python


from pytz import utc

#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

import json
import collect
import korbit
import korbit_rule
import coin

sched = BlockingScheduler()
coinInfo = coin.coinInfo()
currency_pair_list = coinInfo.getCurrentPairList()

db = collect.TradingDB()
api = korbit.KorbitApi('', '', db)
rule1 = korbit_rule.korbitRule1()


@sched.scheduled_job('interval', seconds=60)
def collectTick():
    # 각 코인 마다 api 호출해서 가격 얻어오고 db 에 저장
    for i, currencyPair in enumerate(currency_pair_list):
        resp = api.getTick(currencyPair)
        print("tick resp:" + resp)
        tickData = json.loads(resp)
        db.insertTick(currencyPair, tickData)


@sched.scheduled_job('interval', seconds=60)
def collectOrderBook():
    # 각 코인 마다 api 호출해서 주문 쌓여있는거 얻어오고 db 에 저장
    for i, currencyPair in enumerate(currency_pair_list):
        resp = api.getOrderBook(currencyPair)
        print("order resp:" + resp)
        orderData = json.loads(resp)
        timestamp = orderData['timestamp']
        lastPrice = db.getLastPrice(currencyPair)
        # 파는 사람 볼륨
        asksdata = orderData['asks']
        asksOrderVolume = []
        for row in asksdata:
            asksOrderVolume.append((int(row[0]), float(row[1])))
        asksOrderVolume = sorted(asksOrderVolume, key=lambda order: order[0])
        # 사려는 사람 볼륨
        bidsdata = orderData['bids']
        bidsOrderVolume = []
        for row in bidsdata:
            bidsOrderVolume.append((int(row[0]), float(row[1])))
        bidsOrderVolume = sorted(bidsOrderVolume, key=lambda order: order[0], reverse=True)

        print(str(asksOrderVolume))
        db.insertOrder(currencyPair, timestamp, lastPrice, asksOrderVolume, bidsOrderVolume)


collectTick()
collectOrderBook()


executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

sched.configure(executors=executors, job_defaults=job_defaults, timezone=utc) # jobstores=jobstores,
sched.start()