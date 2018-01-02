#!/usr/bin/env python



class coinInfo:
    currency_pair_list = ["btc_krw", "eth_krw", "xrp_krw", "bch_krw"]

    def getCurrentPairList(self):
        return self.currency_pair_list

    def fitUnit(self, currencyPair, amount):
        if (currencyPair == self.currency_pair_list[0]):
            return int (round(amount / 500)) * 500
        if (currencyPair == self.currency_pair_list[1]):
            return int (round(amount / 50)) * 50
        if (currencyPair == self.currency_pair_list[2]):
            return int (round(amount / 10)) * 10
        if (currencyPair == self.currency_pair_list[3]):
            return int (round(amount / 500)) * 500
        return 0

    def getBuyingAmount(self, currencyPair):
        if (currencyPair == self.currency_pair_list[0]):
            return 0.005
        if (currencyPair == self.currency_pair_list[1]):
            return 0.2
        if (currencyPair == self.currency_pair_list[2]):
            return 50
        if (currencyPair == self.currency_pair_list[3]):
            return 0.02
        return 0