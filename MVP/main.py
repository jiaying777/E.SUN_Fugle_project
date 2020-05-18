import os
import telegram
import pandas as pd
from flask import Flask, request
from telegram import ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from src.bot_agent import Agent
from user_recommend_algorithm import RecommendModel

class ChatBot(Agent):
    def __init__(self):
        self.logger = self.setup_logging(save_dir = "log")
        self.config = self.read_config("config.ini")
        self.public_url = self.run_ngrok(path = "ngrok.exe")
        self.reset_result = self.reset_Webhook(config = self.config, url = self.public_url, logger=self.logger)
        self.initially_message()

    def call_user_recommend_algorithm(self):
        stock_model_num = RecommendModel(
            search_record_path = 'data/0410-0416_user_history.csv',
            subscribed_data_path = 'data/0319-0417_subscribe_wl.csv',
            stock_data_path = 'data/ultimate_stock_data.csv' 
        )
        result_rank_edc = stock_model_num.get_recommend(1544, rtype='stock_rank')
        rank_ls = list(result_rank_edc.head().values)
        rank_ls = ['{}({})'.format(i[0],i[1]) for i in rank_ls]
        rank_ls = ['']+rank_ls
        text = '\n- '.join(rank_ls)[1:]
        
        return text  #result_rank_edc.head().to_string(index = False, justify = 'left') 


    def start_bot(self):
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
            update.message.reply_text('tool',  reply_markup=self.reply_keyboard_markup, pinned_message='123')
            self.logger.info('tool_handler - get tool')

        def reply_handler(bot, update):
            text = update.message.text
            user_id = update.message.from_user.name
            if text=='推薦股票':
                result = self.call_user_recommend_algorithm()
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
        self.help_message = '1. /help\n 2. /tool'
        self.reply_keyboard_markup = ReplyKeyboardMarkup([
                                            ['推薦股票'],
                                            ['推薦股票2']
                                             ])
if __name__ == "__main__":
    Bot = ChatBot()
    Bot.start_bot()
