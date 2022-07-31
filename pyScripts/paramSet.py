import tkinter as tk
from contextlib import suppress


class ParamReturn:
    def __init__(self,x,s,c1,c2,equ,size,title,indLab,depLab,colorLab, print):
        self.x = x
        self.s = s
        self.c1 = c1
        self.c2 = c2
        self.equ = equ
        self.size = size
        self.title = title
        self.indLab = indLab
        self.depLab = depLab
        self.colorLab = colorLab
        self.print = print

def getElement(event, box):  
  with suppress(Exception): # Needless exceptions thrown by tkinter mod
    selection = event.widget.curselection()
    index = selection[0]
    value = event.widget.get(index)

    if box == 1 :
      global indCol
      indCol = index
      var1.set("Scatter Plot\nX Value = " + str(value))
    elif box == 2:
      global scatDep
      scatDep = index
      var2.set("Scatter Plot\nY Value = " + str(value))
    elif box == 3:
      global conInd1
      conInd1 = index
      var3.set("Contour Plot\nParmeter a = " + str(value))
    elif box == 4:
      global conInd2
      conInd2 = index
      var4.set("Contour Plot\nParmeter b = " + str(value))


def submit(win):
  win.destroy()
    

def startPSet (data) : 
  selection = []
  for i in range(len(data.columns)):
      selection.append(data.iat[0,i])
      # print (str(data.iat[0,i]))


  window = tk.Tk()

  window.title('Set Graph Parameters')
  
  window.geometry('1350x500')
  
  global var1
  var1 = tk.StringVar()
  global var2
  var2 = tk.StringVar()
  global var3
  var3 = tk.StringVar()
  global var4
  var4 = tk.StringVar()

  xspacing = 10
  yspacing = 5
  endCol = 5

  space = tk.Label(window, textvariable="").grid(row = 0, column= 4)
  l1 = tk.Label(window, fg='black', textvariable=var1).grid(row = 5, column= endCol, padx=xspacing, pady=yspacing)
  l2 = tk.Label(window, fg='black', textvariable=var2).grid(row = 6, column= endCol, padx=xspacing, pady=yspacing)      
  l3 = tk.Label(window, fg='black', textvariable=var3).grid(row = 3, column= endCol, padx=xspacing, pady=yspacing)
  l4 = tk.Label(window, fg='black', textvariable=var4).grid(row = 4, column= endCol, padx=xspacing, pady=yspacing)

  entItems = tk.StringVar()
  entItems.set(selection)

  listBoxCol = 1
  #Lambda is quirky. It serves as a command within a command.  
  #Here: we give it the var: event, then set event equal to getElement.
  #This is done because args cannot be passed via listboxselect. 
  lbEnt1 = tk.Listbox(window, listvariable=entItems)
  lbEnt1.grid(row = 1, column= listBoxCol, ipadx=xspacing)
  lbEnt1.bind('<<ListboxSelect>>', lambda event: getElement(event, 1))

  lbEnt2 = tk.Listbox(window, listvariable=entItems)
  lbEnt2.grid(row = 1, column= listBoxCol+1, padx=xspacing)
  lbEnt2.bind('<<ListboxSelect>>', lambda event: getElement(event, 2))

  lbEnt3 = tk.Listbox(window, listvariable=entItems)
  lbEnt3.grid(row = 1, column= listBoxCol+2, padx=xspacing)
  lbEnt3.bind('<<ListboxSelect>>', lambda event: getElement(event, 3))

  lbEnt4 = tk.Listbox(window, listvariable=entItems)
  lbEnt4.grid(row = 1, column= listBoxCol+3)
  lbEnt4.bind('<<ListboxSelect>>', lambda event: getElement(event, 4))


  lbl1 = tk.Label(window, text= "Scatter Plot\nX axis data values", font=("8")).grid(row = 0, column= listBoxCol, padx=xspacing, pady=yspacing)
  lbl2 = tk.Label(window, text= "Scatter Plot\nY axis data values", font=("8")).grid(row = 0, column= listBoxCol+1, padx=xspacing, pady=yspacing)
  lbl3 = tk.Label(window, text= "Contour Plot\nParmeter a", font=("8")).grid(row = 0, column= listBoxCol+2, padx=xspacing, pady=yspacing)
  lbl4 = tk.Label(window, text= "Contour Plot\nParmeter b", font=("2")).grid(row = 0, column= listBoxCol+3, padx=xspacing, pady=yspacing)


  contELbl = tk.Label(window, text= "Contour Function Equation", font=("2")).grid(row = 0, column= endCol, padx=xspacing, pady=yspacing)
  contELbl2 = tk.Label(window, text= "Enter an equation for the contour plot.\nExample : a/b", font=("6")).grid(row = 1, column= endCol, padx=xspacing)

  eqVar=tk.StringVar()
  inputeqVar = tk.Entry(window,textvariable=eqVar).grid(row = 2, column=endCol, padx=xspacing, pady=yspacing)

  sizeVar=tk.StringVar()
  lbSize = tk.Label(window, text= "Enter length for sides of graph").grid(row = 2, column= 0, padx=xspacing, pady=yspacing)
  inputSize = tk.Entry(window,textvariable=sizeVar).grid(row = 3, column=0, padx=xspacing, pady=yspacing)

  titleVar=tk.StringVar()
  lbTitle = tk.Label(window, text= "Enter Graph Title").grid(row = 0, column= 0, padx=xspacing, pady=yspacing)
  inputTitle = tk.Entry(window,textvariable=titleVar).grid(row = 1, column=0, padx=xspacing, pady=yspacing)

  indVarGraphLabel=tk.StringVar()
  lbIndVarGl = tk.Label(window, text= "Enter Corresponding Label").grid(row = 2, column= listBoxCol, padx=xspacing, pady=yspacing)
  inputIndVarGl = tk.Entry(window,textvariable=indVarGraphLabel).grid(row = 3, column=listBoxCol, padx=xspacing, pady=yspacing)

  depVarGraphLabel=tk.StringVar()
  lbDepVarGl = tk.Label(window, text= "Enter Corresponding Label").grid(row = 2, column= listBoxCol+1, padx=xspacing, pady=yspacing)
  inputDepVarGl = tk.Entry(window,textvariable=depVarGraphLabel).grid(row = 3, column=listBoxCol+1, padx=xspacing, pady=yspacing)

  cVarGraphLabel=tk.StringVar()
  lbCVarGl = tk.Label(window, text= "Enter Label for Contour Color Bar").grid(row = 2, column= listBoxCol+2, padx=xspacing, pady=yspacing)
  inputCVarGl = tk.Entry(window,textvariable=cVarGraphLabel).grid(row = 3, column=listBoxCol+2, padx=xspacing, pady=yspacing)

  printVar = tk.IntVar()
  printBox = tk.Checkbutton(window, text='Print equations to terminal\n(Will slow down the program)',variable=printVar, onvalue=1, offvalue=0).grid(row = 2, column= listBoxCol+3, padx=xspacing, pady=yspacing)

  
  b1 = tk.Button(window, text='submit parameters', command= lambda: submit(window)).grid(column=endCol, row=7)

  window.mainloop()
  
  equ = eqVar.get()
  if not 'conInd1' in globals():
    global conInd1
    conInd1 = 'X'

  if not 'conInd2' in globals():
    global conInd2
    conInd2 = 'X'
  
  if not 'indCol' in globals():
    raise ("There must to be a value associated with the X axis")


    
  rval = ParamReturn(indCol,scatDep,conInd1,conInd2,eqVar.get(),sizeVar.get(),titleVar.get(),indVarGraphLabel.get(),depVarGraphLabel.get(),cVarGraphLabel.get(), printVar.get())
  return rval

