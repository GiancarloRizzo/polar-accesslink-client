#!/usr/bin/env python
from __future__ import print_function

import requests
from flask import Flask, request, redirect
from config import BASE_URL, REDIRECT_URL, PORT

from utils import load_config, save_config
from accesslink import AccessLink

CONFIG_FILENAME = "config.yml"

config = load_config('credentials.yml')
client_id=config['client_id']
client_secret=config['client_secret']

accesslink = AccessLink(client_id,
                        client_secret,
                        redirect_url=REDIRECT_URL)


app = Flask(__name__)


def get_authorization_code():
    return request.args.get('code')

def get_access():
    code = get_authorization_code()
    token_response = accesslink.get_access_token(code)
    config["user_id"] = token_response["x_user_id"]
    config["access_token"] = token_response["access_token"]
    save_config(config, CONFIG_FILENAME)
    
@app.route("/")
def authorize():
    return redirect(accesslink.authorization_url)


@app.route('/oauth2_callback')
def callback():
    get_access()
    return redirect('visualizer')

@app.route('/visualisizer')
def rendering():

    return

print("Navigate to {}/ for authorization.\n".format(BASE_URL))
app.run(host='localhost', port=PORT)


