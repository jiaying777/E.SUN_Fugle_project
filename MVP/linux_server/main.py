# -*- coding: utf-8 -*-
__author__ = "yen-nan ho"

import re
import os
import telegram
import pandas as pd
from random import sample
from fugle_realtime import intraday
from flask import Flask, request
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from src.bot_agent import Agent
from src.user_agent import userdata
from arithmetic import seen_recommendation, similar_user_recommend, user_recommend_algorithm

class ChatBot(Agent):
    def __init__(self):
        self.logger = self.setup_logging(save_dir = "log")
        self.config = self.read_config("config.ini")
        self.user = userdata("data/user/userid.pickle")
        self.stock = pd.read_pickle('data/m2/stock.pickle')

    def call_m1(self, uid:int=1544):
        m1 = user_recommend_algorithm.Model(
            search_record_path = 'data/m1/0410-0416_user_history.csv',
            subscribed_data_path = 'data/m1/0319-0417_subscribe_wl.csv',
            stock_data_path = 'data/m1/ultimate_stock_data.csv' 
        )
        output = m1.get_recommend(uid = uid, rtype = 'stock_rank')
        rank_ls = list(output.head().values)

        button = InlineKeyboardMarkup([[InlineKeyboardButton(str(i[1]), callback_data='stock {}'.format(i[1])) for i in rank_ls]])
        
        rank_ls = ['{}({})'.format(i[0],i[1]) for i in rank_ls]
        rank_ls = ['']+rank_ls
        text = '\n▸ '.join(rank_ls)[1:]
        
        return text, button  #result_rank_edc.head().to_string(index = False, justify = 'left') 

    def call_m2(self, uid:int=123):
        m2 = similar_user_recommend.Model(
            weight_user_industry_path = 'data/m2/weight_user_industry.csv',
            subscribe_path = 'data/m2/subscribe.pickle',
            stock_data_path = 'data/m2/stock.pickle'
        )
        output = m2.recommendation(int(uid))
        
        button = InlineKeyboardMarkup([[InlineKeyboardButton(str(i), callback_data='stock {}'.format(i)) for i in output]])

        for i in range(len(output)):
            try:
                name = m2.stock.loc[m2.stock['證券代碼']==str(output[i]),'證券名稱'].values[0]
            except:
                name = ''
            output[i] = '{}({})'.format(name, output[i])

        output = ['']+output
        text = '\n▸ '.join(output)
        
        return text, button  #result_rank_edc.head().to_string(index = False, justify = 'left') 

    def call_m3(self, stock_id:int=9951):
        m3 = seen_recommendation.Model(
            views_recommend_path = "data/m3/views_recommend.json",
            subscribe_recommend_path = "data/m3/subscribe_recommend.json"
            )
        output = m3.recommend(stock_id)

        return output  #result_rank_edc.head().to_string(index = False, justify = 'left') 

    def get_stock_info(self, num):
        data = intraday.meta(apiToken=self.config['FUGLE']['fugle_TOKEN'] , symbolId=num , output='raw')
        # data = intraday.meta(apiToken=Bot.config['FUGLE']['fugle_TOKEN'] , symbolId='0050', output='raw')
        df1 = intraday.chart(apiToken=self.config['FUGLE']['fugle_TOKEN'] , symbolId=num)
        # df1 = intraday.chart(apiToken=Bot.config['FUGLE']['fugle_TOKEN'] , symbolId='0050')
        if 'error' in df1.columns:
            return '請輸入正確的股票代碼：'
        elif df1.shape[0] == 0:
            if  'nameZhTw' not in data:
                text = 'api 無回應'
            elif 'industryZhTw' in data:
                text = "【{}({})】  \n⦁ 產業: {} \n⦁ 開盤股價: {}  \n⦁ 昨日漲停價: {} \n⦁ 昨日跌停價: {} ".format(
                                                                        data['nameZhTw'],
                                                                        num, 
                                                                        data['industryZhTw'],
                                                                        data['priceReference'],
                                                                        data['priceHighLimit'],
                                                                        data['priceLowLimit']
                                                                    )
            else:
                text = "【{}({})】  \n⦁ 開盤股價: {}  \n⦁ 昨日漲停價: {} \n⦁ 昨日跌停價: {} ".format(
                                                                        data['nameZhTw'],
                                                                        num, 
                                                                        data['priceReference'],
                                                                        data['priceHighLimit'],
                                                                        data['priceLowLimit']
                                                                    )
            return text
        else:               
            df1 = df1.iloc[-1]
            if 'industryZhTw' in data:
                text = "【{}({})】  \n⦁ 產業: {} \n⦁ 當前股價: {}  \n⦁ 今日漲跌: {}({}%) ".format(
                                                                        data['nameZhTw'],
                                                                        num, 
                                                                        data['industryZhTw'],
                                                                        df1['close'],
                                                                        round(df1['close']-data['priceReference'], 2),
                                                                        round(((df1['close']-data['priceReference'])/data['priceReference'])*100, 2)
                                                                    )
            else:
                text = "【{}({})】  \n⦁ 當前股價: {}  \n⦁ 今日漲跌: {}({}%) ".format(
                                                                        data['nameZhTw'],
                                                                        num, 
                                                                        df1['close'],
                                                                        round(df1['close']-data['priceReference'], 2),
                                                                        round(((df1['close']-data['priceReference'])/data['priceReference'])*100, 2)
                                                                    )

            return text


    def start_bot(self):
        self.initially_message()
        self.public_url = self.run_ngrok(path = "ngrok", config = self.config)
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
                try:
                    if DEBUG:
                        print('|message|', update.message, '\n')
                        print('|callback_query|', update.callback_query, '\n')
                    if update.message == None:
                        text = update.callback_query.data
                        self.logger.info('========================================')
                        self.logger.info('webhook - get message(callback) - {}'.format(text))
                    else:
                        text = update.message.text
                        self.logger.info('========================================')
                        self.logger.info('webhook - get message - {}'.format(text))
                    # Update dispatcher process that handler to process this message
                except:
                    self.logger.error('webhook - get unknow message!')
                dispatcher.process_update(update)  
                
            return 'ok'

        def start_handler(bot, update):
            if update.message.chat.id not in self.user.df.keys():
                bot.send_message(update.message.chat.id,
                                '{} 您好，請輸入id：\n(假設ID為 1111，請輸入: 1111)'.format(update.message.from_user.name))
            else:
                bot.send_message(update.message.chat.id,
                                '{} 您好，當前用戶ID:{} ，輸入 /help 查看更多指令。'.format(
                                                            update.message.from_user.name,
                                                            self.user.df[update.message.chat.id]['id']
                                                            )
                                )
        def id_handler(bot, update):
            del self.user.df[update.message.chat.id] 
            bot.send_message(update.message.chat.id,
                                '{} 您好，請輸入新的id：\n(假設ID為 1111，請輸入： 1111)'.format(update.message.from_user.name))
        
        def ButtonCallback_handler(bot, update):
            order, sid = update.callback_query.data.split(' ')
            user_name = update.callback_query.from_user.first_name + update.callback_query.from_user.last_name # update.message.from_user.first_name
            user_id = update.callback_query.from_user.id

            if order == 'stock':
                text = self.get_stock_info(num = str(sid))
                url = 'https://www.fugle.tw/ai/{}?'.format(sid)
                button = InlineKeyboardMarkup([
                                [
                                    InlineKeyboardButton('更多基本資訊', callback_data='info {}'.format(sid)),
                                    InlineKeyboardButton('最新一筆交易', callback_data='trade {}'.format(sid))
                                    ],
                                [
                                    InlineKeyboardButton('推薦相關股票', callback_data='recommend {}'.format(sid)),
                                    InlineKeyboardButton('前往網站', url=url)
                                    ]])
                bot.send_message(user_id, text,
                                # reply_to_message_id = update.message.message_id,
                                reply_markup = button
                                    )

            if order == 'recommend':
                try:
                    result = self.call_m3(stock_id= int(sid))
                    text = self.get_stock_info(num = str(result))
                    url = 'https://www.fugle.tw/ai/{}?'.format(result)
                    button = InlineKeyboardMarkup([
                                    [
                                        InlineKeyboardButton('更多基本資訊', callback_data='info {}'.format(result)),
                                        InlineKeyboardButton('最新一筆交易', callback_data='trade {}'.format(result))
                                        ],
                                    [
                                        InlineKeyboardButton('推薦相關股票', callback_data='recommend {}'.format(result)),
                                        InlineKeyboardButton('前往網站', url=url)
                                        ]])
                    bot.send_message(user_id, text,
                                        reply_to_message_id = update.callback_query.message.message_id,
                                        reply_markup = button
                                        )
                    self.logger.info("user_name{} | respond_text:{}".format(user_name, text))

                except:
                    update.message.reply_text('請輸入存在的股票id。 \nex:6456、4552')
                    self.logger.info('m3 - uid error')

            if order == 'info':
                data = intraday.meta(apiToken=self.config['FUGLE']['fugle_TOKEN'] , symbolId=sid , output='raw')
                # data = intraday.meta(apiToken=Bot.config['FUGLE']['fugle_TOKEN'] , symbolId='0050' , output='raw')
                try:
                    if 'industryZhTw' in data:
                        text = ('【'+data['nameZhTw']+'('+sid+')'+' 基本資訊】 \n  ⦁ 產業別：'+data['industryZhTw']+'\n  ⦁ 交易幣別：'+data['currency']+'\n  ⦁ 股票中文簡稱：'+data['nameZhTw']+'\n  ⦁ 開盤參考價：'+ str(data['priceReference'])+
                        '\n  ⦁ 漲停價：'+str(data[ 'priceHighLimit'])+'\n  ⦁ 跌停價：'+str(data["priceLowLimit"])+'\n  ⦁ 股票類別：'+data['typeZhTw'])              
                    else:
                        text = ('【'+data['nameZhTw']+'('+sid+')'+' 基本資訊】 \n  ⦁ 交易幣別：'+data['currency']+'\n  ⦁ 股票中文簡稱：'+data['nameZhTw']+'\n  ⦁ 開盤參考價：'+ str(data['priceReference'])+
                        '\n  ⦁ 漲停價：'+str(data[ 'priceHighLimit'])+'\n  ⦁ 跌停價：'+str(data["priceLowLimit"])+'\n  ⦁ 股票類別：'+data['typeZhTw'])
                except:
                    text = '查無此代碼'
                update.callback_query.message.reply_text(text)
                

            if order == 'trade':
                data = intraday.meta(apiToken=self.config['FUGLE']['fugle_TOKEN'] , symbolId=sid , output='raw')
                
                dt = intraday.quote(apiToken=self.config['FUGLE']['fugle_TOKEN'], symbolId=sid, output='raw')
                # intraday.quote(apiToken=Bot.config['FUGLE']['fugle_TOKEN'], symbolId=num, output='raw')
                if 'trade' in dt.keys():
                    trade = dt['trade']
                    text = ('【'+data['nameZhTw']+'('+sid+')'+' 最新一筆交易】 \n'+'  ⦁ 成交價：'+str(trade['price'])+
                            '\n  ⦁ 成交張數：'+str(trade['unit'])+'\n  ⦁ 成交量：'+str(trade['volume'])+'\n  ⦁ 成交序號：'+str(trade['serial']))
                else:
                    text = '查無最新資訊'
                update.callback_query.message.reply_text(text)

        def help_handler(bot, update):
            """Send a message when the command /help is issued."""
            update.message.reply_text(self.help_message)
            self.logger.info('help_handler - get help')

        def tool_handler(bot, update):
            """Send a message when the command /help is issued."""
            update.message.reply_text('tool',  reply_markup = self.reply_keyboard_markup_for_tool)
            self.logger.info('tool_handler - get tool')

        def reply_handler(bot, update, input_num = None):
            text = update.message.text
            user_name = update.message.from_user.first_name + update.message.from_user.last_name 
            user_id = update.message.chat.id
            
            have_num = re.search(r'\d+',text)!=None
            if have_num:
                input_num = re.search(r'\d+',text)[0]

            if user_id not in self.user.df.keys():
                if have_num != None:
                    if input_num != None:
                        if int(input_num) in self.user.df['userid']:
                            try:
                                self.user.write(user_id = user_id,
                                                input_id = input_num,
                                                user_name = user_name)
                                self.logger.info("new id login:{} | userid:{} | user_name{}".format(user_id, input_num, user_name))
                                update.message.reply_text('登入成功 ID：{} , 輸入 /help 查看更多指令'.format(input_num))
                            except:
                                self.logger.error("new id false to add to database!:".format(text))
                        else:
                            user_txt = '、'.join([str(i) for i in sample(self.user.df['userid'], 3)])
                            bot.send_message(user_id, '查無此 ID ，可以嘗試輸入以下 ID: ' + user_txt)
                    else:
                        bot.send_message(user_id, '請輸入正確格式(假設ID為 1111，請輸入：1111)')
                else:
                    bot.send_message(user_id, '請輸入正確格式(假設ID為 1111，請輸入：1111)')
            else:
                if text.find('推薦股票') != -1:
                    if re.match(r'推薦股票[ ,-]?\d+',text)!=None:
                        uid = re.search(r'\d+',text)[0]
                        try:
                            result, button = self.call_m1(uid = uid)
                            bot.send_message(user_id, result,
                                            # reply_to_message_id = update.message.message_id,
                                            reply_markup = button
                                            )
                            self.logger.info('reply_handler - reply - {}'.format(result))
                        except:
                            update.message.reply_text('用戶 id - {} 查無資訊'.format(self.user.df[user_id]['id']))
                            self.logger.info('uid error')
                    else:
                        try:
                            result, button = self.call_m1(uid = int(self.user.df[user_id]['id']))
                            bot.send_message(user_id, result,
                                            # reply_to_message_id = update.message.message_id,
                                            reply_markup = button
                                            )
                            self.logger.info('reply_handler - reply - {}'.format(result))
                        except:
                            update.message.reply_text('用戶 id - {} 查無資訊'.format(self.user.df[user_id]['id']))
                            self.logger.info('uid error')

                        

                elif text.find('其他人也喜歡') != -1:
                    if re.match(r'其他人也喜歡[ ,-]?\d+',text)!=None:
                        uid = re.search(r'\d+',text)[0]
                        try:
                            result, button = self.call_m2(uid = int(uid))
                            bot.send_message(user_id, result,
                                            # reply_to_message_id = update.message.message_id,
                                            reply_markup = button
                                            )
                        except:
                            update.message.reply_text('用戶 id - {} 查無資訊'.format(self.user.df[user_id]['id']))
                            self.logger.info('uid error')
                    else:
                        try:
                            result, button = self.call_m2(uid = int(self.user.df[user_id]['id']))
                            bot.send_message(user_id, result,
                                            # reply_to_message_id = update.message.message_id,
                                            reply_markup = button
                                            )
                            self.logger.info('reply_handler - reply - {}'.format(result))
                        except:
                            update.message.reply_text('用戶 id - {} 查無資訊'.format(self.user.df[user_id]['id']))
                            self.logger.info('uid error')   

                elif have_num: 
                    try:
                        text = self.get_stock_info(num = str(input_num))
                        url = 'https://www.fugle.tw/ai/{}?'.format(input_num)
                        button = InlineKeyboardMarkup([
                                        [
                                            InlineKeyboardButton('更多基本資訊', callback_data='info {}'.format(input_num)),
                                            InlineKeyboardButton('最新一筆交易', callback_data='trade {}'.format(input_num))
                                            ],
                                        [
                                            InlineKeyboardButton('推薦相關股票', callback_data='recommend {}'.format(input_num)),
                                            InlineKeyboardButton('前往網站', url=url)
                                            ]])
                        bot.send_message(user_id, text,
                                        # reply_to_message_id = update.message.message_id,
                                        reply_markup = button
                                        )
                        self.logger.info("user_name{} | respond_text:{}".format(user_name, text))
                    except:
                        bot.send_message(user_id, '查詢不到該股票代碼!')
                        self.logger.error("get stock info error")

                elif text.strip() in self.stock['證券名稱'].values:
                    sid = self.stock.loc[self.stock['證券名稱']==text.strip(),'證券代碼'].values[0]
                    # sid = Bot.stock.loc[Bot.stock['證券名稱']==text.strip(),'證券代碼'].values[0]
                    try:
                        text = self.get_stock_info(num = str(sid))
                        url = 'https://www.fugle.tw/ai/{}?'.format(sid)
                        button = InlineKeyboardMarkup([
                                        [
                                            InlineKeyboardButton('更多基本資訊', callback_data='info {}'.format(sid)),
                                            InlineKeyboardButton('最新一筆交易', callback_data='trade {}'.format(sid))
                                            ],
                                        [
                                            InlineKeyboardButton('推薦相關股票', callback_data='recommend {}'.format(sid)),
                                            InlineKeyboardButton('前往網站', url=url)
                                            ]])
                        bot.send_message(user_id, text,
                                        # reply_to_message_id = update.message.message_id,
                                        reply_markup = button
                                        )
                        self.logger.info("user_name{} | respond_text:{}".format(user_name, text))
                    except:
                        bot.send_message(user_id, '查詢不到該股票代碼!')
                        self.logger.error("get stock info error")
                else:
                    update.message.reply_text('輸入 /help 查看正確指令')
                    self.logger.info('reply_handler - reply - 請輸入正確指令...')

        def error_handler(bot, update, error):
            """Log Errors caused by Updates."""
            self.logger.error('Update {} caused \n>> error {}'.format(update, error))
            if update.message == None:
                bot.send_message(update.callback_query.message.message_id, '對不起伺服器出問題了 Q_Q')
            else:
                update.message.reply_text('對不起伺服器出問題了 Q_Q')

        # This class dispatches all kinds of updates to its registered handlers.
        dispatcher = Dispatcher(bot, None)
        dispatcher.add_handler(CommandHandler(['start', 'myid'], start_handler))
        dispatcher.add_handler(CommandHandler('setid', id_handler))
        dispatcher.add_handler(CommandHandler('help', help_handler))
        dispatcher.add_handler(CommandHandler('tool', tool_handler))
        dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))  
        dispatcher.add_handler(CallbackQueryHandler(ButtonCallback_handler)) 
        dispatcher.add_error_handler(error_handler)

        app.run()

    def initially_message(self):
        self.help_message = (
                            '【指令】\n'+  
                            ' /help : 可以看到所有指令 \n'+
                            ' /tool : 會彈出功能視窗 \n'+
                            ' /myid : 可以查看當前登入的 id \n'+
                            ' /setid : 可以更改當前登入的 id \n\n'+
                            '【基本搜尋】\n'+
                            ' 輸入股票代碼: 回傳該股票的股價和漲跌，可以進一步查看該股票之其他資訊。像是:\n\n'+
                            ' ✔『更多基本資訊』: 串接 fugle api，提供該股基本訊息，包括產業別、交易幣別、開盤參考價...。 \n\n'+
                            ' ✔『最新一筆交易』: 串接 fugle api，提供最新一筆交易資訊，包括成交價成、交張數...。 \n\n'+
                            ' ✔『推薦相關股票』: 以該查詢股票特質，找尋相關股票推薦。  \n\n'+
                            ' ✔『前往網站』: 開啟該股票在 fugle 的網站頁面。  \n\n'
                            )
                            

        self.reply_keyboard_markup_for_tool = ReplyKeyboardMarkup([
                                            ['推薦股票'],
                                            ['其他人也喜歡']
                                                ])
if __name__ == "__main__":
    DEBUG = False
    Bot = ChatBot()
    Bot.start_bot()
