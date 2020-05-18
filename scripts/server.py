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


@app.route('/')
def index():
    return


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
    if args.open_in_browser:
        webbrowser.open_new_tab(f'http://127.0.0.1:{PORT}/')
    app.run(
        host='0.0.0.0',
        debug=args.debug,
        port=PORT,
    )
