# -*- coding: utf-8 -*-
__author__ = "chia-ying wu"

import pickle
class userdata:
    def __init__(self, user_data_path):
        self.user_data_path = user_data_path
        self.df = self.load_data()

    def load_data(self):
        with open(self.user_data_path, 'rb') as file:
            df = pickle.load(file)
        return df
            
    def write(self, user_id, input_id, user_name):
        self.df[user_id] = {'id': input_id, 'name':user_name}
        with open(self.user_data_path, 'wb') as f:
            pickle.dump(self.df, f)