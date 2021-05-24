import numpy as np 
import sys
import os
import pandas_datareader as web
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import torch

'''
Class to do the following
1. load data from Yahoo Finance
2. Partition data into batch sizes for train and test
3. Return batches as tensors 
'''

class load_data(): 

    def __init__(self,stock_alias): 
        self.stock_alias = stock_alias
        self.data = 0 
        self.batchSize = 0 

    
    def dataFromWeb(self,stock_source,start,end):


        self.data = web.DataReader(self.stock_alias, data_source=stock_source, start=start, end=end)

        print(self.data.info())

        print(self.data.head())

        self.data = self.data.filter(['Close']) # Data set is Close Prices 

        self.data=self.data.fillna(method='ffill')

        scaler = MinMaxScaler(feature_range=(-1, 1))
        self.data['Close'] = scaler.fit_transform(self.data['Close'].values.reshape(-1,1))
        return self.data, scaler
    

    def get_batches(self,batchSize): # returns data in batches as tensors 


        self.batchSize = batchSize

        data_raw = self.data.values # convert to numpy array
        
        data = []
        
        # create all possible sequences of length look_back
        for index in range(len(data_raw) - batchSize): 
            data.append(data_raw[index: index + batchSize])
        
        data = np.array(data)
        test_set_size = int(np.round(0.2*data.shape[0]))
        train_set_size = data.shape[0] - (test_set_size)
        
        x_train = data[:train_set_size,:-1,:]
        y_train = data[:train_set_size,-1,:]
        
        x_test = data[train_set_size:,:-1]
        y_test = data[train_set_size:,-1,:]

        # convert datasets to tensors 
        x_train = torch.from_numpy(x_train).type(torch.Tensor)
        x_test = torch.from_numpy(x_test).type(torch.Tensor)
        y_train = torch.from_numpy(y_train).type(torch.Tensor)
        y_test = torch.from_numpy(y_test).type(torch.Tensor)

        
        return [x_train, y_train, x_test, y_test]


        
        
        

