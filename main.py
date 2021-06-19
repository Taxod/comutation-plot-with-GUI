#!/usr/bin/env python
# coding: utf-8

# import package 
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from comut import comut
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re


def define_layout(obj, cols=1, rows=1):
    
    def method(trg, col, row):
        
        for c in range(cols):    
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj)==list:        
        [method(trg, cols, rows) for trg in obj]
    else:
        trg = obj
        method(trg, cols, rows)


def drawResult():
    path = [lable2.get(),lable6.get()]
    sampleName = [lable4.get(), lable8.get()]
    print(sampleName)
    for i in range(len(sampleName)):
        if sampleName[i] == '':
            sampleName[i] = "undefied_" + str(i) 
            
    df1 = formmatData(path[0],sampleName[0])
    df2 = formmatData(path[1],sampleName[1])
    
    df = pd.concat([df1,df2])
    
    df.drop_duplicates(inplace=True)
    df.sort_values(by='category', ascending=False, inplace=True)
    toy_comut = comut.CoMut()
    toy_comut.add_categorical_data(df, name = 'Mutation type')  
    
    import matplotlib.gridspec as gridspec
    
    fig = plt.figure(figsize=(6, 10), tight_layout=False)

    chart_type = FigureCanvasTkAgg(fig, div0)
    toy_comut.plot_comut(x_padding = 0.05, y_padding = 0.04, tri_padding = 0.03, hspace = 0.05, wspace = 0.05,
                         fig = fig)
    chart_type.get_tk_widget().pack()
    
    
    fig2 = plt.figure(figsize=(6, 10), tight_layout=False)
    chart = FigureCanvasTkAgg(fig2, div1)
    
    mut_mapping = {'Substitution': 'green', 'Indel':'#FFD700', 'Absent': {'facecolor': 'grey', 'alpha': 0.2}}
    toy_comut = comut.CoMut()
    toy_comut.add_categorical_data(df, name = 'Mutation type', mapping = mut_mapping, tick_style = 'italic')
    toy_comut.plot_comut(x_padding = 0.05, y_padding = 0.04, tri_padding = 0.03, hspace = 0.05, wspace = 0.05,
                         fig = fig2)
    chart.get_tk_widget().pack()
    

def formmatData(path, sampleName='Unknown'):
    df2 = pd.read_excel(path)
    df1 = df2[df2['Annotated Locus Type']=='Coding region']
    nameList = [sampleName for i in range(df1.shape[0])]
    
    value = []
    for i,j in zip(list(df1['REF']),list(df1['ALT'])):
        if len(i) == len(j):
            value.append('Substitution')
        else:
            value.append('Indel')
    pattern = '(\d+-\d+)'
    prog = re.compile(pattern)
    df = pd.DataFrame({'sample':nameList, 'category':df1['Annotated Locus Name'].str.replace(prog, '#').str.strip('(#)'), 'value':value})
    return df


def upload_file():
    file_path = askopenfilename(filetypes=(("excel", "*.xlsx"),
                                           ("HTML files", "*.html;*.htm"),
                                           ("All files", "*.*") ))

    if not file_path:
        lable2.insert(tk.END,'file path is empty') 
    else:
        if lable2.get() == '':
            lable2.insert(tk.END, file_path)
        else:
            lable6.insert(tk.END, file_path)
                

window = tk.Tk()
window.title('Window')
align_mode = 'nswe'
pad = 5

div_size = 200
img_size = div_size * 2
div0 = tk.Frame(window,  width=0 , height=div_size)
div1 = tk.Frame(window,  width=0, height=div_size)
div2 = tk.Frame(window,  width=div_size , height=div_size)
div3 = tk.Frame(window,  width=div_size , height=div_size)

window.update()
win_size = min( window.winfo_width(), window.winfo_height())

div0.grid(column=0, row=0, padx=pad, pady=pad, sticky=align_mode)
div1.grid(column=0, row=1, padx=pad, pady=pad, sticky=align_mode)
div2.grid(column=1, row=0, padx=pad, pady=pad, sticky=align_mode)
div3.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)



lable1 = ttk.Label(div2, text='File path 1：', font=('Monaco', 16, 'bold'))
lable2 = ttk.Entry(div2, font=('Monaco', 8, 'bold'))
lable3 = ttk.Label(div2, text="Sample name 1：", font=('Monaco', 16, 'bold'))
lable4 = ttk.Entry(div2, font=('Monaco', 16, 'bold'))

lable1.grid(column=0, row=0, sticky=align_mode)
lable2.grid(column=0, row=1, sticky=align_mode)
lable3.grid(column=0, row=2, sticky=align_mode)
lable4.grid(column=0, row=3, sticky=align_mode)


lable5 = ttk.Label(div2, text='File path 2：', font=('Monaco', 16, 'bold'))
lable6 = ttk.Entry(div3, font=('Monaco', 8, 'bold'))
lable7 = ttk.Label(div3, text="Sample name 2：", font=('Monaco', 16, 'bold'))
lable8 = ttk.Entry(div3, font=('Monaco', 16, 'bold'))

lable5.grid(column=0, row=4, sticky=align_mode)
lable6.grid(column=0, row=0, sticky=align_mode)
lable7.grid(column=0, row=1, sticky=align_mode)
lable8.grid(column=0, row=2, sticky=align_mode)


        
bt1 = ttk.Button(div3, text='Upload file', command=upload_file)
bt2 = ttk.Button(div3, text='Draw', command=drawResult)
bt1.grid(column=0, row=3, sticky=align_mode)
bt2.grid(column=0, row=4, sticky=align_mode)



define_layout(window, cols=2, rows=2)
define_layout(div0)
define_layout(div1)
define_layout(div2, rows=5)
define_layout(div3, rows=5)

window.mainloop()

