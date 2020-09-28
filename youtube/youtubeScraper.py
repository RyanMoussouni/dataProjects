# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 10:58:29 2020

@author: LENOVO
"""
#%% Packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import time
import pdb
import sys
#%% Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=940x600")
#%% Driver
pathToDriver = 'chrome\chromeDriver'
driver = webdriver.Chrome(options=chrome_options, executable_path=pathToDriver)
#%% Elements retrieval

def elementRetrieval(commentsDisabled:bool):
    subsCount = getCount(driver.find_element_by_id('owner-sub-count').text)
    
    #Scrolling down to get to the comments
    driver.execute_script('window.scrollTo(0, 480)')
    time.sleep(3)
    heartCount =len(driver.find_elements_by_id('hearted'))
    comments_ = driver.find_elements_by_id('vote-count-middle')
    commentsLikesCount = int(0.2 * np.sum([getCount(comments_[k].text) for k in range(5)])) #took only the first 4 comments
    return subsCount, heartCount, commentsLikesCount

# -- Extracting data from the first database, adding new data to it
videos = pd.read_csv('USVideos.csv')

id_ = videos['video_id']
ratings = videos['ratings_disabled']
comments = videos['comments_disabled']
removed = videos['video_error_or_removed']

url_ = ['https://youtube.com/watch?v='+ videoId for videoId in id_]
url_ = url_[:50]
errIdx = []
del videos
# -- Database
data = {'url': [], 'Subscribers': [], 'Number of Hearts' : [], 'Top Comments Likes' : []}

for idx,url in enumerate(url_):
    driver.get(url) #rendering website to crawl
    time.sleep(3)  #pausing to let the content of the dom be loaded
    commentsDisabled = comments[idx]
    if not(commentsDisabled) and not(removed[idx]):
        try:
            subsCount, heartCount, commentsLikesCount = elementRetrieval(commentsDisabled)
        except:
            print("Unexpected error:", idx)
            errIdx.append(idx)
            subsCount,heartCount,commentsLikesCount = None,None,None
            pass
    else:
        #otherwise, the data might not be interesting for my work, I'll get rid of it later
        subsCount,heartCount,commentsLikesCount = None,None,None
    
    data['url'].append(url)
    data['Subscribers'].append(subsCount)
    data['Number of Hearts'].append(heartCount)
    data['Top Comments Likes'].append(commentsLikesCount)


data = pd.DataFrame(data)
data.to_csv('newData.csv', index = False)


#%% Casting count from string to int
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