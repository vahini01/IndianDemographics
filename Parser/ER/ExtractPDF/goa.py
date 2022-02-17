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


def getDistrict(m_url, element):
    driver = utils.getDriver(m_url)
    mySelect_D = Select(driver.find_element_by_id(element))
    num_D = len(mySelect_D.options)  # Start from 1, 0 -- Select
    return driver, mySelect_D, num_D

def download_file_W_goa(pdf_url, mdir, filename, flag=False):
    filename = mdir + filename
    ssl._create_default_https_context = ssl._create_unverified_context
    wget.download(pdf_url, filename)
    if os.stat(filename).st_size == 0:
        flag = 0
    else:
        flag = 1
    return flag


m_url = "https://ceogoa.nic.in/appln/uil/ElectoralRoll.aspx"
base_url = 'https://ceogoa.nic.in/PDF/EROLL/MOTHERROLL/2021/'
mdir = 'data/Goa/'
driver, _, num_D = getDistrict(m_url, 'ctl00_Main_drpAC')
driver.quit()

i_start = 39
j_start = 1
for i in range(i_start, num_D):
    driver, mySelect_D, _ = getDistrict(m_url, "ctl00_Main_drpAC")
    mySelect_D.options[i].click()
    # Click button
    driver.find_element_by_css_selector('#ctl00_Main_btnSearch').click()
    time.sleep(1)
    # Get Corresponding element
    id = str(i+1)
    path = "//html/body/form/div[3]/div[3]/div/div[5]/div/div[{}]".format(id)+"/div/*"
    n_rows = len(driver.find_elements_by_xpath(path))-2
    # driver.quit()
    if i==39: j_start=13
    for j in range(j_start, n_rows):
        print("\n", i, j)
        suffix = "{}/S05A{}P{}.pdf".format(i,i, j)
        url = base_url + suffix
        print(url)
        fid = suffix.replace("/", "_")
        try:
            flag = download_file_W_goa(url, mdir, fid)
            if flag == 0:
                with open("goa.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            print("Error")
            with open("goa.txt", "a") as myfile:
                myfile.write(url + '\n')
    driver.quit()
