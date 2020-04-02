#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
import os
import re
#通过获取到的歌曲ID，获取歌曲的下载链接和歌曲名字
def get_link(ID):
    url='http://play.taihe.com/data/music/songlink'
    data={
    'songIds': ID,
    'hq': '0',
    'type': 'm4a,mp3',
    'rate': '',
    'pt': '0',
    'flag': '-1',
    's2p': '-1',
    'prerate': -1,
    'bwt': '-1',
    'dur': '-1',
    'bat': '-1',
    'bp': '-1',
    'pos': '-1',
    'auto': '-1',
    }
    header={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '140',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'BAIDUID=32AD223CA67735FE956BB11E40AE00D5:FG=1; log_sid=158556136821732AD223CA67735FE956BB11E40AE00D5; Hm_lvt_2b0f0945031c52df2a103f3ed5d7c3aa=1585542199,1585561368; Hm_lpvt_2b0f0945031c52df2a103f3ed5d7c3aa=1585561368; sort-guide-showtimes=2; sort-guide-lastshow=1585561368445',
    'Host': 'play.taihe.com',
    'Origin': 'http://play.taihe.com',
    'Referer': 'http://play.taihe.com/?__m=mboxCtrl.playSong&__a=674842469&__o=/top||dayhotIcon&fr=-1||-1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }
    response=requests.post(url=url,headers=header,data=data)
    music_json=response.json()['data']['songList']
    response.encoding=response.apparent_encoding
    for i in music_json:
        songlink=i['songLink']
        songname=i['songName']
        #print(songid,songname)
        yield songlink,songname      #生成一个解释器，将所生成的结果包装成一起

#os.mkdir('千千音乐下载')
def get_links():
    url='http://music.taihe.com/top/dayhot'
    response=requests.get(url)
    response.encoding=response.apparent_encoding #万能解码
    html=response.text
    song_id=re.findall(r'a href="/song/(\d+)" target="_blank',html)
    return song_id
#通过获取的歌曲id，还有下载链接，为下载准备
def down(id_list):
    #id_list=['674842469']
    songid=','.join(id_list)
    #print(songid)
    song=get_link(songid)
    path=os.getcwd()
    true_num,false_num=0,0
    false_song=[]
    for songlink,songname in song:#由于生成一个接收器，可以用循环分开
        try:
            music_file=open('千千音乐下载//'+songname+'.m4a','wb')
            response=requests.get(songlink)
            music_file.write(response.content)
            true_num+=1
            print('%s下载成功'%songname)
        except:
            false_num+=1
            print('%s下载失败'%songname)
            false_song.append(songname)
    music_file.close()
    print('此次歌曲下载来自千千音乐的热歌榜，url=http://music.taihe.com/top/dayhot;')
    print('本次一共%s首，下载成功%s首，下载失败%s首'%((true_num+false_num),true_num,false_num))
    print("下载失败的歌曲有%s"%false_song)
songid=get_links()
down(songid)

