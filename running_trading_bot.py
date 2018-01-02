#-*- coding:utf-8 -*-
#!/usr/bin/env python


from pytz import utc

#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

import collect
import korbit
import korbit_rule
import telegram
import coin
import property

myProperty = property.local_property()

sched = BlockingScheduler()
coinInfo = coin.coinInfo()
currency_pair_list = coinInfo.getCurrentPairList()
db = collect.TradingDB()

api = korbit.KorbitApi("", "", db)
api.requestAccessToken(myProperty.getMyKorbitPw())

### rules
rule1 = korbit_rule.korbitRule1()

### user info
print (api.getUserInfo())


@sched.scheduled_job('interval', minutes=20)
def refreshTokens():
    api.refreshAccessToken()
    print("at = \"" + api.getAccessToken() + "\"")
    print("rt = \"" + api.getRefreshToken() + "\"")

@sched.scheduled_job('interval', seconds=180)
def mainProcess():
    msg = telegram.message()
    # 각 코인 마다 api 호출해서 가격 얻어오고 db 에 저장하고, 룰 매칭되는지 여부 확인해서 룰 매칭되면 구입!
    for i, currencyPair in enumerate(currency_pair_list):
        rule1.checkRule(msg, db, api, currencyPair)

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=11, minute=50)
def alertSell():
    msg = telegram.message()
    msg.sendMsg(myProperty.getMyChatId(), "[룰1] 구입했다면 파세요! (매일11시50분에 항상 오는 메시지)")

mainProcess()

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