'''
Created on Jun 1, 2016

@author: omer
'''
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from Tkinter import Frame
from app import process
import tkMessageBox
import ConfigParser
import datetime
import os

class Section(object):
    def __init__(self,master,mLabel = "", isFileOpen = True,mInitialText = ""):
        
        self.master = master
        self.frame = Frame(self.master)
        self.isFileOpen = isFileOpen
        self.label = Label(self.frame, text=mLabel)
        self.textbox = Entry(self.frame,width=60)
        self.textbox.insert(0, mInitialText)
        self.openFileButton = Button(self.frame,text = "Open", command = self.openFile)
    def openFile (self):
        fileName = askopenfilename() if self.isFileOpen else askdirectory()
        self.textbox.delete(0,END)
        self.textbox.insert(0,fileName)
    def pack(self,rowIdx = 1):
        '''self.label.grid(row = 0,column = 0)
        self.label.pack(pady=0, padx = 1)
        self.textbox.pack(pady=0, padx = 2)
        self.openFileButton.pack(pady=0, padx = 3)'''
        self.frame.pack()
        self.packWidget(self.label, rowIdx, 1)
        self.packWidget(self.textbox, rowIdx, 2)
        self.packWidget(self.openFileButton, rowIdx, 3)
    def packWidget(self,widget,rowIdx,colIdx):
        #widget.grid(row=rowIdx,column = colIdx)
        widget.pack(pady=1, padx = 0,side=LEFT)
    def get(self):
        return self.textbox.get()
class GUI(object):
    def __init__(self,config):
        self.config = config
        self.root = Tk()
        self.root.minsize(width=500, height=500)
        self.widgets = {}

        self.helpButton = Button(self.root, text = 'Help', command = self.help)

        self.widgets["1startPage"]=Section(self.root,"Start Page (Setlist.fm)")
        self.widgets["2year"] = Section(self.root,"year (YYYY)")
        self.widgets["3month"] = Section(self.root,"month (mm)")
        self.widgets["4day"] = Section(self.root,"day (dd)")

        self.widgets["5outputFolder"] = Section(self.root,"OutputFolder/dist",False,os.getcwd())
        
        self.processButton = Button(self.root, text = 'Process', command = self.Pressed)
        '''self.processBtn = Button(self.root, text = 'Process', command = self.Pressed)
        
        self.dataFile = Section(self.root,"Data File")'''
        self.pack()
        self.root.mainloop()
    def pack(self):

        idx = 0
        self.helpButton.pack(pady=5, padx = 0,side=LEFT)
        for widgetKey in sorted(self.widgets.keys()):
            self.widgets[widgetKey].pack(idx)
            idx +=1
        self.processButton.pack(pady=5, padx = 0)
    def Pressed(self):                          #function
            #print 'buttons are cool'
            #print ["init",self.widgets["outputFolder"].get(),self.widgets["rpath"].get(),"--vanilla",self.widgets["rscript"].get(),self.widgets["dataFile"].get(),self.widgets["meta"].get()]
            day = self.widgets["4day"].get()
            if len(day) == 1:
                day = "0"+day
            month = self.widgets["3month"].get()
            if len(month) == 1:
                month = "0"+month
            year = self.widgets["2year"].get()
            print day,month,year

            thDate = datetime.datetime.strptime("{0}/{1}/{2}".format(day,month,year), "%d/%m/%Y").date()
            print thDate
            process(self.widgets["1startPage"].get(),thDate,self.widgets["5outputFolder"].get())
    def help(self):     
        text = '''
        Data File - dataset
        Metadata File- | delimited file: cols: colName(not mentioned), isScript(boo), Script(Str), new(bool), newScript(str), remove(bool), isPivot(bool), isVariable(bool)
        R Path - R.exe
        R Script - R script to run
        OutputFolder/dist - folder to save the dist files'''
        tkMessageBox.showinfo("Help",text)
config = {}       
Config = ConfigParser.ConfigParser()
Config.read("config.conf")
for section in Config.sections():
    config[section] = {}
    for option in Config.options(section):
        config[section][option] = Config.get(section, option)

        
gui = GUI(config)

'''root = Tk()                             #main window
button = Button(root, text = 'Press', command = Pressed)
button.pack(pady=20, padx = 20)
Pressed()
root.mainloop()'''