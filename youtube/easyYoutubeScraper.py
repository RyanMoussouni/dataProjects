# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:36:36 2020

@author: LENOVO
"""



from requests_html import HTMLSession

url = 'https://perso.telecom-paristech.fr/rmoussouni/simple.html'

session = HTMLSession()
r = session.get(url)
r.html.render()
about = r.html.find('#lol', first=True)
print(about.text)


