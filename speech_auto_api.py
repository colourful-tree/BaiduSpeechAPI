#coding=utf-8
import urllib, urllib2, sys
import ssl
import base64
import json
import os
import commands

host = 'http://vop.baidu.com/server_api'

origin_path = "./origin"
origin_names = os.listdir(origin_path)
all_origin_files = []
for file_name in origin_names:
    all_origin_files.append(file_name)

FindPath = './data'
for each_origin_file in (all_origin_files):
    file_name = each_origin_file[:each_origin_file.find(".mp3")]
    os.system("mkdir %s/%s" % (FindPath, file_name))
    (status, output) = commands.getstatusoutput("sox %s -n stat" % (origin_path + "/" + file_name + ".mp3"))
    a = output.find("Length (seconds):") + len("Length (seconds):")
    b = output.find(".", a)
    music_len = int(output[a:b])
    for sp in range(0 ,music_len, 30):
        #print (origin_path + "/" + file_name + ".mp3", FindPath + "/" + file_name + "/" + file_name + " " + str(sp)+ ".wav", sp)
        os.system("sox %s -c 1 -r 8000 %s trim %d 30" % (origin_path + "/" + file_name + ".mp3", FindPath + "/" + file_name + "/" + file_name + "_" + str(sp).zfill(6) + ".wav", sp))

    FileNames = os.listdir(FindPath + "/" + file_name + "/")
    all_files = []

    for i in FileNames:
        all_files.append(os.path.join(FindPath, file_name, i))
    with open(FindPath + "/" + file_name + "/res.txt","w") as fout:
        for f in all_files:
            music = None
            with open(f, "r") as fin:
                music = fin.read()
            filesize = os.path.getsize(f)
            music = base64.b64encode(music)

            data = {
                "format":"wav",
                "rate":8000,
                "channel":1,
                "token":"24.3fd0f43802e3b18c73c3a067582b13f9.2592000.1506578811.282335-10067482",
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
                fout.write(content)
