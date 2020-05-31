__author__ = "yen-nan ho"

import re
import os
import telegram
import pandas as pd
from flask import Flask, request
from telegram import ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from src.bot_agent import Agent
from arithmetic import seen_recommendation, similar_user_recommend, user_recommend_algorithm

class ChatBot(Agent):
    def __init__(self):
        self.logger = self.setup_logging(save_dir = "log")
        self.config = self.read_config("config.ini")
        self.initially_message()

    def call_m1(self, uid:int=1544):
        m1 = user_recommend_algorithm.Model(
            search_record_path = 'data/m1/0410-0416_user_history.csv',
            subscribed_data_path = 'data/m1/0319-0417_subscribe_wl.csv',
            stock_data_path = 'data/m1/ultimate_stock_data.csv' 
        )
        output = m1.get_recommend(uid = uid, rtype = 'stock_rank')
        rank_ls = list(output.head().values)
        rank_ls = ['{}({})'.format(i[0],i[1]) for i in rank_ls]
        rank_ls = ['']+rank_ls
        text = '\n• '.join(rank_ls)[1:]
        
        return text  #result_rank_edc.head().to_string(index = False, justify = 'left') 

    def call_m2(self, uid:int=123):
        m2 = similar_user_recommend.Model(
            weight_user_industry_path = 'data/m2/weight_user_industry.csv',
            subscribe_wl_path = 'data/m2/subscribe_wl.csv'
        )
        output = m2.recommendation(int(uid))

        output = ['']+output
        text = '\n• '.join(output)[1:]
        
        return text  #result_rank_edc.head().to_string(index = False, justify = 'left') 

    def call_m3(self, stock_id:int=9951):
        m3 = seen_recommendation.Model(
            views_recommend_path = "data/m3/views_recommend.json",
            subscribe_recommend_path = "data/m3/subscribe_recommend.json"
            )
        output = m3.recommend(stock_id)

        return output  #result_rank_edc.head().to_string(index = False, justify = 'left') 

    def start_bot(self):
        self.public_url = self.run_ngrok(path = "ngrok.exe")
        self.reset_result = self.reset_Webhook(config = self.config, url = self.public_url, logger=self.logger)

        app = Flask(__name__)

        # Initialize our ngrok settings into Flask
        app.config.from_mapping(
            BASE_URL = "http://localhost:5000",
            USE_NGROK = os.environ.get("USE_NGROK", "True"),
        )

        bot = telegram.Bot(token=self.config['TELEGRAM']['ACCESS_TOKEN'])

        @app.route('/hook', methods=['POST'])
        def webhook_handler():
            if request.method == "POST":
                update = telegram.Update.de_json(request.get_json(force=True), bot)
                text = update.message.text
                self.logger.info('========================================')
                self.logger.info('webhook - get message - {}'.format(text))
                # Update dispatcher process that handler to process this message
                dispatcher.process_update(update)
                
            return 'ok'

        def help_handler(bot, update):
            """Send a message when the command /help is issued."""
            update.message.reply_text(self.help_message)
            self.logger.info('help_handler - get help')

        def tool_handler(bot, update):
            """Send a message when the command /help is issued."""
            update.message.reply_text('tool',  reply_markup=self.reply_keyboard_markup)
            self.logger.info('tool_handler - get tool')

        def reply_handler(bot, update):
            text = update.message.text
            user_id = update.message.from_user.name
            if text.find('推薦股票') != -1:
                if re.match(r'推薦股票[ ,-]?\d+',text)!=None:
                    uid = re.search(r'\d+',text)[0]
                    try:
                        result = self.call_m1(uid = int(uid))
                        update.message.reply_markdown(result)
                    except:
                        update.message.reply_text('請輸入存在的用戶id。 \nex:1654、2153、6、62')

                        self.logger.info('uid error')
                else:
                    result = self.call_m1()
                    update.message.reply_markdown(result)

                    self.logger.info('reply_handler - reply - {}'.format(result))

            elif text.find('其他人也喜歡') != -1:
                if re.match(r'其他人也喜歡[ ,-]?\d+',text)!=None:
                    uid = re.search(r'\d+',text)[0]
                    try:
                        result = self.call_m2(uid = int(uid))
                        update.message.reply_markdown(result)
                    except:
                        update.message.reply_text('請輸入存在的用戶id。 \nex:1654、2153、6、62')

                        self.logger.info('uid error')
                else:
                    result = self.call_m2()
                    update.message.reply_markdown(result)
                    self.logger.info('reply_handler - reply - {}'.format(result))

            elif text.find('搜尋相關的股票') != -1:
                if re.match(r'搜尋相關的股票[ ,-]?\d+',text)!=None:
                    stock_id = re.search(r'\d+',text)[0]
                    try:
                        result = self.call_m3(stock_id= int(stock_id))
                        update.message.reply_markdown(result)
                    except:
                        update.message.reply_text('請輸入存在的股票id。 \nex:6456、4552')

                        self.logger.info('uid error')
                else:
                    result = self.call_m3()
                    update.message.reply_markdown(result)
                    self.logger.info('reply_handler - reply - {}'.format(result))

            else:
                update.message.reply_text('請輸入正確指令 \n1. /help \n2. /tool')
                self.logger.info('reply_handler - reply - 請輸入正確指令 \n1. /help \n2. /tool')

        def error_handler(bot, update, error):
            """Log Errors caused by Updates."""
            self.logger.error('Update "%s" caused error "%s"', update, error)
            update.message.reply_text('對不起伺服器出問題了 Q_Q') 
            self.logger.info('error_handler - get error')

        # This class dispatches all kinds of updates to its registered handlers.
        dispatcher = Dispatcher(bot, None)
        dispatcher.add_handler(CommandHandler(['help','start'], help_handler))
        dispatcher.add_handler(CommandHandler('tool', tool_handler))
        dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))   
        dispatcher.add_error_handler(error_handler)

        app.run()

    def initially_message(self):
        self.help_message = '/help : 可以看到所有指令 \n/tool : 會彈出功能視窗 \n\t   •推薦股票: 根據使用者的數位足跡推薦最近的5檔股票。(可自訂義 id: 推薦股票 1554)'
        self.reply_keyboard_markup = ReplyKeyboardMarkup([
                                            ['推薦股票'],
                                            ['其他人也喜歡'],
                                            ['搜尋相關的股票']
                                             ])
if __name__ == "__main__":
    Bot = ChatBot()
    Bot.start_bot()
