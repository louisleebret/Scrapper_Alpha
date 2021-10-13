# Importation of the required libraries
from pandastable import Table
import tkinter as tk
from tkinter.ttk import *

#Importation of the file Scrapper_alpha.py
import Scrapper_Alpha as s_a
  

def open_results():
    """
    This function is called when the user presses the button Show
    This function first check if the user information are correct
    Then the function enters the user requirement inside a scrapper Alpha object
    the method filter_df is called in order to get the user's desired properties
    Then the outputted data frame is transomed into a pandatable object 
    The pandatable ibject is then used to display the data frame inside a new window
    """
    

    # Checking if the user input is in correct form
    if len(e1.get()) == 0:
        newWindow = tk.Toplevel(master) 
        error_message = f'We could not find houses for your search because you did not provide enough information'
        title = 'ERROR'
        newWindow.title(title) 
        tk.Label(newWindow, text=error_message).grid(row=20,column=50,pady=10)

    else:
        post_code = e1.get()
        if len(e2.get()) == 0:
            price_min = 0
        else:
            price_min = int(e2.get())

        if len(e3.get()) == 0:
            price_max = 100000
        else:
            price_max = int(e3.get())

        if price_min>price_max:
            a = price_min
            b = price_max
            price_min = b
            price_max = a

        if len(e4.get()) == 0:
            bedroom = 0
        elif int(e4.get()) == 1:
            bedroom = 0
        else:
            bedroom = int(e4.get())

        if len(e5.get()) == 0:
            bathroom = 0
        elif int(e5.get()) == 1:
            bathroom = 0
        else:
            bathroom = int(e5.get())

        newWindow = tk.Toplevel(master) 
        title = f'House to rend in {e1.get()}'
        newWindow.title(title) 
        newWindow.geometry("1300x1000") 
        frame = tk.Frame(newWindow)
        frame.pack(fill='both', expand=True)

        # Searching for the user's desired properties
        b = s_a.Scrapper_Alpha(post_code,price_min,price_max,bedroom,bathroom)
        df = b.filter_df()
        # Outputing the result inside a new window
        Table(frame, dataframe=df).show()



"""
This piece of code generates the form where user can entered his search requirements
"""
master = tk.Tk()
#master.geometry("500x500") 
master.title("Scrapper Alpha")
tk.Label(master, text="Post Code:").grid(row=20,column=50,pady=10)
tk.Label(master, text="Min Price:").grid(row=21,column=49,pady=10)
tk.Label(master, text="Max Price:").grid(row=21,column=51,pady=10)
tk.Label(master, text="Min bedroom:").grid(row=22,column=49,pady=10)
tk.Label(master, text="Min bathroom:").grid(row=22,column=51,pady=10)

e1 = tk.Entry(master)
e2 = tk.Entry(master)
e3 = tk.Entry(master)
e4 = tk.Entry(master)
e5 = tk.Entry(master)

e1.grid(row=20, column=51,pady=10)
e2.grid(row=21, column=50,pady=10)
e3.grid(row=21,column=52,pady=10)
e4.grid(row=22, column=50,pady=10)
e5.grid(row=22,column=52,pady=10)

tk.Button(master, text='Quit', command=master.quit).grid(row=31,column=40, sticky=tk.W,pady=25,padx = 10)
tk.Button(master,text='Show', command=open_results).grid(row=31,column=60,sticky=tk.W,pady=25,padx = 10)

master.mainloop()




