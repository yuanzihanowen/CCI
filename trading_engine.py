__author__ = 'zihanyuanowen'

import pandas as pd
import numpy as np
import os
import sklearn
from matplotlib import pyplot as plt
import rpy2.robjects as ro

def calculate_cci(security_name, period=15):
    px_file_path = os.getcwd() + '/output/' + security_name + '_data.csv'
    df = pd.read_csv(px_file_path)
    
    df_tp = pd.DataFrame(df, columns=['lowAsk', 'highAsk', 'closeAsk', 'time'])
    df_tp = df_tp.set_index('time')
    df_ask_last = pd.DataFrame(df_tp, columns=['closeAsk'])
    df_ask_high = pd.DataFrame(df_tp, columns=['highAsk'])
    df_ask_low = pd.DataFrame(df_tp, columns=['lowAsk'])
    df_tp = df_tp.sum(1)/3
    df_sma_tp = pd.rolling_mean(df_tp, window=period)
    df_md = pd.rolling_mean(df_sma_tp, window=period)
    df_md = abs(df_tp - df_md)*0.015
    df_cci = (df_tp - df_sma_tp)/df_md
    df_cci.columns = ['cci']
    df_cci.to_csv(os.getcwd() +'/engine_output/' + security_name + '_cci.csv')
    df_cci.columns = ['cci']
    return df_cci


def calculate_volume(security_name, period=15):
    px_file_path = os.getcwd() + '/output/' + security_name + '_data.csv'
    df = pd.read_csv(px_file_path)

    df_volume = pd.DataFrame(df, columns =['volume','time'])
    df_volume = df_volume.set_index(['time'])
    return df_volume


def get_trend(security_name):
    px_file_path = os.getcwd() + '/output/' + security_name + '_data.csv'
    df = pd.read_csv(px_file_path)

    df_tp = pd.DataFrame(df, columns=['lowAsk', 'highAsk', 'closeAsk', 'time'])
    # print(type(df_tp.iloc[1,3]))
    # df_tp['time'] = pd.to_datetime(df_tp['time'],format='%m/%d/%Y% %I:%M:%S')
    # df_tp['time'] = datetime.strptime(df_tp['time'] ,'%m/%d/%Y %I:%M:%S')
    df_tp = df_tp.set_index('time')
    df_tp = pd.DataFrame(df_tp, columns=['closeAsk','highAsk','time'])
    df_tp = df_tp.sum(1)/2
    # print(df_tp)
    df_tp.to_csv(os.getcwd() +'/engine_output/'+security_name+'_px_model.csv')

    # Use Mann-Kendall Test to test the existence of up or down trends
    # there is no package for MannKendall Test in Python
    ro.r("source('getTrend.R')")

    trend = pd.read_csv(os.getcwd()+'/engine_output/'+security_name+'_trend.csv')
    trend = trend.iloc[0,1]
    print(trend)
    return trend


def ts_signal(ts_cci, ts_volume, security_name):
    # time series analysis of the CCI time serie
    ts_cci.index = pd.to_datetime(ts_cci.index)
#    mu_cci = np.mean(ts_cci)
#    sigma_cci = np.std(ts_cci)
    ts_volume = pd.Series(ts_volume['volume'])

    # the model part needs to be worked on
    # Decompose the CCI into two parts (positive and negative)
#     ts_cci_pos = ts_cci
#     ts_cci_pos[ts_cci<0] = 0
# #    ts_cci_pos.plot(style='k--')
#     ts_cci_ne = ts_cci
#     ts_cci_ne[ts_cci>0] = 0
# #    ts_cci_ne.plot(style='k--')
# #     pplt = plt.plot(ts_cci_ne)
# #     pplt.savefig('plt.png')
#     trend = get_trend(security_name)
#     if trend == 'up':
#         ts_cci_ne
    signal_cci = pd.DataFrame(index=ts_cci.index,columns=['signal'])

    ts_cci2 =ts_cci.shift(1)
    for idx in ts_cci.index:
        if ts_cci2[idx]<100 and ts_cci[idx]>100:
            signal_cci.loc[idx,'signal']=-1
        elif ts_cci2[idx]>-100 and ts_cci[idx]<-100:
            signal_cci.loc[idx,'signal']=1

    return signal_cci
    # print(signal_cci[2])
# range(1,len(ts_cci.index))


def backtest(signal_cci,security):
    px_file_path = os.getcwd() + '/output/' + security + '_data.csv'
    df = pd.read_csv(px_file_path)

    df_tb = pd.DataFrame(df, columns=['time', 'closeAsk', 'closeBid'])
    df_tb.set_index('time')

    df_tb['signal']=signal_cci['signal']
    # df_trade=pd.DataFrame(sginal_cci,index=signal_cci.index,columns=signal_cci.columes)
    # df_trade[df_tb['signal']>1]
    df_tb['trade']=np.nan
    df_tb['quantity']=np.nan

    print(df_tb)




if __name__ == '__main__':
    os.chdir(os.path.expanduser('~/Desktop/Py_trading'))
    # security_list = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF']
    security_list = ['EUR_USD']

    for security in security_list:
        if not os.path.exists(os.getcwd() +'/engine_output/'):
            os.makedirs(os.getcwd() +'/engine_output/')
        df_cci = calculate_cci(security)
        # get_trend(security)
        df_volume = calculate_volume(security)
        df_cci = df_cci.dropna()
        df_cci.name = ['cci']
        # print(df_cci.name)
        df_volume = pd.DataFrame(df_volume, index=df_cci.index)
        df_signal_cci = ts_signal(df_cci, df_volume, security)
        backtest(df_signal_cci,security)
