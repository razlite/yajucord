# -*- coding: utf-8 -*-

import sys
import time
import json
import random
import asyncio
import aiohttp
import discord
import requests

client = discord.Client()

# - Configuration -

# Discord
prefix = 'Y$'
token = ''
channels = [] # Channel ID

# Bot
api_url = 'https://coinsmarkets.com/apicoin.php'
debug = False

# 起動時
@client.event
async def on_ready():
    print('[BOT] Yajucord Ready...')
    print('[BOT] Client-Username: ' + client.user.name)
    print('[BOT] Client-User-ID : ' + client.user.id)

    game = discord.Game(name='Coinsmarkets.com')
    await client.change_presence(game=game, status=discord.Status.online, afk=False)


# メッセージを受信した時
@client.event
async def on_message(message):
    if debug:
        print("[BOT][INFO] NEW MESSAGE !")
        print("[BOT][TEST] Author  : ", message.author)
        print("[BOT][TEST] Message : ", message.content)
        print("[BOT][TEST] Server  : ", message.server)
        print("[BOT][TEST] Channel： ", message.channel)

    if message.content.startswith(prefix + 'logout'):
        await client.send_message(message.channel, ":wave:")
        await client.logout()

    elif message.content.startswith(prefix + 'now'):
        msg = await client.send_message(message.channel, 'Coinsmarkets.com からYAJUCOINの情報を取得しています。しばらくお待ちください。')
        r = requests.get(api_url)

        # レスポンスが返ってきた場合
        if r.status_code == 200:
            # json を取得
            j = r.json()

            # キーを表示
            # print(j.keys())

            # yajucoin
            yaju = j['BTC_YAJU']
            yaju_sell = yaju['lowestAsk']
            yaju_buy = yaju['highestBid']

            # await client.send_message(message.channel, '最低売値: 1 YAJU / ' + yaju_sell + ' BTC')
            # await client.send_message(message.channel, '最高買値: 1 YAJU / ' + yaju_buy + ' BTC')

            await client.delete_message(msg)
            await client.send_message(message.channel,
                                      '最低売値: 1 YAJU / ' + yaju_sell + ' BTC\n' +
                                      '最高買値: 1 YAJU / ' + yaju_buy + ' BTC')

        # 失敗した場合
        else:
            await client.delete_message(msg)
            await client.send_message(message.channel, 'YAJUCOINの情報の取得に失敗したゾ...。 STATUS CODE: ' + r.status_code)
    elif message.content.startswith(prefix + 'btc'):
        msg = await client.send_message(message.channel, 'Coinsmarkets.com からYAJUCOINの情報を取得しています。しばらくお待ちください。')
        r = requests.get(api_url)

        # レスポンスが返ってきた場合
        if r.status_code == 200:
            # json を取得
            j = r.json()

            # yajucoin
            yaju = j['BTC_YAJU']
            yaju_buy = yaju['highestBid']

            #          1 BTC = 100000000 Satoshi
            # 0.00000001 BTC =         1 Satoshi
            # 取得できたので削除する
            await client.delete_message(msg)

            highestBid = float(yaju_buy)

            await client.send_message(message.channel,
                                      '1 YAJU を 今 BTC に替えると' + str(highestBid / 0.00000001) +
                                      ' Satoshi (' + str((highestBid / 0.00000001) / 100000000) + ' BTC) になるかもしれないゾ。\n')


    elif message.content.startswith(prefix + 'jpy'):
        msg = await client.send_message(message.channel, 'Coinsmarkets.com からYAJUCOINの情報を取得しています。しばらくお待ちください。')
        r = requests.get(api_url)

        # レスポンスが返ってきた場合
        if r.status_code == 200:
            # json を取得
            j = r.json()

            # yajucoin
            yaju = j['BTC_YAJU']
            yaju_buy = yaju['highestBid']

            #          1 BTC = 100000000 Satoshi
            # 0.00000001 BTC =         1 Satoshi

            # 取得できたので削除する
            await client.delete_message(msg)

            # to float
            highestBid = float(yaju_buy)

            # 1 BTC は 日本円 で ... ?
            zaif_url = 'https://api.zaif.jp/api/1/last_price/btc_jpy'
            rz = requests.get(zaif_url)

            if rz.status_code == 200:
                jz = rz.json()
                btc2jpy = jz['last_price']
                print(btc2jpy)
                one_jpy = float(btc2jpy)

                # YAJU -> BTC -> JPY
                await client.send_message(message.channel,
                                          "1 BTC は 現在 " + str(btc2jpy) + " 円 だゾ。\n" +
                                          "1 YAJU を 今 BTC に替えると" + str(highestBid) + " BTC になるかもしれないゾ。\n" +
                                          "そこから 日本円に替えると " + str(one_jpy * highestBid) + " 円 になるかもしれないゾ。" +
                                          "(手数料があるとは言っていない)")

        # 失敗した場合
        else:
            await client.delete_message(msg)
            await client.send_message(message.channel, 'YAJUCOINの情報の取得に失敗したゾ...。 STATUS CODE: ' + r.status_code)

    else:
        pass

client.run(token)
