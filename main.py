#
#   THIS IS VERY MUCH SO A WORK IN PROGRESS
#   DONT EXPECT THIS TO BE 100% FUNCTIONAL
#

from tkinter import *
from tkinter import ttk
import GenPass as gp
import random, string
import sqlite3 as sl
from cryptography.fernet import Fernet
#connect/create database
con = sl.connect('gen.db')
#create cursor for datavase
cur = con.cursor()
#define key
setKey = ""
#Try Creating Key Table
try:
    cur.execute("CREATE TABLE genKey(key)")
    print("Key Table Created")
except:
    print("Key Table Found :)")

#Try Creating Data Table
try:
    cur.execute("CREATE TABLE passwords(website, email, password)")
    print("Password Table Created :)")
except:
    print("Password Table Found")
#Get Encryption Key
keyRet = cur.execute("SELECT key FROM genKey")
key = keyRet.fetchone()
#Check if key doesn't exist
if (key is None):
    #Gen Key if doesn't exist
    setKey = Fernet.generate_key()
    #set key to list
    key = [setKey]
    #Send Key to database
    cur.execute("INSERT INTO genKey VALUES(?)", key)
    con.commit()
    print("Key Set")
#Key Generated or Already exists
print("Key Found")
#Get Key data
listlessKey = (key[0])

#initialize fernet
fernet = Fernet(listlessKey)
#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("450x550")
win.resizable(False, False)
win.configure(background='grey14')
win.attributes('-alpha',0.95)
win.wm_title("Password Bank GUI")

class scrollingFrame(Frame):
    def __init__(self, parentObject, background):
        Frame.__init__(self, parentObject, background = background)
        self.canvas = Canvas(self, borderwidth=0, background = background, highlightthickness=0)
        self.frame = Frame(self.canvas, background = background)

        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview, background=background)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky=N+S)

        self.hsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview, background=background)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky=E+W)

        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        self.window = self.canvas.create_window(0,0, window=self.frame, anchor="nw", tags="self.frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)


    def onFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        #Resize the inner frame to match the canvas
        minWidth = self.frame.winfo_reqwidth()
        minHeight = self.frame.winfo_reqheight()

        if self.winfo_width() >= minWidth:
            newWidth = self.winfo_width()
            #Hide the scrollbar when not needed
            self.hsb.grid_remove()
        else:
            newWidth = minWidth
            #Show the scrollbar when needed
            self.hsb.grid()

        if self.winfo_height() >= minHeight:
            newHeight = self.winfo_height()
            #Hide the scrollbar when not needed
            self.vsb.grid_remove()
        else:
            newHeight = minHeight
            #Show the scrollbar when needed
            self.vsb.grid()

        self.canvas.itemconfig(self.window, width=newWidth, height=newHeight)

class messageList(object):
    def __init__(self, scrollFrame, innerFrame):
        self.widget_list = []
        self.innerFrame = innerFrame
        self.scrollFrame = scrollFrame

        # Keep a dummy empty row if the list is empty
        self.placeholder = Label(self.innerFrame, text=" ")
        self.placeholder.grid(row=0, column=0)

    # add new entry and update layout
    def add_message(self, text):
        print('add message')
        self.placeholder.grid_remove()
        # create var to represent states
        int_var = IntVar()

        cb = Checkbutton(self.innerFrame, text=text, variable=int_var)
        cb.grid(row=self.innerFrame.grid_size()[1], column=0, padx=1, pady=1, sticky='we')
        self.widget_list.append(cb)

        self.innerFrame.update_idletasks()
        self.scrollFrame.onCanvasConfigure(None)

    # delete all messages
    def del_message(self):
        print('del message')
        for it in self.widget_list:
            it.destroy()

        self.placeholder.grid()
        self.innerFrame.update_idletasks()
        self.scrollFrame.onCanvasConfigure(None)

win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)

frame_canvas = ttk.Frame(win)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)
frame_canvas.config(height=250, width=400)
frame_canvas.place(x=225, y=380, anchor='center')

canvas = Canvas(frame_canvas, bg="grey20", borderwidth=0, highlightthickness=0)
canvas.grid(row=0, column=0, sticky="news")

vsb = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set, yscrollincrement=5, scrollregion=canvas.bbox("all"))
frame_buttons = Frame(canvas)
frame_buttons.config(background='grey18', borderwidth=0, highlightthickness=0)
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
#canvas.config(scrollregion=canvas.bbox("all"))
style = ttk.Style(frame_buttons)
style.configure('TLabel', background='grey18', foreground='Red')
style.configure('TFrame', background='grey18')

frame_buttons.update_idletasks()

def sendToDatabase():
    phase1WebsiteText = str(webSiteEntry.get())
    phase1EmailText = str(emailEntry.get())
    phase1PasswordText = str(passwordLabel.cget("text"))
    print(phase1WebsiteText)
    print(phase1EmailText)
    print(phase1PasswordText)
    byteWebsite = str.encode(phase1WebsiteText)
    #Encrypt Password
    encryptedWeb = fernet.encrypt(byteWebsite)

    byteEmail = str.encode(phase1EmailText)
    #Encrypt Password
    encryptedEmail = fernet.encrypt(byteEmail)

    bytePass = str.encode(phase1PasswordText)
    #Encrypt Password
    encryptedPass = fernet.encrypt(bytePass)
    print(str(bytePass))
    data = ([encryptedWeb, encryptedEmail, encryptedPass])
    cur.execute("INSERT INTO passwords VALUES(?, ?, ?)", data)
    con.commit()

def readData():
    currentRow = 0
    for row in cur.execute("SELECT website, email, password FROM passwords ORDER BY website"):
        strDecryptedWebsite = gp.decryptData(row[0])
        strDecryptedEmail = gp.decryptData(row[1])
        strDecryptedPassword = gp.decryptData(row[2])

        colum1 = ttk.Label(frame_buttons, text=(strDecryptedWebsite)).grid(column=1, row=currentRow)
        colum2 = ttk.Label(frame_buttons, text=(strDecryptedEmail)).grid(column=2, row=currentRow)
        colum3 = ttk.Label(frame_buttons, text=(strDecryptedPassword)).grid(column=3, row=currentRow)
        currentRow = currentRow+1

def generatePassword():
    length = int(passLength.get())
    passwordText=gp.genPassword(length)
    passwordLabel["text"] = (f'{passwordText}')

passwordLabel = Label(win, text="", font= ('Century 12'), width=28)
passwordLabel.grid()
passwordLabel.place(x=225, y=160, anchor='center')

webSiteLabel= ttk.Label(win,font=('Century 12'),width=7, text="Website", anchor='center', background='grey14', foreground='Red')
webSiteLabel.grid()
webSiteLabel.place(x=225,anchor='center', y=10)

webSiteEntry = ttk.Entry(win,font=('Century 12'),width=28, foreground='grey18', background='grey18',)
webSiteEntry.config({"background": "grey18"})
webSiteEntry.grid()
webSiteEntry.place(x=225, y=40, anchor='center')

emailLabel= ttk.Label(win,font=('Century 12'),width=7, text="Email", anchor='center', background='grey14', foreground='Red')
emailLabel.grid()
emailLabel.place(x=225,anchor='center', y=70)

emailEntry = ttk.Entry(win,font=('Century 12'),width=28, foreground='grey18', background='grey18')
emailEntry.config({"background": "grey18"})
emailEntry.grid()
emailEntry.place(x=225, y=100, anchor='center')

passwordLabelTitle = Label(win, text="Password", font= ('Century 12'), width=28, background='grey18', foreground='Red')
passwordLabelTitle.grid()
passwordLabelTitle.place(x=225, y=130, anchor='center')
passLength = ttk.Entry(win,font=('Century 12'),width=6,)
passLength.config({"background": "grey18"})
passLengthLabel = ttk.Label(win,font=('Century 12'),width=7, text="Length", anchor='center', background='grey14', foreground='Red')
passLengthLabel.grid()
passLengthLabel.place(x=227, y=200, anchor='w')
passLength.grid()
passLength.place(x=223, y=200, anchor='e')

GenerateButton= ttk.Button(win, text="Generate", command= generatePassword, width=8)
GenerateButton.grid()
GenerateButton.place(x=225, y=230, anchor='center')

readButton = ttk.Button(win, text="Read Passwords", command= readData, width=16)
readButton.grid()
readButton.place(x=60, y=530, anchor='center')

saveButton = ttk.Button(win, text="Save Password", command= sendToDatabase, width=16)
saveButton.grid()
saveButton.place(x=180, y=530, anchor='center')


win.mainloop()
