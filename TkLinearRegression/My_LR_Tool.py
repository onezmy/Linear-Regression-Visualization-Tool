# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 17:11:02 2023

@author: Sam Zhang
"""

# import functions
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.tix import *
import tkinter.font as tkFont
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


"""
init data
"""
X = []
Y = []
data = []
df = {}
max_iter = 1000
tol = 1e-5

"""
define functions for UI
"""
def show_all():
    """
    print new data in the window
    """
    list_X.delete(0,END)
    list_Y.delete(0,END)
    for x in X:
        list_X.insert(END, x)
    for y in Y:
        list_Y.insert(END, y)
    
def add():
    """
    function for add button, update the data then show new data in window
    """
    x = input_X.get()
    y = input_Y.get()
    X.append(x)
    Y.append(y)
    data.append(tuple([x,y]))
    show_all()
    points_plot()
    
    
def remove():
    """
    function for remove button, update the data then show new data in window
    """
    global X,Y,data
    x = input_X.get()
    y = input_Y.get()
    if (x,y) in data:
        idx = data.index((x,y))
        X = X[:idx] + X[idx+1:]
        Y = Y[:idx] + Y[idx+1:]
        data = data[:idx] + data[idx+1:]
        show_all()
        points_plot()

def clear_points_plot():
      for widget in window.winfo_children():
           if "Canvas" in str(type(widget)):
              widget.destroy()


def points_plot():
    X = list(list_X.get(0,list_X.size()-1))
    Y = list(list_Y.get(0,list_Y.size()-1))
    if len(X) == 0:
        return
    df['X'] = X
    df['Y'] = Y
    clear_points_plot()
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(X,Y,c="#7E95F2", s = 1)
    ax.set_title("Linear Regression")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    canvas1 = FigureCanvasTkAgg(fig,master=window)
    canvas1.draw()
    canvas1.get_tk_widget().pack()


"""
init window
"""
window = Tk()
window.title("Linear Regression")
window.geometry("1400x500")



"""
define fonts
"""
font_yh1 = tkFont.Font(family='microsoft yahei', size=12, weight='bold')
font_yh2 = tkFont.Font(family='microsoft yahei', size=8, weight='bold')



"""
add buttons/labels
"""

# 'Enter X' label
Enter_X = tk.Label(window,text="Enter X: ",anchor="w", font=font_yh1)
Enter_X.place(x=50,y=50,width=100)
input_X = Entry(window)
input_X.place(x=130,y=55,width=100)

# 'Enter Y' label
Enter_Y = tk.Label(window,text="Enter Y: ",anchor="w", font=font_yh1)
Enter_Y.place(x=50,y=75,width=100)
input_Y = Entry(window)
input_Y.place(x=130,y=80,width=100)

# 'Tolerance' label
Tolerance = tk.Label(window,text="Tolerance: ",anchor="w", font=font_yh1)
Tolerance.place(x=250,y=50,width=100)
input_Tol = Entry(window)
input_Tol.place(x=350,y=55,width=100)
input_Tol.insert(0,'0.00001')

# 'Max Iter' label
Max_iter = tk.Label(window,text="Max Iter: ",anchor="w", font=font_yh1)
Max_iter.place(x=250,y=75,width=100)
input_Max_iter = Entry(window)
input_Max_iter.place(x=350,y=80,width=100)
input_Max_iter.insert(0,'1000')

# 'Add' button
Add = Button(window,text="Add",command=add)
Add.place(x=50,y=125,width=87)

# 'Remove' button 
Remove = Button(window,text="Remove",command=remove)
Remove.place(x=150,y=125,width=87)

# 'Start' button ######################################################
Start = Button(window,text="Start",command=add)
Start.place(x=250,y=125,width=87)

# 'Stop' button ######################################################
Stop = Button(window,text="Stop",command=add)
Stop.place(x=350,y=125,width=87)

# 'Load Data' button ######################################################
Load_data = Button(window,text="Load Data :", font=font_yh2, command=add)
Load_data.place(x=200,y=195,width=87)
input_data_file = Entry(window)
input_data_file.place(x=300,y=200,width=150)

# 'Save Data' button ######################################################
Save_data = Button(window,text="Save Data :", font=font_yh2, command=add)
Save_data.place(x=200,y=275,width=87)
output_data_file = Entry(window)
output_data_file.place(x=300,y=280,width=150)

# show all X
list_X = Listbox(window)
list_X.place(x=50,y=175,width=67)

# show all Y
list_Y = Listbox(window)
list_Y.place(x=120,y=175,width=67)

























window.mainloop()
