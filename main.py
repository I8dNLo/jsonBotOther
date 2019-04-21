#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pandas import Series
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! I'm geojsonbot.\n Just send be geojson and i will return csv with object counts.")

def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', bot, update.error)

def count_objects(filename):
    with open(f'in/{filename}.geojson', "r", encoding="utf-8") as f:
        dct = json.load(f)

    s = Series(map(lambda x: x['geometry']['type'], dct['features'])).value_counts()
    path_out = f"out/object_count.csv"
    s.to_csv(path_out)
    return path_out

def doc(bot, update):
    file = bot.getFile(update.message.document.file_id)
    file_id = str(update.message.document.file_id)
    print (f"file_id: {file_id}")
    file.download(f'in/{file_id}.geojson')
    try:
        out = count_objects(file_id)
        bot.send_document(chat_id=update.message.chat_id, document=open(out, 'rb'))
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Something wrong with file. This bot excepts only geojson format.")

def main():
    with open("token.txt", "r") as f:
        token = f.readline()
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, doc))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
