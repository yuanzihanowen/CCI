# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 00:56:55 2015

@author: zihanyuanowen
"""

import requests
import os
# import json
import pandas as pd
import rpy2.robjects as ro
# import datetime



# def calendar_parser():
#     os.chdir(os.path.expanduser('~/Desktop/Py_trading'))
#     filename = os.getcwd() + '/EconCalendar/Calendar.xls'
#     out_dir = os.getcwd() + '/EconCalendar/output/'
#
#     print xlrd.__VERSION__
#     wb = xlrd.open_workbook(filename,).sheet_by_index(0)
#     # print wb._all_sheets_count

def calendar_parser():
    os.chdir(os.path.expanduser('~/Desktop/Py_trading/EconCalendar/'))
    # file = pd.read_csv(os.getcwd() + 'calendar.csv')
    ro.r("source('readCalendar.R')")

if __name__ == '__main__':
    # website = 'http://www.dailyfx.com/files'
    # hdr = {'User-Agent': 'Mozilla/5.0'}
    # n = 0 - datetime.datetime.today().weekday() -1
    # date = datetime.datetime.today() + datetime.timedelta(days=n)
    # date = date.strftime('%m-%d-%Y')
    # f = website + '/Calendar-' + date + '.xls'
    #
    # try:
    #     req = urllib2.Request(f, headers=hdr)
    # except urllib2.urlError, e:
    #     print(e.reason)
    #
    # response = urllib2.urlopen(req)
    # myfile = open('Calendar.xls','w')
    # myfile.write(response.read())
    # myfile.close
    # calendar_parser()

    os.chdir(os.path.expanduser('~/Desktop/Py_trading'))
    domain = 'https://api-fxpractice.oanda.com/'
    acct_token = '9e6898d3bc4f5ef5dd0cacd8fd025b31-7dc39a42131d5dfbaa3844e0ea330914' #Access Token needed
    acct_id = '8244239'

    conn = requests.session()
    url = domain + "labs/v1/calendar"
    l_instrument = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF','AUD_USD','NZD_USD']
    period = 86400    # 86400 - 1 day; 604800- 1 week;
    param = {'accountId': acct_id, 'instrument': l_instrument, 'period':period}
    header = {'Authorization': 'Bearer ' + acct_token}

    req = requests.Request('GET', url, headers=header, params=param)
    pre = req.prepare()
    resp = conn.send(pre)

    out_dir = os.getcwd() + '/EconCalendar/'
    file = resp.json()
    file = pd.DataFrame(file)
    file.to_csv(out_dir+'calendar.csv')

    conn.close()
    calendar_parser()







