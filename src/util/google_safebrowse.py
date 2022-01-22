
""" Version 0.2.0

Google Safe Browsing Lookup library for Python.

If you need to check less than 10,000 URLs a day against the Google Safe Browsing v2 API (http://code.google.com/apis/safebrowsing/), you can use the Lookup API (http://code.google.com/apis/safebrowsing/lookup_guide.html) as a lighter alternative to the more complex API (http://code.google.com/apis/safebrowsing/developers_guide_v2.html).

You need to get an API key from Google at http://code.google.com/apis/safebrowsing/key_signup.html """

import urllib.request
import re
import http.client
import requests
import json
from pysafebrowsing import SafeBrowsing
from datetime import date, timedelta
import json
import time
import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import pandas as pd
from gspread.models import Cell
import numpy as np

# api_key = 'AIzaSyBfGrp3D80GN7CB2rEnp_TtmLjLnqvbQpg'
api_key = 'AIzaSyB6IL1wAQZZEh1fil04YIUNTzi1EsXR1ls'
# api_key = 'AIzaSyAGlId-l2ePh7TimYgyOz0AbcSZXSgWd58'

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def call_gs_browsing(date_):
    # TODO check the URLs after 1 month to get FNs
    '''check how many'''
    with open('{}_safebrowsing.json'.format(date_), 'r') as f:
        results = json.load(f)
    print(len(results))

    '''call google sb'''
    try:
        df = [x.strip().split('\t') for x in open('./{}.txt'.format(date_), encoding='ISO-8859-1').readlines()]
    except FileNotFoundError:
        exit()
    urls = [x[1] for x in df[1:]]
    results = []
    if os.path.exists('{}_safebrowsing.json'.format(date_)):
        with open('{}_safebrowsing.json'.format(date_), 'r') as f:
            results = json.load(f)
    print(len(results))

    for url in urls:
        print(url)
        if os.path.exists('{}_safebrowsing.json'.format(date_)):
            if url in open('{}_safebrowsing.json'.format(date_)).read():
                print('skip')
                continue
        s = SafeBrowsing(api_key)
        try:
            r = s.lookup_urls([url])
        except:
            continue
        results.append(r)
    with open('{}_safebrowsing.json'.format(date_), 'w') as f:
        json.dump(results, f)


def get_fn_fromgs(date_):

    result_txt = './{}.txt'.format(date_)
    df = [x.strip().split('\t') for x in open(result_txt, encoding='ISO-8859-1').readlines()]
    df_pos = [x for x in df if (len(x) >= 3) and (x[2] == '1')]
    intention_pos_urls = np.asarray([x[1] for x in df_pos])

    with open('{}_safebrowsing.json'.format(date_), 'r') as f:
        results = json.load(f)
    urls = [list(x.keys())[0] for x in results]
    maliciousness = [list(x.values())[0]['malicious'] for x in results]
    assert len(urls) == len(maliciousness)
    gs_df = pd.DataFrame({'url': urls, 'maliciousness': maliciousness})
    gs_pos_urls = list(gs_df.loc[gs_df['maliciousness'] == True]['url'])
    # corresponding folders
    gs_pos_folders = []
    for j in range(len(gs_pos_urls)):
        for i in range(len(df)):
            if df[i][1] == gs_pos_urls[j]:
                gs_pos_folders.append(df[i][0])
                break

    gs_pos_urls = np.asarray(gs_pos_urls)
    gs_pos_folders = np.asarray(gs_pos_folders)
    assert len(gs_pos_folders) == len(gs_pos_folders)

    isreported_by_intention = np.isin(np.asarray(gs_pos_urls), intention_pos_urls) # if google safebrowsing URLS is not reported by phishintention

    intention_fn_folder = gs_pos_folders[isreported_by_intention == False]
    intention_fn_urls = gs_pos_urls[isreported_by_intention == False]
    intention_fn_date = [date_] * len(intention_fn_urls)

    intention_tp_folder = gs_pos_folders[isreported_by_intention == True]
    intention_tp_urls = gs_pos_urls[isreported_by_intention == True]
    intention_tp_date = [date_] * len(intention_tp_folder)

    return intention_fn_date, intention_fn_folder, intention_fn_urls, \
           intention_tp_date, intention_tp_folder, intention_tp_urls


class gwrapperFN():
    def __init__(self):
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        file_name = 'tele/cred.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
        client = gspread.authorize(creds)
        # Fetch the sheet
        self.sheet = client.open('Phishintention_FN_GoogleSafe').sheet1
        self.rows = self.get_records()

    def get_records(self):
        return self.sheet.get_all_records()

    def update_list(self, to_update):
        folder_names = list(map(lambda x: x['URLs'], self.rows))
        if np.isin(to_update[0][2], folder_names).any():
            return
        self.sheet.append_rows(to_update)


if __name__ == '__main__':
    call_gs_browsing(date_=date(2021, 10, 29).strftime("%Y-%m-%d"))
    # intention_fn_date, intention_fn_folder, intention_fn_urls, \
    # intention_tp_date, intention_tp_folder, intention_tp_urls =  get_fn_fromgs(date(2021, 10, 27).strftime("%Y-%m-%d"))
    #
    # gs = gwrapperFN()
    # for i in range(len(intention_fn_urls)):
    #     toupdate = [[intention_fn_date[i], intention_fn_folder[i], intention_fn_urls[i], 'no', '']]
    #     time.sleep(1)
    #     gs.update_list(toupdate)
    #
    # for i in range(len(intention_tp_urls)):
    #     toupdate = [[intention_tp_date[i], intention_tp_folder[i], intention_tp_urls[i], 'yes', '']]
    #     time.sleep(1)
    #     gs.update_list(toupdate)
