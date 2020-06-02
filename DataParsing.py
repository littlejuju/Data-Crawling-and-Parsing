# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:18:17 2019

@author: Xiangqi
"""
import pandas as pd
#from requests_html import HTMLSession
import requests
import html2text
from License import users, headers
from constants import seasons
import numpy as np

class DataParsing(object):
    session = requests.Session()
    
    
    """ 1. download data from website based """
    # get main url list by stickers and website
    @staticmethod
    def get_url(sticker, website = 'seeker'):
        if website == 'seeker':
            url = 'https://seekingalpha.com/symbol/' + sticker + '/earnings/transcripts'
        elif website == 'fool':
            url = 'https://seekingalpha.com/symbol/' + sticker + '/earnings/transcripts'
        return url
    
    # get urls for 12 cosecutive quarters
    @staticmethod
    def get_sub_url(sticker, website = 'seeker'):
        url = DataParsing.get_url(sticker, website = website)
        print(url)
        url_list = list()
        index = np.random.randint(low = 0, high = len(users))
        data = users[index]
        r = DataParsing.session.get(url, headers = headers, data = data)
        text = str(r.text)
        url_list = text.split('<div class="symbol_article"><a href="')
        url_list = ['https://seekingalpha.com' + url.split('"')[0] for url in url_list if DataParsing.contain_season(url)]
        print(url_list)
        if website == 'fool':
#            print('fool')
            website = 'seeker'
            return DataParsing.get_sub_url(url, website)
        return url_list
    
    def contain_season(url):
        for season in seasons:
            if season in url:
                return True
        return False
    
    """ 2. parsing """
    def get_text(url):
        text_frame = {'Comments': list(), 'Participant': list(), 'Designation':list()}
    #    comment_index_dict = dict()
        comment_index_list = list()
        comment_index_end_list = list()
        index = np.random.randint(low = 0, high = len(users))
        data = users[index]
        r = DataParsing.session.get(url, headers = headers, data = data)
        text = str(r.text)
        text = html2text.html2text(text)
        try:
            participants = text.split('Company Participants')[1].split('Operator')[0]
        except IndexError:
            print(text)
            participants = text.split('Executives')[1].split('Operator')[0]
        participants = [part for part in participants.split('\n') if len(part) > 2 and ' - ' in part]
        for part in participants:
            part1 = part.split(' - ')
            part2 = part1[0] + '**\n'
            text_frame['Participant'].append(part1[0])
            text_frame['Designation'].append(part1[1])
            text_frame['Comments'].append(list())
            index_list = [i for i in range(len(text)) if text.startswith(part2, i)] 
            index_end_list = [i for i in range(len(text)) if text.startswith('\n**', i)] 
    #        comment_index_dict[part2] = (index_list)
            comment_index_list.extend(index_list)
            comment_index_end_list.extend(index_end_list)
        comment_index_list = sorted(comment_index_list)
        comment_index_end_list = sorted(comment_index_end_list)
        for index in comment_index_list:
            try:
                end_index = len(text)
                end_point = 0
                while end_index > index:
                    end_point -= 1
                    end_index = comment_index_end_list[end_point]
                end_index = comment_index_end_list[end_point+1]
                comments = text[index : end_index]
            except IndexError:
                comments = text[comment_index_list[index] :]
            name = comments.split('\n')[0]
            for part_index in range(len(text_frame['Participant'])):
                part = text_frame['Participant'][part_index]
                if part in name:
                    text_frame['Comments'][part_index].append(comments[comments.index('\n')+2:])
                    continue
        df_frame = {'Comments': list(), 'Participant': list(), 'Designation':list()}
        for index in range(len(text_frame['Participant'])):
            if len(text_frame['Comments'][index]) == 0 or (len(text_frame['Comments'][index]) == 1 and text_frame['Comments'][index][0] == ''):
                continue
            df_frame['Comments'].append(text_frame['Comments'][index])
            df_frame['Participant'].append(text_frame['Participant'][index])
            df_frame['Designation'].append(text_frame['Designation'][index])
        df_frame = pd.DataFrame(df_frame)
        return df_frame
    
    ##### test here
    