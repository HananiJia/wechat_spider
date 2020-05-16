# coding: utf-8

from .ArticlesUrls import ArticlesUrls
from .ArticlesInfo import ArticlesInfo
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString
import re
import json

class ArticlesAPI(object):
    """
    整合ArticlesInfo和ArticlesInfo, 方便调用
    """

    def __init__(self,
                 username=None,
                 password=None,
                 official_cookie=None,
                 token=None,
                 appmsg_token=None,
                 wechat_cookie=None,
                 outfile=None):
        """
        初始化参数
        Parameters
        ----------
        username: str
            用户账号
        password: str
            用户密码
        official_cookie : str
            登录微信公众号平台之后获取的cookie
        token : str
            登录微信公众号平台之后获取的token
        wechat_cookie: str
            点开微信公众号文章抓包工具获取的cookie
        appmsg_token: str
            点开微信公众号文章抓包工具获取的appmsg_token

        Returns
        -------
            None
        """
        # 两种登录方式, 扫码登录和手动输入登录
        if (token != None) and (official_cookie != None):
            self.officical = ArticlesUrls(cookie=official_cookie, token=token)
        elif (username != None) and (password != None):
            self.officical = ArticlesUrls(username=username, password=password)
        else:
            raise SystemError("please check your paramse")

        # 支持两种方式， mitmproxy自动获取参数和手动获取参数
        if (appmsg_token == None) and (wechat_cookie == None) and (outfile !=
                                                                   None):
            from .ReadOutfile import Reader
            reader = Reader()
            reader.contral(outfile)
            self.appmsg_token, self.cookie = reader.request(outfile)
        elif (appmsg_token != None) and (wechat_cookie != None):
            self.appmsg_token, self.cookie = appmsg_token, wechat_cookie
        else:
            raise SystemError("please check your params")

        self.wechat = ArticlesInfo(self.appmsg_token, self.cookie)

    def download_img(self,url, name,images_path):
        response = requests.get(url)
        img = response.content
        imgpath = images_path.format(name)
        with open(imgpath, 'wb') as f:
            f.write(img)

    def parse_section(self,sections,str_lst,parse_lst):
        content = ''
        global section
        for section in sections:
            if section.name == None:
                content += section
            elif section.name == 'section':
                section_str = str(section)
                for img in section.find_all('img'):
                    section_str = section_str.replace(
                        str(img), '\n\n![img]({})\n\n'.format(img['data-src']))
                content += section_str
                content += section_str
            elif section.name in str_lst:
                content += str(section)
            elif section.name == 'p':
                tmp = ''.join(str(content) for content in section.contents)
                content += tmp
            elif section.name in parse_lst:
                content += self.parse_section(section.contents,str_lst,parse_lst)
            elif section.name == 'img':
                url = section['data-src']
                """
                name = url.split('/')[-2] + '.' + url.split('/')[-1].split('=')[1]
                download_img(url, name)
                content += '![{}]({})\n'.format(name, path.format(name))
                """
                content += '![img]({})\n'.format(url)
                # content += str(section)
            elif section.name == 'br':
                content += '</br>'
            elif section.name == 'strong':
                content += '<strong>{}</strong>'.format(section.string)
            elif section.name == 'iframe':
                content += 'iframe\n'
            else:
                print(section.name)
                # print(section)

        return content
    
    def loading_url(self,url_lst,articles_path): 
        print("link:",url_lst) 
        parse_lst = ['article', 'a']
        str_lst = ['hr', 'span', 'ul']   
        for url in url_lst[::-1]:
            html = requests.get(url)
            soup = bs(html.text, 'lxml')
            # try:
            body = soup.find(class_="rich_media_area_primary_inner")
            titles = body.find(class_="rich_media_title")
            if not titles:
                continue
            title = titles.text.strip()
            author = body.find(
                class_="rich_media_meta rich_media_meta_nickname").a.text.strip()
            content_p = body.find(class_="rich_media_content")
            content_lst = content_p.contents

            content = ''

            for item in content_lst:
                if item.name == None:
                    content += item
                elif item.name == 'section':
                    section_str = str(item)
                    for img in item.find_all('img'):
                        section_str = section_str.replace(
                            str(img), '\n\n![img]({})\n\n'.format(img['data-src']))
                    content += section_str
                elif item.name in str_lst:
                    content += str(item)
                elif item.name == 'p':
                    tmp = ''.join(str(content) for content in item.contents)
                    content += tmp
                elif item.name in parse_lst:
                    content += self.parse_section(item.contents,str_lst,parse_lst)
                elif item.name == 'br':
                    content += '</br>'
                elif item.name == 'strong':
                    content += '<strong>{}</strong>'.format(item.string)
                elif item.name == 'iframe':
                    content += 'iframe\n'
                elif section.name == 'img':
                    url = section['data-src']
                    content += '![img]({})\n'.format(url)
                else:
                    print(item.name)
            md_path = articles_path.format(f'{title}.md')
            print(f'loading {title}')        
            with open(md_path, 'w+', encoding='utf-8') as f:
                f.write('## ' + title + '\n')
                f.write(author + '\n')
                f.write(content + '\n')
                f.write('<div style="page-break-after: always;"></div>\n')
                # except:
                #     print(url)
                #     pass


    def complete_info(self, nickname, begin=0, count=5):
        """
        获取公众号的抓取的文章文章信息
        Parameters
        ----------
        nickname: str
            公众号名称
        begin: str or int
            起始爬取的页数
        count: str or int
            每次爬取的数量，1-5

        Returns
        -------
        list:
            由每个文章信息构成的数组
            [
              {
                'aid': '2650949647_1',
                'appmsgid': 2650949647,
                'comments': 文章评论信息
                    {
                        "base_resp": {
                            "errmsg": "ok", 
                            "ret": 0
                        }, 
                        "elected_comment": [
                            {
                                "content": 用户评论文字, 
                                "content_id": "6846263421277569047", 
                                "create_time": 1520098511, 
                                "id": 3, 
                                "is_from_friend": 0, 
                                "is_from_me": 0, 
                                "is_top": 0, 是否被置顶
                                "like_id": 10001, 
                                "like_num": 3, 
                                "like_status": 0, 
                                "logo_url": "http://wx.qlogo.cn/mmhead/OibRNdtlJdkFLMHYLMR92Lvq0PicDpJpbnaicP3Z6kVcCicLPVjCWbAA9w/132", 
                                "my_id": 23, 
                                "nick_name": 评论用户的名字, 
                                "reply": {
                                    "reply_list": [ ]
                                }
                            }
                        ], 
                        "elected_comment_total_cnt": 3, 评论总数
                        "enabled": 1, 
                        "friend_comment": [ ], 
                        "is_fans": 1, 
                        "logo_url": "http://wx.qlogo.cn/mmhead/Q3auHgzwzM6GAic0FAHOu9Gtv5lEu5kUqO6y6EjEFjAhuhUNIS7Y2AQ/132", 
                        "my_comment": [ ], 
                        "nick_name": 当前用户名, 
                        "only_fans_can_comment": false
                    }, 
                'cover': 封面的url'digest': 文章摘要,
                'itemidx': 1,
                'like_num': 18, 文章点赞数
                'link': 文章的url,
                'read_num': 610, 文章阅读数
                'title': 文章标题,
                'update_time': 更新文章的时间戳
              },
            ]
        如果list为空则说明没有相关文章
        """
        # 获取文章数据
        artiacle_data = self.officical.articles(
            nickname, begin=str(begin), count=str(count))

        # 提取每个文章的url，获取文章的点赞、阅读、评论信息，并加入到原来的json中
        print("artiacle_data:",artiacle_data)
        for data in artiacle_data:
            article_url = data["link"]
            comments = self.wechat.comments(article_url)
            #read_like_nums = self.wechat.read_like_nums(article_url)
            data["comments"] = comments
            data["read_num"], data["like_num"] = 0,0

        return artiacle_data

    def __extract_info(self, articles_data):
        # 提取每个文章的url，获取文章的点赞、阅读、评论信息，并加入到原来的json中
        for data in articles_data:
            article_url = data["link"]
            comments = self.wechat.comments(article_url)
            #read_like_nums = self.wechat.read_like_nums(article_url)
            data["comments"] = comments
            data["read_num"], data["like_num"] = 0 , 0

        return articles_data

    def continue_info(self, nickname, begin = 0,articles_path=''):
        """
        自动获取公众号的抓取的文章文章信息，直到爬取失败为止
        Parameters
        ----------
        nickname: str
            公众号名称
        begin: str or int
            起始爬取的页数

        Returns
        -------
        list:
            由每个文章信息构成的数组
            [
              {
                'aid': '2650949647_1',
                'appmsgid': 2650949647,
                'comments': 文章评论信息
                    {
                        "base_resp": {
                            "errmsg": "ok", 
                            "ret": 0
                        }, 
                        "elected_comment": [
                            {
                                "content": 用户评论文字, 
                                "content_id": "6846263421277569047", 
                                "create_time": 1520098511, 
                                "id": 3, 
                                "is_from_friend": 0, 
                                "is_from_me": 0, 
                                "is_top": 0, 是否被置顶
                                "like_id": 10001, 
                                "like_num": 3, 
                                "like_status": 0, 
                                "logo_url": "http://wx.qlogo.cn/mmhead/OibRNdtlJdkFLMHYLMR92Lvq0PicDpJpbnaicP3Z6kVcCicLPVjCWbAA9w/132", 
                                "my_id": 23, 
                                "nick_name": 评论用户的名字, 
                                "reply": {
                                    "reply_list": [ ]
                                }
                            }
                        ], 
                        "elected_comment_total_cnt": 3, 评论总数
                        "enabled": 1, 
                        "friend_comment": [ ], 
                        "is_fans": 1, 
                        "logo_url": "http://wx.qlogo.cn/mmhead/Q3auHgzwzM6GAic0FAHOu9Gtv5lEu5kUqO6y6EjEFjAhuhUNIS7Y2AQ/132", 
                        "my_comment": [ ], 
                        "nick_name": 当前用户名, 
                        "only_fans_can_comment": false
                    }, 
                'cover': 封面的url'digest': 文章摘要,
                'itemidx': 1,
                'like_num': 18, 文章点赞数
                'link': 文章的url,
                'read_num': 610, 文章阅读数
                'title': 文章标题,
                'update_time': 更新文章的时间戳
              },
            ]
        如果list为空则说明没有相关文章
        """
        artiacle_datas = []
        count = 5
        while True:
            # 获取文章数据
            print(f'正在抓取第{begin}篇到第{begin + count}篇文章数据')
            artiacle_data = self.officical.articles(nickname, begin=str(begin), count=str(count))
            print("article_data:",len(artiacle_data))
            for artiacle in artiacle_data:
                url_lst = [artiacle['link']]
                self.loading_url(url_lst,articles_path)
            artiacle_datas.extend(artiacle_data)
            begin += count

        flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
        print("第{}篇文章爬取失败，请过段时间再次尝试或换个帐号继续爬取".format(begin))
        return self.__extract_info(flatten(artiacle_datas))
