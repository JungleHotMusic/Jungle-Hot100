from email import charset
import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbHotMusic

def drop_chart():
    db.charts.drop()
    

drop_chart()

def insert_chart():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.melon.com/chart/', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser') 

    charts = soup.select('#tb_list > form > div > table > tbody > tr')

    for chart in charts:

        musics = chart.select_one('td:nth-child(6) > div >  div.wrap_song_info > div > span > a').text
        img_urls = chart.select_one('td:nth-child(4) > div > a > img')['src']
        artist = chart.select_one('td:nth-child(6) > div > div.wrap_song_info > div > a').text
        rank = chart.select_one('td:nth-child(2) > div > span.rank').text
        click_urls = chart.select_one('td:nth-child(4) > div > a')['href']
        click_url_num = re.sub(r'[^0-9]','',click_urls)
        base_url = 'https://www.melon.com/album/detail.htm?albumId=' 
        click_url = base_url + click_url_num
  
    
        doc = {
            'rank': rank,
            'music': musics,
            'artist': artist,
            'img_url':img_urls,
            'click_url': click_url
        }

        db.charts.insert_one(doc)

insert_chart()
