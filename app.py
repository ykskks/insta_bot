import os
import random

from flask import Flask
from instapaper import Instapaper as ipaper
import requests



INSTAPAPER_KEY = os.getenv('INSTAPAPER_KEY')
INSTAPAPER_SECRET = os.getenv('INSTAPAPER_SECRET')
EMAIL_ADRESS = os.getenv('EMAIL_ADRESS')
PASSWORD = os.getenv('PASSWORD')
URL = os.getenv('URL')


app = Flask(__name__)


@app.route('/')
def pick_article():
    # 未読の記事と既読の記事（復習がてら）一件ずつ
    i = ipaper(INSTAPAPER_KEY, INSTAPAPER_SECRET)
    i.login(EMAIL_ADRESS, PASSWORD)

    # 未読
    new_article = random.choice(i.bookmarks(limit=500))
    new = requests.post(URL, json={"text": new_article.url})  

    id_old = i.folders()[0]["folder_id"]   
    new_article.move(id_old) 


    # 既読
    old_article = random.choice(i.bookmarks(limit=500, folder=id_old))      
    old = requests.post(URL, json={"text": old_article.url})  
     


if __name__ == '__main__':
    app.run()