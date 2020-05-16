# coding: utf-8
import os
import sys
import json
from pprint import pprint
sys.path.append(os.getcwd())
from wechatarticles.ReadOutfile import Reader
from wechatarticles import ArticlesAPI
import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString
import re

config_path = '/home/hanani/code/personal/wechat_spider/config.json'

if __name__ == '__main__':
    config_dict = {}
    with open(config_path,"r") as config:
        config_dict = json.load(config)
    official_cookie = config_dict['config']['official_cookie']
    token = config_dict['config']['token']
    appmsg_token = config_dict['config']['appmsg_token']
    wechat_cookie = config_dict['config']['wechat_cookie']
    nickname = config_dict['config']['nickname']

    # 手动输入所有参数
    test = ArticlesAPI(
        official_cookie=official_cookie,
        token=token,
        appmsg_token=appmsg_token,
        wechat_cookie=wechat_cookie)

    data = test.continue_info(nickname=nickname,begin=0,articles_path= config_dict['articles_path'])
    #data = test.complete_info(nickname=nickname, begin="0")
    print(f'共抓取文章数据{len(data)}篇')