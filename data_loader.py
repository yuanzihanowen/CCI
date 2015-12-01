__author__ = 'zihanyuanowen'

import requests
import json
import pandas as pd
# import numpy as np
# import logging
import os


def connect(domain, access_token, account_id, inst, frequency='M15', count=5000):

    try:
        s = requests.session()
        url = domain + "/v1/candles"
        # url = domain + "/v1/prices" # Get Streaming data
        param = {'accountId': account_id, 'instrument': inst, 'granularity': frequency, 'count': count}
        # param = {'accountId': account_id, 'instruments': inst}
        header = {'Authorization' : 'Bearer ' + access_token,   # 'X-Accept-Datetime-Format' : 'unix'
                  }
        req = requests.Request('GET', url, headers=header, params=param)
        prep = req.prepare()
        response = s.send(prep)
        return response
    except Exception as e:
        s.close()
        print str(e)


def read_data(r, inst_name):
    json_file = r.json()  # r is the response
    file_name = inst_name + '.json'

    # out_dir = '~/Desktop/PyScrap/output/'
    out_dir = os.getcwd() + '/output/'
    with open(out_dir+file_name, "w") as outfile:
        json.dump(json_file, outfile)

    json_data = json.load(open(out_dir+file_name))
    df_dict_instrument = pd.DataFrame(json_data['candles'])
    df_dict_instrument.to_csv(out_dir+inst_name+'_data.csv')


def load_dict(accountid, dict_domain, token):
    s = requests.session()
    dict_domain += "/v1/instruments"
    parameter = {'accountId': accountid}
    hdr= {'Authorization' : 'Bearer ' + token}
    req = requests.Request('GET', dict_domain, headers=hdr, params=parameter)
    pre = req.prepare()
    dict_resp = s.send(pre)

    # out_dir = '~/Desktop/PyScrap/output/'
    out_dir = os.getcwd() + '/output/'
    with open(out_dir+'dict.json', "w") as outfile:
        json.dump(dict_resp.json(), outfile)

    json_data = open(out_dir+'dict.json')
    data = json.load(json_data)
    list_instruments = data["instruments"]
    df_dict_instrument = pd.DataFrame(list_instruments)
    df_dict_instrument.to_csv(out_dir+'dict_instr.csv')
    return df_dict_instrument


if __name__ == '__main__':

    os.chdir(os.path.expanduser('~/Desktop/Py_trading'))
    print(os.getcwd())
    dm = 'https://api-fxpractice.oanda.com'
    a_t = '9e6898d3bc4f5ef5dd0cacd8fd025b31-7dc39a42131d5dfbaa3844e0ea330914' #Access Token needed
    acct_id = '8244239'

    dict_security = load_dict(acct_id, dm, a_t)
    for instrument in ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF']:
        resp = connect(dm, a_t, acct_id, instrument)
        read_data(resp, instrument)
