# Import the library
from tkinter import *
from tkinter import filedialog
import pandas as pd


def createDS(win):
   filepath = filedialog.askopenfilename(title="Open a Text File", filetypes=(("text    files","*.txt"), ("all files","*.*")))
   file = open(filepath,'r')
   win.destroy()

# I dislike the global, but apparently pass by ref is not a thing in python >:(
#Also function calls via button press do not return values, always void functions.
   global data 
   data = pd.read_csv(file, sep= '	', header=None)
   # data = pd.read_csv(file, sep= ',', header=None)
   file.close()


   col = []
   for x in range(len(data.columns)):
      col.append(str(x))

def startSel():
   window=Tk()
   window.title('Jake\'s Plotter')

   window.geometry("700x300")
   Label(window, text="Hello!\nClick the button and proceed to select a file", font='Arial 16 bold').pack(pady=15)
   button = Button(window, text="Open", command= lambda: createDS(window))
   button.pack()
   window.mainloop()
   print (data)
   return data

