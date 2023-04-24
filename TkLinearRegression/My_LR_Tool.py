# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 17:11:02 2023

@author: Sam Zhang
"""

# import functions
import os
import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.tix import *
import tkinter.font as tkFont

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
    """
    function to pliot the scatter plot of current data
    """
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
    fig = plt.figure(figsize = (9, 9), dpi=50)
    ax = fig.add_subplot()
    ax.scatter(X_num,Y_num,c="#7E95F2", marker = '.')
    ax.set_title("Linear Regression")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.xlim(min(X_num)-1, max(X_num)+1)
    plt.ylim(min(Y_num)-1, max(Y_num)+1)

    canvas1 = FigureCanvasTkAgg(fig,master=window)
    canvas1.draw()
    canvas1.get_tk_widget().pack(padx=10, pady=20)

    
    
    
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
    fig = plt.figure(figsize = (9, 9),dpi=50)
    ax=fig.add_subplot()
    fig2 = plt.figure(figsize=(9, 9),dpi=50)
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
    for i in range(epochs): 
        Y_pred = m * X_num + c  # The current predicted value of Y
        D_m = (-2/n) * sum(X_num * (Y_num - Y_pred))  # Derivative wrt m
        D_c = (-2/n) * sum(Y_num - Y_pred)  # Derivative wrt c
        m = m - LR * D_m  # Update m
        c = c - LR * D_c  # Update c
        m_list.append(m)
        c_list.append(c)
        ax.scatter(X_num,Y_num, c = '#7E95F2', marker = '.')
        im, = ax.plot(x,lr(m,c),'r')
        function_exp = "y = "+str(m)+" * x + "+str(c)
        title= ax.text(0.5,1.05,"iteration = " + str(i) + "\n "+function_exp, 
                        size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes, )
        ims.append([im,title])
        
        if i%10 == 0:
            print('Processing iteration', i)
    print('Saving to gif')
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=False)
    ani.save("test.gif",writer='pillow')
    print('Done')
    lbl = ImageLabel(window)
    lbl.pack()
    lbl.place(x=475,y=20,width=500)
    lbl.load('test.gif')
        
        
        
def load_data():
    input_file_name = input_data_file.get()
    if input_file_name[-3:] != 'csv':
        input_file_name += '.csv'
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
        
    else:
      messagebox.showerror("Error","No data found to load")


def save_data():
    output_file_name = output_data_file.get()
    if output_file_name[-3:] != 'csv':
        output_file_name += '.csv'
    pd.DataFrame(data).to_csv(output_file_name, index=False)

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

# 'Learning Rate' label
Learning_Rate = tk.Label(window,text="Learning Rate: ",anchor="w", font=font_yh1)
Learning_Rate.place(x=250,y=50,width=100)
input_LR = Entry(window)
input_LR.place(x=350,y=55,width=100)
input_LR.insert(0,'0.01')

# 'Max Iter' label
Max_iter = tk.Label(window,text="Max Iter: ",anchor="w", font=font_yh1)
Max_iter.place(x=250,y=75,width=100)
input_Max_iter = Entry(window)
input_Max_iter.place(x=350,y=80,width=100)
input_Max_iter.insert(0,'50')

# 'Add' button
Add = Button(window,text="Add",command=add)
Add.place(x=50,y=125,width=87)

# 'Remove' button 
Remove = Button(window,text="Remove",command=remove)
Remove.place(x=150,y=125,width=87)

# 'Start' button 
Start = Button(window,text="Start",command=regression_plot)
Start.place(x=250,y=125,width=87)

# 'Stop' button ######################################################
Stop = Button(window,text="Stop",command=add)
Stop.place(x=350,y=125,width=87)

# 'Load Data' button 
Load_data = Button(window,text="Load Data :", font=font_yh2, command=load_data)
Load_data.place(x=200,y=195,width=87)
input_data_file = Entry(window)
input_data_file.place(x=300,y=200,width=150)

# 'Save Data' button 
Save_data = Button(window,text="Save Data :", font=font_yh2, command=save_data)
Save_data.place(x=200,y=275,width=87)
output_data_file = Entry(window)
output_data_file.place(x=300,y=280,width=150)

# show all X
list_X = Listbox(window)
list_X.place(x=50,y=175,width=67)

# show all Y
list_Y = Listbox(window)
list_Y.place(x=120,y=175,width=67)








tkinter.mainloop()





















window.mainloop()
