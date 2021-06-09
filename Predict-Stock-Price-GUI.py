from tkinter import *
import subprocess

root = Tk()

e = Entry(root, width=7, borderwidth=0)
TickerSymb = Label(root, text="Please Enter Ticker Symbol Here:")

TickerSymb.grid(row=0, column=0)
e.grid(row=0, column=1)

def myClick():
    SubprocessCall = "python3 train-predict-stock.py " +  e.get()
    subprocess.call(SubprocessCall, shell=True)

myButton = Button(root, text="Click Here to Run Program", padx=40, command=myClick, bg="dark grey")
myButton.grid()

root.mainloop()