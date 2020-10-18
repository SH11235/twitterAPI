#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config
import urllib
from requests_oauthlib import OAuth1
import requests
# import sys
import cgi

# args = sys.argv


def main():
    # APIの秘密鍵
    CK = config.CONSUMER_KEY
    CKS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_SECRET

    # 検索時のパラメーター
    form = cgi.FieldStorage()
    text = form.getvalue('text', '')
    # word = args[1]  # 検索ワード
    word = text  # 検索ワード
    count = 10  # 一回あたりの検索数(最大100/デフォルトは15)
    range = 10  # 検索回数の上限値(最大180/15分でリセット)

    html_body = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>受信したデータを表示</title>
        <style>
        h1 {
        font-size: 3em;
        }
        </style>
        </head>
        <body>
        <h1>TwitterAPI Result</h1>
        <div>%s</div>
        </body>
        </html>
        """

    path = './test.txt'
    spacer = "=============================================\n"

    # ツイート検索・テキストの抽出
    if not text:
        print("引数でキーワードを指定")
    else:
        tweets = search_tweets(CK, CKS, AT, ATS, word, count, range)
        # 検索結果を表示
        spaceNum = 0
        with open(path, mode='w') as f:
            for tweet in tweets:
                if (spaceNum % 5 == 0):
                    f.write(spacer)
                spaceNum += 1
                f.write(tweet)

        print(html_body % (''.join(tweets)))


def search_tweets(CK, CKS, AT, ATS, word, count, range):
    # 文字列設定
    word += ' exclude:retweets'  # RTは除く
    word = urllib.parse.quote_plus(word)
    # リクエスト
    url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q=" + \
        word+"&count="+str(count)
    auth = OAuth1(CK, CKS, AT, ATS)
    response = requests.get(url, auth=auth)
    data = response.json()['statuses']
    # 2回目以降のリクエスト
    cnt = 0
    tweetsCount = 0
    tweets = []
    while True:
        if len(data) == 0:
            break
        cnt += 1
        if cnt > range:
            break
        for tweet in data:
            tweetsCount += 1
            user = tweet["user"]
            tweets.append(str(tweetsCount) + "件目<br>")
            tweets.append("name:" + user["name"] + "\n" + "<br>")
            # tweets.append(user["statuses_count"])  # 投稿数
            # tweets.append(user["friends_count"])  # フォロー数
            # tweets.append(user["followers_count"])  # フォロワー数
            tweets.append("投稿日時:" + tweet["created_at"] + "\n" + "<br>")
            tweets.append(
                "いいね数:" + str(tweet["favorite_count"]) + "\n" + "<br>")
            tweets.append(
                "リツイート数：" + str(tweet["retweet_count"]) + "\n" + "<br>")
            tweets.append(tweet['text'] + "\n" + "<br>")
            maxid = int(tweet["id"]) - 1
        url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q=" + \
            word+"&count="+str(count)+"&max_id="+str(maxid)
        response = requests.get(url, auth=auth)
        try:
            data = response.json()['statuses']
        except KeyError:  # リクエスト回数が上限に達した場合のデータのエラー処理
            print('上限まで検索しました')
            break
    return tweets


if __name__ == '__main__':
    main()
