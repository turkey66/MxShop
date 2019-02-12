# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/1/13 11:05'

import requests

def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_url = "http://192.168.1.100:8000/complete/weibo/"
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={re_url}".format(client_id='714666249', re_url=redirect_url)

    print(auth_url)
    # http://192.168.1.100:8000/complete/weibo/?code=bf6c78d9e135ff83f17a45d54ed7fcbc
def get_access_token(code="bf6c78d9e135ff83f17a45d54ed7fcbc"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    res_dict = requests.post(access_token_url, data={
        "client_id":'714666249',
        "client_secret": "74394e2bcc0375e131910ea2a50f13fa",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://192.168.1.100:8000/complete/weibo/"
    })
    print(print(res_dict.json()))
    # {'access_token': '2.00Acx2vB0z1f3m2b06605ccbRtYqLD', 'remind_in': '157679999', 'expires_in': 157679999, 'uid': '1763618024', 'isRealName': 'true'}

def get_user_info(access_token="", uid=""):
    user_info_url = "https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}".format(access_token=access_token, uid=uid)
    print(user_info_url)

if __name__ == "__main__":
    get_auth_url()
    get_access_token(code="bf6c78d9e135ff83f17a45d54ed7fcbc")
    get_user_info(access_token="2.00Acx2vB0z1f3m2b06605ccbRtYqLD", uid="1763618024")