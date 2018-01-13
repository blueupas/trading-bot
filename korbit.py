#!/usr/bin/env python
import requests
import json
import property

myProperty = property.local_property()

class KorbitApi:
    key = myProperty.getKorbitApiKey()
    secret = myProperty.getKorbitApiSecret()
    accessToken = ""
    refreshToken = ""
    db = None

    def __init__(self, accessToken, refreshToken, db):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.db = db

    def getNonce(self):
        nonce = self.db.getLastNonce()
        return nonce

    def getRefreshToken(self):
        return self.refreshToken

    def getAccessToken(self):
        return self.accessToken

    def requestAccessToken(self, passwd):
        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {'client_id': self.key, 'client_secret': self.secret, 'username': myProperty.getKorbitUserId(), 'password': passwd,
                'grant_type': 'password'}
        resp = json.loads(requests.post(url, data=data).text)
        self.accessToken = resp['access_token']
        self.refreshToken = resp['refresh_token']

    def refreshAccessToken(self):
        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {'client_id': self.key, 'client_secret': self.secret, 'refresh_token': self.refreshToken,
                'grant_type': 'refresh_token'}
        resp = requests.post(url, data=data).text
        print ("refresh at - resp : " + resp)
        jsonData = json.loads(resp)
        self.accessToken = jsonData['access_token']
        self.refreshToken = jsonData['refresh_token']

    def getTick(self, currency):
        url = "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=" + currency
        resp = requests.get(url).text
        return resp

    def getBalance(self):
        url = "https://api.korbit.co.kr/v1/user/balances"
        headers = {'Authorization': 'Bearer ' + self.accessToken}
        return requests.get(url, headers=headers).text


    def getUserInfo(self):
        url = "https://api.korbit.co.kr/v1/user/info"
        headers = {'Authorization': 'Bearer ' + self.accessToken}
        return requests.get(url, headers=headers).text

    def buy(self, coinPrice, coinAmount, currencyPair):
        url = "https://api.korbit.co.kr/v1/user/orders/buy"
        headers = {'Authorization': 'Bearer ' + self.accessToken}
        data = {'currency_pair': currencyPair, 'type': 'limit', 'price': coinPrice,
                'coin_amount': coinAmount, 'nonce':self.getNonce()}
        return requests.post(url, data=data, headers=headers)


