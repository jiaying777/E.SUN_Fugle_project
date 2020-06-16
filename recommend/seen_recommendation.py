__author__ = "chia-ying wu"

import pandas as pd
import json
from random import sample

class seen_recommendation:
    def __init__(self):
        with open("views_recommend.json","r") as f:
            self.views_recommend = json.load(f)
            self.views_recommend = json.loads(self.views_recommend)
        with open("subscribe_recommend.json","r") as f:
            self.subscribe_recommend = json.load(f)
            self.subscribe_recommend = json.loads(self.subscribe_recommend)
            
            
    def recommend(self,symbolId):
        symbolId = str(symbolId)
        if symbolId in self.subscribe_recommend.keys():
            output = sample(self.subscribe_recommend[symbolId],1)[0]
            return output
        elif symbolId in self.views_recommend.keys():
            output = sample(self.views_recommend[symbolId],1)[0]
            return output
        
if __name__ == '__main__':
    recommendation = seen_recommendation()
    output = recommendation.recommend('9951')
    print(output)