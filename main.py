import logging
import requests
from flask import Flask, request, jsonify, send_file, render_template
import itchat
import itchat.content
from itchat.config import (DINGTALK_APP_KEY, DINGTALK_APP_SECRET, 
                           LOG_LEVEL)
import farpush
import socket
import json
import _thread
import os
import datetime

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# store messages
messages = []

def get_access_token():
    url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    headers = {"Content-Type": "application/json"}
    data = {"appKey": DINGTALK_APP_KEY, "appSecret": DINGTALK_APP_SECRET}
    logger.debug(f"Sending request to {url} with data: {json.dumps(data)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        logger.info("Successfully obtained access token")
        return response_data.get("accessToken")
    else:
        logger.error(f"Failed to get access token: {response.status_code} {response.text}")
        return None

@app.route("/send", methods=['POST'])
def received():
    data = request.json
    username = data['username']
    nametype = data['type']
    content = data['content']
    logger.info(f"Received message from {username}: {content}")
    if nametype == '0':
        send4nick(username, content)
    else:
        send(username, content)
    return 'ok'

@app.route("/getuser", methods=['POST'])
def getuser():
    data = request.json
    username = data['username']
    logger.info(f"Fetching user info for {username}")
    friends = itchat.search_friends(name=username)
    if friends:
        author = friends[0]
        user = {'nickName': author.nickName, 'remarkName': author.remarkName, 'headImage': author.get_head_image_url()}
    return json.dumps(user)

@app.route("/getuserphoto", methods=['POST'])
def getuserphoto():
    data = request.json
    username = data['username']
    logger.info(f"Fetching user photo for {username}")
    friends = itchat.search_friends(name=username)
    if friends:
        author = friends[0]
        return itchat.get_head_img(author.userName)
    return "fail"

# 调用定义的方法
@app.route("/getmessagelist", methods=['GET'])
def getmessage():
    logger.info("Fetching message list")
    message = {"messages": messages}
    return json.dumps(message)

@app.route("/getfile", methods=['POST'])
def getfile():
    filename = request.json['filename']
    logger.info(f"Sending file: {filename}")
    return send_file(filename)

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    message = {}
    sender = msg.user.remarkName or msg.user.nickName
    logger.info(f"Received text message from {sender}: {msg.text}")
    message['name'] = sender
    message['content'] = msg.text
    message['time'] = int(datetime.datetime.now().timestamp())
    messages.append(message)
    farpush_instance.push_text(sender, msg.text)

@itchat.msg_register(itchat.content.MEDIA_TYPE_MSG)
def text_media(msg):
    if msg.type in itchat.content.MESSAGE_TEXT:
        msgtext = itchat.content.MESSAGE_TEXT[msg.type]
    else:
        msgtext = '未定义类型'
    sender = msg.user.remarkName or msg.user.nickName
    logger.info(f"Received media message from {sender}: {msgtext}")
    farpush_instance.push_text(sender, msgtext)

@itchat.msg_register([itchat.content.RECORDING, itchat.content.PICTURE])
def mes_media(msg):
    if not os.path.exists("files"):
        os.mkdir("files")
    msg.download(msg.fileName)
    sender = msg.user.remarkName or msg.user.nickName
    logger.info(f"Downloaded media file: {msg.fileName}")
    farpush_instance.push_text(sender, f"Received media: {msg.fileName}")

# for group
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    logger.info(f"Received group text message from {msg.user.nickName}: {msg.text}")
    farpush_instance.push_text(msg.user.nickName, msg.text)

def send(username, content):
    logger.info(f"Sending message to {username}: {content}")
    itchat.send(content, toUserName=username)

def send4nick(nickname, content):
    logger.info(f"Sending message to nickname {nickname}: {content}")
    friends = itchat.search_friends(name=nickname)
    if friends:
        author = friends[0]
        author.send(content)

def flask(ip, port):
    from waitress import serve
    logger.info(f"Starting Flask server on {ip}:{port}")
    serve(app, host=ip, port=port)

if __name__ == '__main__':
    logger.info("Starting application")
    farpush_instance = farpush.farpush()
    _thread.start_new_thread(flask, ('0.0.0.0', 9091))
    itchat.check_login()
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()