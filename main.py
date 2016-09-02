# -*- coding: utf-8 -*-

import Tkinter as tk
import cv2
from PIL import Image, ImageTk
import datetime
import time

#RECORD AND CHANGE VIEW BUTTON FUNCTIONS

def change():
    global output
    if b.cget('text') == u"MOG":
        b.config(text=u"RAW")
    else:
       b.config(text=u"MOG")

def recordPlay():
    if b2.cget('text') == u'⬤':
        b2.config(text=u"⬛", fg="snow")
    else:
       b2.config(text=u"⬤", fg="#ff4d4d")


############GUI#############

window = tk.Tk()
window.wm_title("")
window.wm_geometry("880x400")
window.resizable(width=False, height=False)
window.iconbitmap('icon.ico')
image = Image.open("gui.jpg")
photo = ImageTk.PhotoImage(image)


#VIDEO FRAME
label = tk.Label(image=photo)
label.image = photo # keep a reference!
label.place(x=0, y=0, relwidth=1, relheight=1)
imageFrame = tk.Frame(window, width=600, height=500,bd=0,background="#1a1a1a")
imageFrame.grid(row=0, rowspan=12,column=2, columnspan=1,padx=2.5)
lmain2 = tk.Label(imageFrame,bd=0,background="#1a1a1a")
lmain2.grid(row=0, rowspan=12, column=2,columnspan=1)

#SCALE
w = tk.Scale(window, from_=1,fg="snow", to=100,width=13,length=300, orient=tk.HORIZONTAL,background="#5e5e5e", bd=0,highlightbackground="#5e5e5e", troughcolor="#666666")
w.grid(row=7,column=0,columnspan=2,padx=19,pady=18)

#STRING VARIABLES
var = tk.StringVar(window)
var.set("DVIX")
var2 = tk.StringVar(window)
var2.set(".avi")
var3 = tk.StringVar()
var3.set("C:/")

#DROPDOWN MENU (CODECS)
codecs = ['DVIX', 'XVID', 'FFMPEG', 'LAGS', 'MJPG']
option = tk.OptionMenu(window,var, *codecs)
option.config(bg = "#666666", bd=0, highlightbackground="snow", fg="white")
option.grid(row=8,column=0,pady=2)

#DROPDOWN MENU (EXTENSIONS)
extensions = ['.avi', '.mp4', '.h264', '.mov']
option2 = tk.OptionMenu(window,var2, *extensions)
option2.config(bg = "#666666", bd=0, highlightbackground="snow", fg="white")
option2.grid(row=8,column=1, pady=2)

#SAVE PATH ENTRY FIELD
e = tk.Entry(window, width=40, textvariable=var3)
e.grid(row=10,column=0, columnspan=2)

#VIDEO CAPTURE
lmain = tk.Label(imageFrame,bd=0)
lmain.grid(row=0, column=2, columnspan=2)
cap = cv2.VideoCapture("testfile.avi")

#VIDEO OUTPUT
fourcc = cv2.cv.CV_FOURCC('i', 'Y', 'U', 'V')
out = cv2.VideoWriter(str(e.get()),fourcc, 10.0, (640,480))

#MOG
fgbg = cv2.BackgroundSubtractorMOG()

#RECORD BUTTON
b2 = tk.Button(window, text=u"⬤", bg="#666666", fg="#ff4d4d",command=recordPlay, width=4,height=1,font=("Century Gothic", 8, "bold"))
b2.grid(row=0,rowspan=2,column=2,padx=12,pady=4,sticky=tk.NE)

#CHANGE VIEW BUTTON
b = tk.Button(window, text=u"MOG", bg="#666666", fg="snow", command=change, font=("Century Gothic", 7, "bold"))
b.grid(row=1,rowspan=2,column=2,pady=10,padx=15,sticky=tk.NE)


#DISPLAY VIDEO AND ANALYSIS FUNCTION
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (0,0), fx=0.845, fy=0.845)

    #MASK
    fgmask = fgbg.apply(frame)
    fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)

    #ANALYSIS
    white_pixels = cv2.countNonZero(fgmask)
    if white_pixels > w.get() * 1000:
        font = cv2.FONT_HERSHEY_SIMPLEX

        button_value = b2.cget('text')
        now = datetime.datetime.utcnow()

        if button_value != u"⬛":
            pass

        elif b.cget('text') == u"MOG" and button_value == u"⬛":
            cv2.rectangle(frame, (445,360),(525,390),(255, 77, 77),2)
            cv2.putText(frame, "UTC "+ str(now)[11:19], (300,382), font, 0.6,(255,255,255), 1,cv2.CV_AA)
            cv2.putText(frame, 'REC', (466,381), font, 0.6,(0,0,0), 1,cv2.CV_AA)

        else:
            cv2.rectangle(fgmask, (445,360),(525,390),(255, 77, 77),2)
            cv2.putText(fgmask, "UTC "+str(now)[11:19], (300,382), font, 0.6,(255,255,255), 1,cv2.CV_AA)
            cv2.putText(fgmask, 'REC', (466,381), font, 0.6,(255,255,255), 1,cv2.CV_AA)


    #CHANGE VIEW FUNCTION
    if b.cget('text') == "MOG":
        img = Image.fromarray(frame)
    else:
        img = Image.fromarray(fgmask)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk,)
    lmain.after(10, show_frame)

show_frame()
window.mainloop()

