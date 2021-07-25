@@ -0,0 +1,210 @@
from tkinter import *
import subprocess

import re
from typing import Sized
import pandas as pd
from pandas import DataFrame as dff
import pandas_datareader as dr
from datetime import date
# import pandas_datareader as web
#for plotting stocks
import matplotlib.pyplot as plt
from loadData import load_data

class Open_GUI():
    def __init__(self, master):
        self.master = master
        master.title("Stock Predict AI")

        #GUI Elements
        self.AppTittle_lb = Label(root, text="Predict Stock Price App", font='bold')    #TickerSymb Label
        self.AppTittle_lb.grid(row=0, column=0)                                         #Placement of Label

        self.TickerSymb = Label(root, text="Please Enter Ticker Symbol Here:")   #TickerSymb Label
        self.TickerSymb.grid(row=1, column=0)                                    #Placement of Label

        self.Ticker_tb = Entry(root, width=7, borderwidth=4)     #Create Textbox
        self.Ticker_tb.grid(row=1, column=1)                     #Placement of Textbox

        def TickerEntered():
         
            

            
            #declear var to be used in TickerEnter()
            TodaysHigh = "High"
            TodaysLow = "Low"
            TodaysOpen = "Open"
            TodaysClose = "Close"
            TodaysVolume = "Volume"


            start = '1950-01-01'

            dataLoader2 = load_data("GE")

            minOpen, maxOpen =  dataLoader2.dateMaxima('yahoo', start) # stock history 
            # put into calendar fields 


            print(minOpen,maxOpen) # delete me 

            '''

            #***add try and Catch to check that the stock is tradeing today as the API doesn't work if it's not trading!

            #add code to get connect high, low and stuff
            '''
            '''
            fundamentals = dataloader2.get_fundamentals(date) # custom date --recomend dateTime 
            TodaysHigh = fundamentals['High'] 
            TodaysLow = fundamentals['Low']
            TodaysOpen = fundamentals['Open']
            TodaysClose = fundamentals['Close']
            TodaysVolume = fundamentals['Volume']
            #print("Today's high: " + str(TodaysHigh))
            '''

            '''
            Obj_row = 4     #To keep control of rows

            #GUI Elements  
            StockHigh_lb = Label(root, text="High :")     #Create Label
            StockHigh_lb.grid(row=Obj_row, column=0)      #Placement of Label

            StockHigh_tb = Entry(root, width=7, borderwidth=0)     #Create Textbox
            StockHigh_tb.grid(row=Obj_row, column=1)                     #Placement of Textbox
            Obj_row += 1

            StockLow_lb = Label(root, text="Low :")     #Create Label
            StockLow_lb.grid(row=Obj_row, column=0)      #Placement of Label

            StockLow_tb = Entry(root, width=7, borderwidth=0)     #Create Textbox
            StockLow_tb.grid(row=Obj_row, column=1)                     #Placement of Textbox
            Obj_row += 1


            StockOpen_lb = Label(root, text="Open :")     #Create Label
            StockOpen_lb.grid(row=Obj_row, column=0)      #Placement of Label

            StockOpen_tb = Entry(root, width=7, borderwidth=0)     #Create Textbox
            StockOpen_tb.grid(row=Obj_row, column=1)                     #Placement of Textbox
            Obj_row += 1

            StockClose_lb = Label(root, text="Close :")     #Create Label
            StockClose_lb.grid(row=Obj_row, column=0)      #Placement of Label

            StockClose_tb = Entry(root, width=7, borderwidth=0)     #Create Textbox
            StockClose_tb.grid(row=Obj_row, column=1)                     #Placement of Textbox
            Obj_row += 1

            StockVol_lb = Label(root, text="Volume :")   #Create Label
            StockVol_lb.grid(row=Obj_row, column=0)      #Placement of Label

            StockVol_tb = Entry(root, width=7, borderwidth=0)       #Create Textbox
            StockVol_tb.grid(row=Obj_row, column=1)                       #Placement of Textbox
            Obj_row += 1
            #row 8


            #write the information into the textboxes
            StockHigh_tb.delete(0, END)
            StockHigh_tb.insert(0, str(TodaysHigh))

            StockLow_tb.delete(0, END)
            StockLow_tb.insert(0, str(TodaysLow))

            StockOpen_tb.delete(0, END)
            StockOpen_tb.insert(0, str(TodaysOpen))

            StockClose_tb.delete(0, END)
            StockClose_tb.insert(0, str(TodaysClose))

            StockVol_tb.delete(0, END)
            StockVol_tb.insert(0, str(TodaysVolume))
            '''

        self.GetFundementals_btn = Button(root, text="Click to see stock fundementals", padx=40, command=TickerEntered, bg="dark grey")
        self.GetFundementals_btn.grid(row=2, column=0)

        def myClick():  #What to do with button click
            try:
                SubprocessCall = "python3 train-predict-stock.py " +  Ticker_tb.get()   #Create sting to run program
                subprocess.call(SubprocessCall, shell=True)                             #Run AI program as subprogram
            except:
                print("Failed to run program please check that you have entered a valid ticker symbol")     #Program fail to run
    
        self.RunAI_btn = Button(root, text="Click Here to Run AI Prediction", padx=40, command=myClick, bg="dark grey")     #Create button to execute program
        self.RunAI_btn.grid() 

        def AllDatesCommand():
            #Use the get date class to get info
            return

        def ViewStockChart(StartDateOption, EndDateOption):
            #Use the get date class to get info
            return

        def DateRangeCommand():

            DateRangeList = [   #Get actual dates for when the stock is trading
                "2000",
                "2001",
                "2002",
                "2003",
                "2004",
                "2005",
                "2006",
                "2007",
                "2008",
                "2009",
                "2010",
                "2011",
                "2012",
                "2013",
                "2014",
                "2015",
                "2016",
                "2017",
                "2018",
                "2019",
                "2020",
                "2021"
            ]

            ### start date drop down menu

            #First Element of drop down menu
            self.StartDateOption = StringVar()
            self.StartDateOption.set("Please Select a Start Date")

            #Fill items of drop Start date down menu
            self.StartDateRange_om = OptionMenu(root, StartDateOption,  *DateRangeList)
            self.StartDateRange_om.grid(row=11, column=1)

            ### end date drop down menu

            self.EndDateOption = StringVar()
            self.EndDateOption.set("Please Select a End Date")

            self.ViewStockChart_btn = Button(root, text="Click Here to See Stock Chart", command=lambda: ViewStockChart(StartDateOption.get(), EndDateOption.get()), padx=40, bg="dark grey")     #Create button to execute program
            self.ViewStockChart_btn.grid(row=13, column=1) 
            return
        
        #Show date options once button is clicked
        def ShowDateButtons():
            AllDate_btn = Button(root, text="See All Dates", command=AllDatesCommand, bg="dark grey")
            AllDate_btn.grid(row=10, column=0)

            DateRange_btn = Button(root, text="Select Date Range", command=DateRangeCommand, bg="dark grey")
            DateRange_btn.grid(row=10, column=1)
            return
        
        #Button to view charts
        self.ViewCharts_btn = Button(root, text="Click to View Charts", padx=70, command=ShowDateButtons, bg="dark grey")
        self.ViewCharts_btn.grid(row=9, column=0)

root = Tk()
my_gui = Open_GUI(root)
root.mainloop()