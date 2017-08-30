#coding=utf-8
import urllib, urllib2, sys
import ssl
import base64
import json
import os

host = 'http://vop.baidu.com/server_api'

FindPath = './4_data'
FileNames = os.listdir(FindPath)

all_files = []
for file_name in FileNames:
    all_files.append(os.path.join(FindPath,file_name))

for f in all_files:
    music = None
    with open(f, "r") as fin:
        music = fin.read()
    filesize = os.path.getsize(f)
    music = base64.b64encode(music)

    data = {
        "format":"amr",
        "rate":8000,
        "channel":1,
        "token":"xxx",
        "cuid":"BAIDU_SPEECH_DIAOYAN",
        "len":filesize,
        "speech":music
    }
    j = json.dumps(data)

    request = urllib2.Request(host, data=j)
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        print content
