# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 10:07:50 2023

@author: mathi
"""

import tkinter as tk


class appTkinter(tk.Tk) :
    def __init__(self) :
        tk.Tk.__init__(self)
        self.creer_widgets()

    def creer_widgets(self) :
        self.label = tk.Label(self, text="hello")
        self.bouton = tk.Button(self, text="Quitter", command=self.quit)
        self.label_client = tk.Label(self, text='nom :')
        self.label_client.config()
        self.label.pack()
        self.label_client.pack()
        self.bouton.pack()

app = appTkinter()
app.title("Ma Premiere App")
app.mainloop()