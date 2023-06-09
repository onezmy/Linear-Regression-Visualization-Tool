# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 17:11:02 2023

@author: Sam Zhang
"""

# import functions
import os
import numpy as np
import pandas as pd
import time


import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.tix import *
import tkinter.font as tkFont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
import matplotlib.animation as animation

from PIL import Image, ImageTk
from itertools import count, cycle


"""
init data
"""
X = []
Y = []
data = []
df = {}
input_Max_iter = 50

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
    global data
    x = input_X.get()
    y = input_Y.get()
    X.append(x)
    Y.append(y)
    data.insert(0,tuple([x,y]))
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
    """
    function to pliot the scatter plot of current data
    """
    clear_points_plot()
    
    X = list(list_X.get(0,list_X.size()-1))
    Y = list(list_Y.get(0,list_Y.size()-1))
    if len(X) == 0:
        return
    df['X'] = X
    df['Y'] = Y 
    X_num, Y_num = [], []
    n = len(X)
    for i in range(n):
        try:
            X_num.append(float(X[i]))
            Y_num.append(float(Y[i]))
        except:
            continue
    fig = plt.figure(figsize = (9, 10), dpi=50)
    ax = fig.add_subplot()
    ax.scatter(X_num,Y_num,c="#7E95F2", marker = '.')
    ax.set_title("Linear Regression")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.xlim(min(X_num)-1, max(X_num)+1)
    plt.ylim(min(Y_num)-1, max(Y_num)+1)

    canvas1 = FigureCanvasTkAgg(fig,master=window)
    canvas1.draw()
    canvas1.get_tk_widget().pack(padx=800, pady=10)

    
    
    
class ImageLabel(tk.Label):
    """
    class to add acces the regression gif
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()
    def unload(self):
        self.config(image=None)
        self.frames = None
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
 

def regression_plot():
    """
    function for start button, plot the regression gif
    """
    clear_points_plot()

    fig = plt.figure(figsize = (13, 13),dpi=50)
    ax=fig.add_subplot()
    fig2 = plt.figure(figsize=(13, 13),dpi=50)
    ax2 = fig2.add_subplot()
    X_num, Y_num = [], []
    n = len(X)
    for i in range(n):
        try:
            X_num.append(float(X[i]))
            Y_num.append(float(Y[i]))
        except:
            continue
        
    x = np.linspace(min(X_num)-1, max(X_num)+1, 120)
    
    def lr(m, c):
        return m * x + c
    
    # Performing Gradient Descent 
    m, c = 0, 0
    m_list, c_list = [0], [0]
    LR = float(input_LR.get()) 
    epochs = int(input_Max_iter.get())  
    ims = []
    ims_loss = []
    X_num = np.array(X_num)
    Y_num = np.array(Y_num)
    iteration_lsit = []
    loss_list = []
    for i in range(epochs): 
        Y_pred = m * X_num + c  # The current predicted value of Y
        D_m = (-2/n) * sum(X_num * (Y_num - Y_pred))  # Derivative wrt m
        D_c = (-2/n) * sum(Y_num - Y_pred)  # Derivative wrt c
        m = m - LR * D_m  # Update m
        c = c - LR * D_c  # Update c
        m_list.append(m)
        c_list.append(c)
        plt.rcParams["axes.titlesize"]='xx-large'
        ax.scatter(X_num,Y_num, c = '#7E95F2', marker = '.')
        im, = ax.plot(x,lr(m,c),'r')
        function_exp = "y = "+str(m)+" * x + "+str(c)
        title= ax.text(0.5,1.05,"iteration = " + str(i) + "\n "+function_exp, 
                        size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes,)
        ims.append([im,title])
        iteration_lsit.append(i)
        cur_loss = 1/n * sum(Y_num - Y_pred)
        loss_list.append(cur_loss)
        ax2.axis(xmin=0,xmax=epochs,ymin=0,ymax=1.2*loss_list[0])
        im2, = ax2.plot(iteration_lsit,loss_list,c='r')
        title2 = ax2.text(0.5,1.05,"loss over iteration \n current loss ="+str(cur_loss), 
                        size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes, )
        ims_loss.append([im2,title2])
        if i%10 == 0:
            print('Processing iteration', i)
            
    print('Saving to gif')
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=False)
    ani.save("test.gif",writer='pillow')
    
    ani2 = animation.ArtistAnimation(fig2, ims_loss, interval=50, blit=False)
    ani2.save("test_loss.gif",writer='pillow')
    print('Done')
    
    global lbl, lbl2

    lbl.load('test.gif')
    lbl2.load('test_loss.gif')
    
        
        
def load_data():
    input_file_name = input_data_file.get()
    if os.path.exists(input_file_name):
        data = pd.read_csv(input_file_name)
        values = data.values
        list_X.delete(0,END)
        list_Y.delete(0,END)
        X.clear()
        Y.clear()
        for row in values:
             list_X.insert(END,row[0])
             X.append(str(row[0]))
             list_Y.insert(END,row[1])
             Y.append(str(row[1]))
        show_all()
        points_plot()
    else:
      messagebox.showerror("Error","No data found to load")


def save_data():
    output_file_name = output_data_file.get()
    if output_file_name[-3:] != 'csv':
        output_file_name += '.csv'
    pd.DataFrame(data).to_csv(output_file_name, index=False)

def clear_data():
    X = []
    Y = []
    data = []
    df = {}
    clear_points_plot()
    list_X.delete(0,END)
    list_Y.delete(0,END)

"""
init window
"""

window = ttk.Window()
window.title("Linear Regression")
window.geometry("2000x800")



"""
define fonts
"""
font1 = tkFont.Font(size=10)
font2 = tkFont.Font(size=12, weight='bold')




"""
add buttons/labels
"""

# 'Enter X' label
Enter_X = ttk.Label(window,text="Enter X :",anchor="w", background = '#fff', font = font1)
Enter_X.place(x=50,y=50,width=120)
input_X = ttk.Entry(window, cursor=	'left_ptr')
input_X.place(x=180,y=50,width=150)

# 'Enter Y' label
Enter_Y = ttk.Label(window,text="Enter Y :",anchor="w", background = '#fff', font = font1)
Enter_Y.place(x=50,y=100,width=120)
input_Y = ttk.Entry(window, cursor=	'left_ptr')
input_Y.place(x=180,y=100,width=150)

# 'Learning Rate' label
Learning_Rate = ttk.Label(window,text="Learning Rate:",anchor="w", background = '#fff', font = font1)
Learning_Rate.place(x=50,y=210,width=180)
input_LR = ttk.Entry(window)
input_LR.place(x=240,y=210,width=90)
input_LR.insert(0,'0.01')

# 'Max Iter' label
Max_iter = ttk.Label(window,text="Max Iteration:",anchor="w", background = '#fff', font = font1)
Max_iter.place(x=50,y=260,width=180)
input_Max_iter = ttk.Entry(window)
input_Max_iter.place(x=230,y=260,width=100)
input_Max_iter.insert(0,'50')

# 'Add' button
Add = ttk.Button(window,text="Add",command=add,bootstyle = ttk.constants.PRIMARY)
Add.place(x=50,y=155,width=130)

# 'Remove' button 
Remove = ttk.Button(window,text="Remove",command=remove,bootstyle = ttk.constants.WARNING)
Remove.place(x=200,y=155,width=130)

# 'Load Data' button 
Load_data = ttk.Button(window,text="Load Data :",command=load_data, bootstyle = (ttk.constants.PRIMARY, ttk.constants.OUTLINE))
Load_data.place(x=50,y=310,width=150)
input_data_file = ttk.Entry(window)
input_data_file.place(x=210,y=310,width=120)

# 'Save Data' button 
Save_data = ttk.Button(window,text="Save Data :", command=save_data, bootstyle = (ttk.constants.INFO, ttk.constants.OUTLINE))
Save_data.place(x=50,y=360,width=150)
output_data_file = ttk.Entry(window)
output_data_file.place(x=210,y=360,width=120)

# 'Start' button 
Start = ttk.Button(window,text="Start",command=regression_plot, bootstyle=ttk.constants.SUCCESS)
Start.place(x=50,y=420,width=130)

# 'Restart' button 
Start = ttk.Button(window,text="Clear",command= clear_data, bootstyle=ttk.constants.DANGER)
Start.place(x=200,y=420,width=130)

# values label
Max_iter = ttk.Label(window,text="X-Values  |   Y-Values",anchor="w", background = '#fff', font = font2)
Max_iter.place(x=415,y=50,width=330)

# show all X
list_X = tk.Listbox(window)
list_X.place(x=400,y=100,width=170)

# show all Y
list_Y = tk.Listbox(window)
list_Y.place(x=580,y=100,width=170)

lbl = ImageLabel(window)
lbl.pack()
lbl.place(x=800,y=10,width=550)

lbl2 = ImageLabel(window)
lbl2.pack()
lbl2.place(x=1350,y=10,width=550)



window.mainloop()
