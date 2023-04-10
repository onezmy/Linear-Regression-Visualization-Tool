# Linear Regression Example
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


def updatelists():
      lstdistance.delete(0,END)
      lstfare.delete(0,END)
      for distance in distances:
           lstdistance.insert(END,distance)
      for fare in fares:
           lstfare.insert(END,fare)

def add():
      if txtdistance.get() in distances:
         i = distances.index(txtdistance.get())
         distances[i] = txtdistance.get()
         fares[i] = txtfare.get()
      else:
         distances.append(txtdistance.get())
         fares.append(txtfare.get())
      updatelists()
      plot()

def delete():
      #d = lstdistance.get(ANCHOR)
      try:
         d = lstdistance.get(lstdistance.curselection())
         if d in distances:
            i = distances.index(d)
            del distances[i]
            del fares[i]
            lstdistance.delete(i)
            lstfare.delete(i)
            lstpredfare.delete(i)
            plot()
      except:
            pass

def plot():
      distances = list(lstdistance.get(0,lstdistance.size()-1))
      if len(distances) == 0:
         return
      fares = list(lstfare.get(0,lstfare.size()-1))
      distances = [int(n) for n in distances]
      fares = [int(n) for n in fares]
      data["distances"] = distances
      data["fares"] = fares
      df = pd.DataFrame(data)
      X = df[["distances"]]
      y = df["fares"]
      model = LinearRegression()
      model.fit(X,y)
      y_pred = model.predict(X)
      lstpredfare.delete(0,END)
      for n in y_pred:
           lstpredfare.insert(END,n)
      txtintercept.delete(0,END)
      txtintercept.insert(0,str(round(model.intercept_,2)))
      txtslope.delete(0,END)
      txtslope.insert(0,str(round(model.coef_[0],2)))
      clearplot()
      fig = plt.figure()
      ax = fig.add_subplot(111)
      ax.plot(X,y,color="red",marker="o",markerfacecolor="blue",label="Actual Fare")
      ax.plot(X,y_pred,color="blue",marker="o",markerfacecolor="blue",label="Predicted Fare")
      ax.set_title("Linear Regression Example")
      ax.set_xlabel("Distance")
      ax.set_ylabel("Fare")
      ax.legend()
      canvas = FigureCanvasTkAgg(fig,master=window)
      canvas.draw()
      canvas.get_tk_widget().pack()

def clearplot():
      for widget in window.winfo_children():
           if "Canvas" in str(type(widget)):
              widget.destroy()

def listselected(event):
      if len(lstdistance.curselection()) == 0:
         return
      i = lstdistance.curselection()[0]
      txtdistance.delete(0,END)
      txtdistance.insert(END,distances[i])
      txtfare.delete(0,END)
      txtfare.insert(END,fares[i])

def savedata():
      pd.DataFrame(data).to_csv("data.csv",index=False)

def opendata():
      if os.path.exists("data.csv"):
          data = pd.read_csv("data.csv")
          values = data.values
          lstdistance.delete(0,END)
          lstfare.delete(0,END)
          distances.clear()
          fares.clear()
          for row in values:
               lstdistance.insert(END,row[0])
               distances.append(str(row[0]))
               lstfare.insert(END,row[1])
               fares.append(str(row[1]))
      else:
          messagebox.showerror("Error","No data found to load")

distances = []
fares = []
data = {}
window = Tk()
window.title("Linear Regression")
window.geometry("1800x500")
tip = Balloon(window)
lbldistance = Label(window,text="Enter X: ",anchor="w")
lbldistance.place(x=50,y=50,width=100)
txtdistance = Entry(window)
txtdistance.place(x=150,y=50,width=100)
lblfare = Label(window,text="Enter Y: ",anchor="w")
lblfare.place(x=50,y=75,width=100)
txtfare = Entry(window)
txtfare.place(x=150,y=75,width=100)
btnadd = Button(window,text="Add/Update",command=add)
btnadd.place(x=50,y=100,width=100)
btndelete = Button(window,text="Delete",command=delete)
btndelete.place(x=150,y=100,width=100)
btnplot = Button(window,text="Plot",command=plot)
btnplot.place(x=50,y=125,width=100)
btnclear = Button(window,text="Clear",command=clearplot)
btnclear.place(x=150,y=125,width=100)
btnsave = Button(window,text="Save Data",command=savedata)
btnsave.place(x=50,y=150,width=100)
btnopen = Button(window,text="Open Data",command=opendata)
btnopen.place(x=150,y=150,width=100)
lstdistance = Listbox(window)
lstdistance.place(x=50,y=175,width=67)
lstfare = Listbox(window)
lstfare.place(x=120,y=175,width=67)
lstpredfare = Listbox(window)
lstpredfare.place(x=190,y=175,width=67)
lblintercept = Label(window,text="Y-Intercept: ",anchor="w")
lblintercept.place(x=50,y=350,width=100)
txtintercept = Entry(window)
txtintercept.place(x=150,y=350,width=100)
lblslope = Label(window,text="Slope: ",anchor="w")
lblslope.place(x=50,y=375,width=100)
txtslope = Entry(window)
txtslope.place(x=150,y=375,width=100)
lstdistance.bind("<<ListboxSelect>>",listselected)
tip.bind_widget(lstdistance,balloonmsg="Distances")
tip.bind_widget(lstfare,balloonmsg="Actual Fares")
tip.bind_widget(lstpredfare,balloonmsg="Predicted Fares")
window.mainloop()