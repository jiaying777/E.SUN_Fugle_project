import os
import sys
import time
import logging
import requests
import datetime
import configparser
from pyngrok import ngrok

class Agent:
    def run_ngrok(self, path:str, port:int = 5000):
        ngrok.DEFAULT_NGROK_PATH = path

        if len(ngrok.get_tunnels())!=0:
            ngrok.kill()

        # Open a ngrok tunnel to the dev server
        public_url = ngrok.connect(port)
        public_url = public_url.replace('http:','https:')

        print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, port))

        return public_url

    def reset_Webhook(self, config, url:str, logger):
        access_token = config['TELEGRAM']['ACCESS_TOKEN']
        delete_result = requests.post('https://api.telegram.org/bot'+access_token+'/deleteWebhook').text
        set_result = requests.post('https://api.telegram.org/bot'+access_token+'/setWebhook?url='+url+'/hook').text
        logger.info('reset webhook\n {}'.format(set_result))
        
        return {'delete_result': delete_result, 'set_result': set_result}

    def mkdir(self, path):
        if not os.path.exists(path):
            print ('Crate folder at -> %s' %(path))
            os.makedirs(path)

    def setup_logging(self, save_dir:str='', debug = False):
                # Enable logging
        path = os.path.join(save_dir, datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M_%S"))
        try:
            self.mkdir(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        if not os.path.isdir(save_dir):
            print('Please create saved directoray at "{}"'.format(save_dir))
            exit()
        
        if debug == True:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=log_level, filename = os.path.join(path, 'logging.txt'))
        logger = logging.getLogger(__name__)

        return logger

    def read_config(self, path:str):
        config = configparser.ConfigParser()
        config.read(path)

        return config

