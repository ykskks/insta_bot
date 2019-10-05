import os
import random
import datetime

from flask import Flask
from instapaper import Instapaper as ipaper
import requests



INSTAPAPER_KEY = os.getenv("INSTAPAPER_KEY")
INSTAPAPER_SECRET = os.getenv("INSTAPAPER_SECRET")
EMAIL_ADRESS = os.getenv("EMAIL_ADRESS")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")


app = Flask(__name__)


@app.route("/")
def hello_world():
    print("Hello, this is an instapaper bot!")
    return "ok"


@app.route("/pick_article", methods=["GET"])
def pick_article():
    i = ipaper(INSTAPAPER_KEY, INSTAPAPER_SECRET)
    i.login(EMAIL_ADRESS, PASSWORD)

    # 今日の日付(USで実行されるのでUSにおける翌日の日付を取得)
    today = datetime.date.today() + datetime.timedelta(days=1)     
    today = today.strftime("%-m/%-d")
    r = requests.post(URL, json={"text": f"今日は{today}です!\n"})

    # 既読の記事からランダムに復習
    id_old = i.folders()[0]["folder_id"]   
    old_article = random.choice(i.bookmarks(limit=500, folder=id_old))      
    old = requests.post(URL, json={"text": "復習\n" + old_article.url})  

    # 未読の記事を新たに勉強、既読フォルダへ移行
    new_article = random.choice(i.bookmarks(limit=500))
    new = requests.post(URL, json={"text": "新しい記事\n" + new_article.url})  

    new_article.move(id_old)

    return "ok"
     


if __name__ == "__main__":
    port = int(os.environ.get("PORT"))
    app.run(host="0.0.0.0", port=port, debug=False)
  

