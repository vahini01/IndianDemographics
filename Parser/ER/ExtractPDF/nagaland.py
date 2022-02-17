#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 09:49:05 2017

@author: dhingratul
"""
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import urllib
import sys
sys.path.insert(0, '../tools/')
import utils
import ssl
import requests
import wget
import os
import numpy as np
import pandas as pd

def download_file_W_nagaland(pdf_url, mdir, filename, flag=False):
    filename = mdir + filename
    ssl._create_default_https_context = ssl._create_unverified_context
    wget.download(pdf_url, filename)
    if os.stat(filename).st_size == 0:
        flag = 0
    else:
        flag = 1
    return flag


m_url = "http://ceonagaland.nic.in/DownloadERoll"
base_url = 'http://ceonagaland.nic.in/Downloads/FinalRoll2021/'
mdir = 'data/Nagaland/'

df = pd.read_csv('nagaland.csv')
len = df.shape[0]
for x in range(1858,len):
    pdf_name = df['filename'][x]
    i = int(pdf_name[2:5])
    j = int(pdf_name[9:12])
    print("\n", i, j)
    suffix = "{}/S17A{}P{}.pdf".format(i,i,j)
    url = base_url + suffix
    print(url)
    fid = suffix.replace("/", "_")
    try:
        flag = download_file_W_nagaland(url, mdir, fid)
        if flag == 0:
            with open("nagaland.txt", "a") as myfile:
                myfile.write(url + '\n')
    except urllib.error.HTTPError:
        print("Error")
        with open("nagaland.txt", "a") as myfile:
            myfile.write(url + '\n')
