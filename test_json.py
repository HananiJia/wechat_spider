import os
import sys
import json
import time


if __name__ == '__main__':
    json_data = {}
    path = '/home/hanani/code/personal/wechat_spider/data/ding.json'
    with open(path, "r") as data:
        json_data = json.load(data)
    articles = json_data   
    yiyue_article = 0
    yiyue_like = 0
    yiyue_read =0
    yiyue_comment = 0
    yiyue_wan = 0
    shier_artice = 0
    shier_like = 0
    shier_read = 0
    shier_comment = 0
    shier_wan = 0
    eryue_article = 0
    eryue_like = 0
    eryue_read = 0 
    eryue_wan = 0
    eryue_comment = 0
    title_dict ={}
    for article in articles:
        if 'read_num' not in article:
            continue
        title = article['title']
        if title not in title_dict.keys():
            title_dict[title] = 0
        else:
            continue    
        time = article['update_time']
        if time >= 1575129600 and time <1577808000:
            yiyue_article += 1
            if int(article['read_num']) == 100001:
                yiyue_wan += 1
            yiyue_read += int(article['read_num'])
            yiyue_like += int(article['like_num'])
            yiyue_comment += len(article['comments']['elected_comment'])
        elif time >=1577808000 and time < 1580486400:
            eryue_article += 1
            if int(article['read_num']) == 100001:
                eryue_wan += 1
            eryue_read += int(article['read_num'])
            eryue_like += int(article['like_num'])
            eryue_comment += len(article['comments']['elected_comment'])
        elif time >= 1580486400 and time <1582905600:
            shier_artice += 1
            if int(article['read_num']) == 100001:
                shier_wan += 1
            shier_read += int(article['read_num'])
            shier_like += int(article['like_num'])
            shier_comment += len(article['comments']['elected_comment'])
        else:
            pass
    print(f'十二月共发表文章:{yiyue_article}篇,评论{yiyue_comment}条,平均{yiyue_comment/yiyue_article},阅读人数{yiyue_read},平均{yiyue_read/yiyue_article},在看人数{yiyue_like},平均{yiyue_like/yiyue_article},超过十万的有{yiyue_wan}篇')   
    print(f'一月共发表文章:{eryue_article}篇,评论{eryue_comment}条,平均{eryue_comment/eryue_article},阅读人数{eryue_read},平均{eryue_read/eryue_article},在看人数{eryue_like},平均{eryue_like/eryue_article},超过十万的有{eryue_wan}篇')     
    print(f'二月共发表文章:{shier_artice}篇,评论{shier_comment}条,平均{shier_comment/shier_artice},阅读人数{shier_read},平均{shier_read/shier_artice},在看人数{shier_like},平均{shier_like/shier_artice},超过十万的有{shier_wan}篇')    
