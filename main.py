import pandas as pd
import datetime
import re
import os

import plotly.figure_factory as ff
import tweepy

# 今日の日付を取得
now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
today = now.date()

# スプレッドシート読み込み
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5yTYaZX7YOA0bTx_DYShEVCBXqKntpOyHdBDJWVODzfcXAjpoBDScrMaVF1VSfYMcREZb3E30E0ha/pub?gid=630053475&single=true&output=csv"

df = pd.read_csv(url).fillna("")

# df['確認日']をdatetime型に変換
df['確認日'] = pd.to_datetime( df['確認日'], format = '%Y/%m/%d', errors='coerce')

# df['確認日']から今日のデータを抽出
df1 = df[df["確認日"] == pd.Timestamp(today)]

# df['所在地']から市区町村名を抽出する関数
def get_prefectures(address):

    pattern = '奈良市|大和高田市|大和郡山市|天理市|橿原市|桜井市|五條市|御所市|生駒市|香芝市|葛城市|宇陀市|山添村|平群町|三郷町|斑鳩町|安堵町|川西町|三宅町|田原本町|曽爾村|御杖村|高取町|明日香村|上牧町|王寺町|広陵町|河合町|吉野町|大淀町|下市町|黒滝村|天川村|野迫川村|十津川村|下北山村|上北山村|川上村|東吉野村'

    m = re.match(pattern, address)

    if m:
        return m.group()
    else:
        return address

# df['開局状況']の値を置換する為の辞書
df_replace = {
    'OK': '開局',
    'NG': '未開局',
    'OK(仮)': '開局(仮)',
    'OK(未知局)': '開局(未知局)',
    'NG(仮)': '未開局(仮)',
}

if len(df1) > 0:

    df1['市区町村名'] = df1['所在地'].apply(get_prefectures)

    df1['開局状況'] = df1['開局状況'].replace(df_replace)

    df2 = df1[['名称', '開局状況']]

    fig = ff.create_table(df2)

    # 下部に余白を付けて更新日を表記
    fig.update_layout(
    title_text = now.strftime("%Y年%m月%d日") + ' に確認された基地局一覧です。',
    title_x = 0.98,
    title_y = 0.025,
    title_xanchor = 'right',
    title_yanchor = 'bottom',
    # 余白の設定
    margin = dict(l = 0, r = 0, t = 0, b = 45)

    ) 

    # タイトルフォントサイズ
    fig.layout.title.font.size = 10

    # scale=10だとツイート時に400 Bad Request
    fig.write_image('data/today_finded.png', engine='kaleido', scale=2)

    count_dic = df1['市区町村名'].value_counts().to_dict()

    count = ''

    for key, value in count_dic.items():
        count += key + '：' + str(value) + '件' + '\n'

    tweet = f'【本日の調査まとめ】\n\n{count}\n調査ご報告ありがとうございました。\n\nhttps://denpayanara.github.io/rakuten/map.html\n#楽天モバイル #奈良 #bot'

    print(tweet)

    # ツイート

    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET_KEY"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    client = tweepy.Client(consumer_key = api_key, consumer_secret = api_secret, access_token = access_token, access_token_secret = access_token_secret,)

    media_ids = []

    res_media_ids = api.media_upload('data/today_finded.png')

    media_ids.append(res_media_ids.media_id)

    client.create_tweet(text = tweet, media_ids=media_ids)
