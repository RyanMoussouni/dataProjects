# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:36:36 2020

@author: LENOVO
"""
import pandas as pd
from requests_html import HTMLSession
import random
import time
#-- Getting number of subs properly
def getCount(strCount:str)->int:
    splitString = strCount.replace(',','.').split()
    if len(splitString) > 1:
        multiplier = splitString[1] # the k in 1,1 k for instance
        if multiplier == 'k':
            strCount = int(float(splitString[0]) * 1e3)
        else:
            strCount = int(float(splitString[0]) * 1e6) # multiplier = M
    elif strCount == '':
        strCount = 0
    else:
        strCount = int(strCount)
    return strCount
# -- Extracting data from the first database, adding new data to it
videos = pd.read_csv('USVideos.csv')
id_ = videos['video_id']
url_ = ['https://youtube.com/watch?v='+ videoId for videoId in id_]
url_ = url_[:50]
errIdx = []
del videos
# -- Database
data = {'url': [], 'Subscribers': []}
for idx,url in enumerate(url_):
    if idx%10 ==0:
        print(idx)
    session = HTMLSession()
    r = session.get(url)
    print(r.headers)
    break
    r.html.render()
    try:
        about = r.html.find('#owner-sub-count', first=True)
        subsCount = getCount(about.text)
    except:
        print("Unexpected error:", idx)
        errIdx.append(idx)
        subsCount = None #will be NaN in the csv file
        pass
    session.close()
    data['url'].append(url[28:]) #taking only the id
    data['Subscribers'].append(subsCount)

data = pd.DataFrame(data)
data.to_csv('newData0-100.csv', index = False)
errIdx = pd.DataFrame(errIdx)
errIdx.to_csv('errIdx0-100.csv', index = False)

