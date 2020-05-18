# coding: utf-8
import os
import sys
import json
import time
from pprint import pprint
sys.path.append(os.getcwd())
from wechatarticles.ReadOutfile import Reader
from wechatarticles import ArticlesAPI
import requests
import pymongo
from pathlib import Path
from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString
import re

config_path = '/home/hanani/code/personal/wechat_spider/config.json'

if __name__ == '__main__':
    config_dict = {}
    with open(config_path, "r") as config:
        config_dict = json.load(config)
    official_cookie = config_dict['config']['official_cookie']
    token = config_dict['config']['token']
    appmsg_token = config_dict['config']['appmsg_token']
    wechat_cookie = config_dict['config']['wechat_cookie']
    nickname = config_dict['config']['nickname']
    data_path = config_dict['data_path']
    print(json.dumps(config_dict,indent=4))
    time.sleep(3)
    print('读取参数配置完成!')
    print('初始化内部结构体')
    time.sleep(1)
    test = ArticlesAPI(official_cookie=official_cookie,
                       token=token,
                       appmsg_token=appmsg_token,
                       wechat_cookie=wechat_cookie)
    print('程序初始化完成')
    data_json = {
        'nickname:': nickname,
        'articles_num': test.officical.articles_nums(nickname),
        'dump_sum': 0,
    }
    markdown_path = f"{config_dict['md_path']}{nickname}"
    html_path = f"{config_dict['html_path']}{nickname}"
    gap_time = config_dict['gap_time']
    if not os.path.exists(markdown_path):
        os.makedirs(markdown_path)
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    article_nums = config_dict['article_nums']    
    data = test.continue_info(nickname=nickname,
                              begin=0,
                              md_path=markdown_path,
                              html_path=html_path,
                              gap_time=gap_time,
                              articles_nums=article_nums)
    #data = test.complete_info(nickname=nickname, begin="0")
    print(f'共抓取文章数据{len(data)}篇')
    data_json['data'] = data
    data_json['dump_sum'] = len(data)
    data_json_path = f'{data_path}/{nickname}.json'
    print('写入抓取数据文件')
    with open(data_json_path, 'w+') as j:
        j.write(json.dumps(data_json, indent=4,ensure_ascii=False))