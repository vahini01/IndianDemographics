#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 12:53:49 2018

@author: dhingratul
"""
import time
from bs4 import BeautifulSoup
import urllib
import ssl
import requests
import wget
import os

def download_file_W_delhi(pdf_url, mdir, filename, flag=False):
    filename = mdir + filename
    ssl._create_default_https_context = ssl._create_unverified_context
    wget.download(pdf_url, filename)
    if os.stat(filename).st_size == 0:
        flag = 0
    else:
        flag = 1
    return flag

mdir = 'data/Delhi/'
base_url = "https://ceodelhi.gov.in/engdata/"

i_start = 21
j_start = 1
arr = [296, 305, 184, 162, 217, 254, 344, 279, 274, 173, 248, 180, 171, 164, 143, 154, 182, 164, 174, 133, 131, 152,179, 189]
for i in range(i_start, 25):
    if i==21:
        j_start = 90
    else:
        j_start = 1
    for j in range(j_start, arr[i-1]+1):
        print("\n", i, j)
        suffix = "AC{}/U05A{}P{}.pdf".format(i, i, j)
        url = base_url + suffix
        print(url)
        fid = suffix.replace("/", "_")
        try:
            flag = download_file_W_delhi(url, mdir, fid)
            if flag == 0:
                with open("Delhi.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            with open("Delhi.txt", "a") as myfile:
                myfile.write(url + '\n')
