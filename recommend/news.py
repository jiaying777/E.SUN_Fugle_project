import requests
import json
import time
from datetime import datetime
from random import sample,shuffle
from similar_user_recommend import subscription_list_recommendation

class WebCrawler:
    def __init__(self,user_id):
        self.url = "https://www.fugle.tw/api/v1/data/new_content/FCNT000050?symbol_id="
        self.symbolId = subscription_list_recommendation().recommend_all_list(user_id)
        shuffle(self.symbolId)
    
    def Crawler(self):
        '''推薦清單隨機挑選一間公司的今日的新聞'''
        output = []
        for symbolId in self.symbolId:
            text = requests.get(self.url+symbolId).json()
            try:
                newtime = datetime.strptime(text['rawContent'][0]['timestamp'][:10], "%Y-%m-%d")
            except KeyError:
                continue
            if newtime.date() == datetime.today().date():
                title = text['rawContent'][0]['title']
                url = text['rawContent'][0]['url']
                output.append([title,url])
                if len(output) == 3:
                    return output
            time.sleep(3)
        if len(output) != 0:
            return output
        return
        
    def symbolnews(self,symbolId):
        '''查詢個股最新的新聞'''
        text = requests.get(self.url+symbolId).json()
        try:
            title = text['rawContent'][0]['title']
            url = text['rawContent'][0]['url']
            return [title,url]
        except KeyError:
            return

    
if __name__ == '__main__':
    
    '''
    output[i][0]：新聞標題
    output[i][1]：新聞網址
    若是當天沒有新聞則回傳None
    '''
    WebCrawler = WebCrawler(123)
    output = WebCrawler.Crawler()
    print(output)
