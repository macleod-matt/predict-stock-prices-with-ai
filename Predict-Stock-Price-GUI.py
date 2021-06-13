import re
from tkinter import *
import subprocess
from typing import Sized
import pandas as pd
import pandas_datareader as dr
from datetime import date

#for plotting stocks
import matplotlib.pyplot as plt
from loadData import load_data

#make a class

#First Window to open on launch
root = Tk()

AppTittle_lb = Label(root, text="Predict Stock Price App", font='bold')    #TickerSymb Label
AppTittle_lb.grid(row=0, column=0)                                         #Placement of Label

TickerSymb = Label(root, text="Please Enter Ticker Symbol Here:")   #TickerSymb Label
TickerSymb.grid(row=1, column=0)                                    #Placement of Label


Ticker_tb = Entry(root, width=7, borderwidth=4)     #Create Textbox
Ticker_tb.grid(row=1, column=1)                     #Placement of Textbox


#declear var to be used in TickerEnter()
TodaysHigh = "High"
TodaysLow = "Low"
TodaysOpen = "Open"
TodaysClose = "Close"
TodaysVolume = "Volume"

def TickerEntered():
    #***add try and Catch to check that the stock is tradeing today as the API doesn't work if it's not trading!
    StartDate = EndDate = "2021-06-10"

    #startDate = EndDate = str(date.today())
    df = dr.data.get_data_yahoo(Ticker_tb.get(), start=StartDate, end=EndDate)
    
    #set to global to allow fundemental textboxes to access them
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
    #print("Today's high: " + str(TodaysHigh))
    
    Obj_row = 4

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
    
GetFundementals_btn = Button(root, text="Click to see stock fundementals", padx=40, command=TickerEntered, bg="dark grey")
GetFundementals_btn.grid(row=2, column=0)

def myClick():  #What to do with button click
    try:
        SubprocessCall = "python3 train-predict-stock.py " +  Ticker_tb.get()   #Create sting to run program
        subprocess.call(SubprocessCall, shell=True)                             #Run AI program as subprogram
    except:
        print("Failed to run program please check that you have entered a valid ticker symbol")     #Program fail to run

myButton = Button(root, text="Click Here to Run AI Prediction", padx=40, command=myClick, bg="dark grey")     #Create button to execute program
myButton.grid()                                                                                         #Place button in the middle of the app

#Check Boxes
'''
AllDatesChecked = IntVar()

AllDates_cb = Checkbutton(root, text = "See All Dates")
AllDates_cb.grid(row=9, column=0)

SelectDateRangeChecked = IntVar()

SelectDateRange_cb = Checkbutton(root, text = "Select Date Range")
SelectDateRange_cb.grid(row=9, column=1)
'''



def AllDatesCommand():

    StartDate = '2012-01-01'
    EndDate = '2021-01-01'

    StockGraphData = dr.get_data_yahoo(Ticker_tb.get(), start = StartDate, end = EndDate)

    StockGraphData['Adj Close'].plot()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(Ticker_tb.get() + " Stock Chart")
    plt.show()
    return


def ViewStockChart(StartDateOption, EndDateOption):

    
    TodaysDate = date.today().month

    StartDate = str(StartDateOption) + '-01-01'
    EndDate = str(EndDateOption) + '-'+ str(date.today().month) +'-'+ str(date.today().day)

    try:
        StockGraphData = dr.get_data_yahoo(Ticker_tb.get(), start = StartDate, end = EndDate)

        StockGraphData['Adj Close'].plot()
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title(Ticker_tb.get() + " Stock Chart")
        plt.show()
    finally:
        print("The stock was not trading on or before the entered start date, " + str(StartDate) + ".  Please select a differnt start date.")
    return


def DateRangeCommand():

    DateRangeList = [
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

    StartDateOption = StringVar()
    StartDateOption.set("Please Select a Start Date")

    StartDateRange_om = OptionMenu(root, StartDateOption,  *DateRangeList)
    StartDateRange_om.grid(row=11, column=1)

    EndDateOption = StringVar()
    EndDateOption.set("Please Select a End Date")

    EndDateRange_om = OptionMenu(root, EndDateOption,  *DateRangeList)
    EndDateRange_om.grid(row=12, column=1)

    ViewStockChart_btn = Button(root, text="Click Here to See Stock Chart", command=lambda: ViewStockChart(StartDateOption.get(), EndDateOption.get()), padx=40, bg="dark grey")     #Create button to execute program
    ViewStockChart_btn.grid(row=13, column=1) 
    return

#Show date options once button is clicked
def ShowDateButtons():
    AllDate_btn = Button(root, text="See All Dates", command=AllDatesCommand, bg="dark grey")
    AllDate_btn.grid(row=10, column=0)

    DateRange_btn = Button(root, text="Select Date Range", command=DateRangeCommand, bg="dark grey")
    DateRange_btn.grid(row=10, column=1)
    return

#Button to view charts
ViewCharts_btn = Button(root, text="Click to View Charts", padx=70, command=ShowDateButtons, bg="dark grey")
ViewCharts_btn.grid(row=9, column=0)

root.mainloop()     #keep running until program is closed
