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

def download_file_W_meghalaya(pdf_url, mdir, filename, flag=False):
    filename = mdir + filename
    ssl._create_default_https_context = ssl._create_unverified_context
    wget.download(pdf_url, filename)
    if os.stat(filename).st_size == 0:
        flag = 0
    else:
        flag = 1
    return flag

m_url = "http://ceomeghalaya.nic.in/erolls/erolldetails.html"
mdir = 'data/Meghalaya/'
base_url = "http://ceomeghalaya.nic.in/erolls/pdf/english/"

i_start = 1
j_start = 1
for i in range(i_start, 61):
    for j in range(j_start, 75):
        print("\n", i, j)
        p1 = format(i, '03d')
        p2 = format(j, '04d')
        suffix = "A{}/A{}{}.pdf".format(p1, p1, p2)
        url = base_url + suffix
        print(url)
        fid = suffix.replace("/", "_")
        try:
            flag = download_file_W_meghalaya(url, mdir, fid)
            if flag == 0:
                with open("Meghalaya.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            with open("Meghalaya.txt", "a") as myfile:
                myfile.write(url + '\n')
        time.sleep(1)
