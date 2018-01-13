# trading-bot

1. 아래의 형태로 property.py 생성 후 
```

class local_property:

    def getKorbitUserId(self):
        return '코빗 아이디'
    def getMyKorbitPw(self):
        return "코빗 비번"
    def getKorbitApiKey(self):
        return "코빗 API KEY"
    def getKorbitApiSecret(self):
        return "코빗 API SECRET"

    def getMyChatId(self):
        return 텔레그램 chat id
    def getTelegramToken(self):
        return "텔레그램 토큰"

    def getMariaDbPw(self):
        return 'DB 비번'

```

2. running- 으로 시작하는 파일들을 실행해두면 됨.
