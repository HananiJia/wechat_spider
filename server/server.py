import os
import re
import json
import time
import base64
import argparse
import webbrowser
import sys
import markdown
import codecs
from pydash import py_
from collections import defaultdict
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)
PORT = 8080
RES_PATH = ''
PWD = os.path.abspath(os.path.dirname(__file__))
ARTICLES_PATH = '/home/hanani/code/personal/wechat_spider/articles_html'
NOW_ARTICLES = []

@app.route('/')
def send_files():
    print(NOW_ARTICLES)
    if len(NOW_ARTICLES)!=0 :
        print("NOW",NOW_ARTICLES[-1])
        articles_name = NOW_ARTICLES[-1]
        NOW_ARTICLES.clear()
        return render_template(articles_name) 
    else:
        return render_template('index.html') 

@app.route('/index')
def index_html():
    return render_template('index.html') 

@app.route('/json_object/<query_type>')
def query_jsonObject(query_type):
    artles_dir = os.listdir(ARTICLES_PATH)
    content_dict = {}
    for a_dir in artles_dir:
        article_path = f'{ARTICLES_PATH}/{a_dir}'
        content_dict[a_dir] = os.listdir(article_path)
    #print(json.dumps(content_dict, indent=4))
    return jsonify(content_dict)

@app.route('/res/<file_name>', methods=['GET'])
def load_res(file_name):
    file_path = f'{RES_PATH}/{file_name}'
    print("file_path:", file_path)
    if not os.path.exists(file_path):
        raise ValueError(f'invalid file path {file_path}')
    with open(file_path) as f:
        file = f.read()
    return Response(file)

@app.route('/articles/<name>')
def load_articles(name):
    for artles_dir in os.listdir(ARTICLES_PATH):
        print('artles_dir:',artles_dir)
        path = f'{ARTICLES_PATH}/{artles_dir}'
        print("path:",path)
        for artles in os.listdir(path):
            if artles == name:
                file_path = f'{artles}'
                NOW_ARTICLES.append(file_path)
                print('NOEW',NOW_ARTICLES)
                return Response(file_path)       

if __name__ == '__main__':
    prog = 'python -m articles_server'
    description = ('articles server')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '--port',
        type=int,
        help='port to open',
    )
    parser.add_argument(
        '--open-in-browser',
        default=True,
        help='open in browser, default: True',
    )
    parser.add_argument(
        '--debug',
        default=True,
        help='debug flask app? default: True',
    )
    args = parser.parse_args()
    if args.port:
        PORT = args.port
    RES_PATH = f'{PWD}/res'
    if args.open_in_browser:
        webbrowser.open_new_tab(f'http://127.0.0.1:{PORT}/')
    app.run(
        host='0.0.0.0',
        debug=args.debug,
        port=PORT,
    )
