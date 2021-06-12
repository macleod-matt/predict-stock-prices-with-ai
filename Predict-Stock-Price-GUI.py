from tkinter import *
import subprocess
from typing import Sized
import pandas as pd
import pandas_datareader as dr
from datetime import date

#make a class

#First Window to open on launch
root = Tk()

AppTittle_lb = Label(root, text="Predict Stock Price App", font='bold')   #TickerSymb Label
AppTittle_lb.grid(row=0, column=0)                                    #Placement of Label

TickerSymb = Label(root, text="Please Enter Ticker Symbol Here:")   #TickerSymb Label
TickerSymb.grid(row=1, column=0)                                    #Placement of Label

e = Entry(root, width=7, borderwidth=4)     #Create Textbox
e.grid(row=1, column=1)                     #Placement of Textbox


TodaysHigh = "High"
TodaysLow = "Low"
TodaysOpen = "Open"
TodaysClose = "Close"
TodaysVolume = "Volume"


def TickerEntered():
    startDate = EndDate = str(date.today())
    df = dr.data.get_data_yahoo(e.get(), start=startDate, end=EndDate)
    
    global TodaysHigh
    global TodaysLow
    global TodaysOpen
    global TodaysClose
    global TodaysVolume
    
    TodaysHigh = df['High'][EndDate]
    TodaysLow = df['Low'][EndDate]
    TodaysOpen = df['Open'][EndDate]
    TodaysClose = df['Close'][EndDate]
    TodaysVolume = df['Volume'][EndDate]
    print("Today's high: " + str(TodaysHigh))
    
    
TodaysHigh_lb = Label(root, text=str(TodaysHigh))   #TickerSymb Label
TodaysHigh_lb.grid(row=3, column=0)                      #Placement of Label

GetFundementals_btn = Button(root, text="Click to see stock fundementals", padx=40, command=TickerEntered, bg="dark grey")
GetFundementals_btn.grid(row=2, column=0)

def myClick():  #What to do with button click
    try:
        SubprocessCall = "python3 train-predict-stock.py " +  e.get()   #Create sting to run program
        subprocess.call(SubprocessCall, shell=True)                     #Run AI program as subprogram
    except:
        print("Failed to run program please check that you have entered a valid ticker symbol")     #Program fail to run

myButton = Button(root, text="Click Here to Run Program", padx=40, command=myClick, bg="dark grey")     #Create button to execute program
myButton.grid()                                                                                         #Place button in the middle of the app

root.mainloop()     #keep running until program is closed
