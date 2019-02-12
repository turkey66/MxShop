# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/12/23 17:35'

import json

import requests


class YunPian:

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://wwwwwwwwww.cccc.comssss/cc"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "llllllllll{code}".format(code)
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == "__main__":
    yun_pian = YunPian("asdasda1123123asdasd")
    yun_pian.send_sms("2015","13421885566")