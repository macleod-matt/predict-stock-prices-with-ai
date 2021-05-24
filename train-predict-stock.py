'''
This Module will Train the RNN and predict results for individual stocks on yahoo finance
Notes: 
1. Script must be run with a NYSC stock alias as an input paramter e.g AAPL == Apple
2. If a trained model already exists i.e same params (stock alias, start, end) it will 
exist in the models directory. This will save time using program
3. If a model does not exist, the program must train a new dataset (will take 10mins - 1 hr depending on batch size ) 
4. The NN architecture description is found in myModel.py 
5. The final ouput will be dispalyed as a plot showing the AI attempting to predict the stock 
over the predicted start and end 

'''


import os
import math 
import numpy as np 
import pandas as pd
import torch 
from torch import nn as nn 
from torch.autograd import Variable
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import sys
from mymodel import myRNN # my imported NN class
from loadData import load_data


# Device config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# File paths 

curr_dir = os.getcwd() # get current working durectory 
data_set_path = curr_dir + '/Dataset/'
model_path = curr_dir + '/Models/'


# Hyperparameters

input_dim = 1
hidden_dim = 32
num_layers = 2 
output_dim = 1
learning_rate = 0.001
num_epochs = 100


'''
***************************
CALDER: Turn this into a GUI if you so choose

'''


# Stock Aquisition Parameters


try: 

    stock_alias = str(sys.argv[1]) # imput stock alias e.g AAPL = Apple, FB = Facebook 

except IndexError: 
    print("ERROR:  Must run script with a stock alias...\ne.g running with command: \"pyhton3 stock-predict.py IBM\" \
\n...This will run the predict the stock prices of IBM")
    exit()

stock_source = 'yahoo'
start = '2012-01-01'
end = '2021-01-01'
batchSize = 200


'''
***************************


'''



dataLoader =  load_data(stock_alias) # instantiate dataloader class constructor

# retrieve data and scalar value from stock choses from yahoo finance
data, scaler = dataLoader.dataFromWeb(stock_source,start,end) 

print(scaler)

# get train and test batches from data loader
x_train, y_train, x_test, y_test = dataLoader.get_batches(100)


''' 
****** Training ******

1. Program will attempt to load previosuly trained model. 
2. If it is unable to it will train a new model
3. New loss function will be plotted

'''


try:
    
    trained_model_path = model_path + '{}_{}_{}_TRAINED.pth'.format(stock_alias,start,end)
    
    model = myRNN(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

    model.load_state_dict(torch.load(trained_model_path))
    
    print("Loading Previously Trained Model:\n[{}] ".format(trained_model_path))

except FileNotFoundError: 
    
    
    print("\n******** Training Model For Stock Data ********* \n ")

    model = myRNN(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)



    # loss function -  Mean squared 

    criterion  = torch.nn.MSELoss()

    # optimizer - RMSprop 

    optimiser = torch.optim.RMSprop(model.parameters(), lr=learning_rate)


    hist = np.zeros(num_epochs)

    for i in range(num_epochs):

        
        # Forward pass
        y_train_pred = model(x_train)

        # calcualte loss function 

        loss = criterion(y_train_pred, y_train)

        if i % 10 == 0 and i !=0:
            print("EPOCH: [{}] | ERROR: [{}] ".format(i,loss.item()))
                
        # Zero out gradient, else they will accumulate between epochs
        optimiser.zero_grad()

        # Backward pass
        loss.backward()

        # Update parameters
        optimiser.step()

    # invert predictions
    y_train_pred = scaler.inverse_transform(y_train_pred.detach().numpy())
    trainScore = math.sqrt(mean_squared_error(y_train[:,0], y_train_pred[:,0]))
    print('Train RMSE: %.3f' % (trainScore))
    
    # Save Model For Multiple Use
    print("Saving model here: ", trained_model_path)
    torch.save(model.state_dict(), trained_model_path)

''' 

Predictions

''' 

y_test_pred = model(x_test)
# invert predictions
y_train = scaler.inverse_transform(y_train.detach().numpy())
y_test_pred = scaler.inverse_transform(y_test_pred.detach().numpy())
y_test = scaler.inverse_transform(y_test.detach().numpy())

# calculate RMS Error

testScore = math.sqrt(mean_squared_error(y_test[:,0], y_test_pred[:,0]))
print('Test RMSE: [%.3f] ' % (testScore))



''' 
**** PresentData **** 
For Calder 

'''


figure, axis = plt.subplots(figsize=(10, 5))

axis.plot(data[len(data)-len(y_test):].index, y_test, color = 'blue', label = 'Real {} Stock Price:'.format(stock_alias))
axis.plot(data[len(data)-len(y_test):].index, y_test_pred, color = 'green', label = 'Predicted {} Stock Price'.format(stock_alias))

plt.title('{} Stock Price Prediction'.format(stock_alias))
plt.xlabel('Period')
plt.ylabel('{} Stock Price'.format(stock_alias))
plt.legend()
plt.show()