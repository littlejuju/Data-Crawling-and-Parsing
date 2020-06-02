# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 09:19:15 2019

@author: Xiangqi
"""
from constants import path, sleep_time, if_save
import sys
import time
import pandas as pd
from DataParsing import DataParsing


def main():
    """ 1. derive all parameters """
    if len(sys.argv) == 1:
        sticker_list = ['BIDU']
        website = 'seeker'
    elif len(sys.argv) > 1:
        sticker_list = [sys.argv[index] for index in range(len(sys.argv)-1) if index > 0]
        if sys.argv[-1] == 'seeker':
            website = 'seeker'
        elif sys.argv[-1] == 'fool':
            website = 'fool'
        else:
            sticker_list.append(sys.argv[-1])
            website = 'seeker'
    
    print(sticker_list)
    """ 2. get all url and parsing text based on stickers"""
    for sticker in sticker_list:
#        print(sticker)
        url_list = DataParsing.get_sub_url(sticker = sticker, website = website)
#        print(url_list)
        df_sticker = list()
        for url in url_list:
            df_sticker.append(DataParsing.get_text(url))
            time.sleep(sleep_time)
            print('get parsing text from: ' + url)
        df = pd.concat(df_sticker)
        if if_save:
            df.to_csv(path + sticker + '.csv')
            print('store data in ' + path + sticker + '.csv')

if __name__ == "__main__":
    main()