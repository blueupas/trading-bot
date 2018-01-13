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

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=21, minute=00)
def saveTriggerAmount():
    # 특정 가격을 넘어가면 구입할 수 있게 룰에 따라 특정 가격을 저장해줌.
    db.cancelWait()
    for i, currencyPair in enumerate(currency_pair_list):
        resp = api.getTick(currencyPair)
        jsonObj = json.loads(resp)
        amount = int(jsonObj['last']) + (int(jsonObj['high']) - int(jsonObj['low'])) * 0.5
        rule1.saveTriggerAmount(db, currencyPair, amount)


@sched.scheduled_job('interval', seconds=60)
def collectTick():
    # 각 코인 마다 api 호출해서 가격 얻어오고 db 에 저장
    for i, currencyPair in enumerate(currency_pair_list):
        resp = api.getTick(currencyPair)
        print("resp:" + resp)
        tickData = json.loads(resp)
        db.insertTick(currencyPair, tickData)



collectTick()

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