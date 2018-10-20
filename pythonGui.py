from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np

class Example(Frame):
  in_path=""
  grayscaled=[]
  image=[]
  closing=[]
  threshold=[]
  image2=[]
  imgBienSo=[]
  def __init__(self, parent):
    Frame.__init__(self, parent)
 
    self.parent = parent

    self.initUI()
  
  def initUI(self):
    self.parent.title("Simple Menu")
    menuBar = Menu(self.parent)
    self.parent.config(menu=menuBar)
    fileMenu = Menu(menuBar)
    functionMenu=Menu(menuBar)
    aboutMenu=Menu(menuBar)
    fileMenu.add_command(label="Open",command=self.openFile)
    fileMenu.add_command(label="Save",command=self.saveImage)
    fileMenu.add_command(label="Exit", command=self.onExit)
    menuBar.add_cascade(label="File", menu=fileMenu)

    functionMenu.add_command(label="lam xam",command=self.grayImage)
    functionMenu.add_command(label="morphologyEx",command=self.morphologyEx)
    functionMenu.add_command(label="thredshold",command=self.normalize)
    functionMenu.add_command(label="loc",command=self.loc)
    functionMenu.add_command(label="lam nhoe", command=self.lam_nhoe)
    functionMenu.add_command(label="nhanDang",command=self.nhanDang)
    functionMenu.add_command(label="tach bien so",command=self.tachBienSo)
    menuBar.add_cascade(label="Function",menu=functionMenu)

    aboutMenu.add_command(label="About me")
    menuBar.add_cascade(label="About",menu=aboutMenu)

  def onExit(self):
    self.quit()
  def openFile(self):
    self.in_path = filedialog.askopenfilename()
    if self.in_path!="":
      minc = Image.open(str(self.in_path))
      mincol = ImageTk.PhotoImage(minc)
      label3 = Label(self.parent, image=mincol)
      label3.image = mincol
      label3.place(x=5, y=5)
    else:
      print("cuong")
  def grayImage(self):
    self.image=cv.imread(self.in_path)
    self.grayscaled = cv.cvtColor(self.image,cv.COLOR_BGR2GRAY)
    if self.in_path!="":
      minc = Image.fromarray(self.grayscaled)
      mincol = ImageTk.PhotoImage(minc)
      label3 = Label(self.parent, image=mincol)
      label3.image = mincol
      label3.place(x=5, y=5)
    else:
      print("cuong")
  def saveImage(self):
    toSave = tkFileDialog.asksaveasfile()
  def morphologyEx(self):
    kernel = np.ones((5,10),np.uint8)
    self.closing = cv.morphologyEx(self.grayscaled, cv.MORPH_BLACKHAT, kernel)
    if self.in_path!="":
      minc = Image.fromarray(self.closing)
      mincol = ImageTk.PhotoImage(minc)
      label3 = Label(self.parent, image=mincol)
      label3.image = mincol
      label3.place(x=5, y=5)
  def normalize(self):
    cv.normalize(self.closing,self.closing,0,255,cv.NORM_MINMAX)
    retval,self.threshold=cv.threshold(self.closing,100,255,cv.THRESH_BINARY)
    cv.imshow('normalize',self.threshold)
  def loc(self):
    w,h,chanel=self.image.shape
    kernel = np.ones((5,10),np.uint8)
    size = w, h, chanel
    for j in range(0,h+h,4):
      for i in range(0,w+w,4):
          img=self.threshold[j:j+8,i:i+16]
          nonezero1=cv.countNonZero(img)
          img=self.threshold[j:j+8,i+16:i+32]
          nonezero2=cv.countNonZero(img)
          img=self.threshold[j+8:j+16,i:i+16]
          nonezero3=cv.countNonZero(img)
          img=self.threshold[j+8:j+16,i+16:i+32]
          nonezero4=cv.countNonZero(img)
          cnt=0
          if(nonezero1<12):
            cnt+=1;
          if(nonezero2<12):
            cnt+=1;
          if(nonezero3<12):
            cnt+=1;
          if(nonezero4<12):
            cnt+=1;
          if(cnt>2):
      # print 'cnt=',cnt
            self.threshold[j:j+8,i:i+16]=[0]
    cv.imshow("threshold", self.threshold)

  def lam_nhoe(self):
    kernel = np.ones((5,10),np.uint8)
    self.image2=cv.dilate(self.threshold,kernel,2)
    cv.imshow("image2",self.image2)

  def nhanDang(self):
    w,h,chanel=self.image.shape
    kernel = np.ones((5,10),np.uint8)
    size = w, h, chanel
    im2, contours, hierarchy = cv.findContours(self.image2,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    for i in range(0,len(contours)):
      x,y,w,h = cv.boundingRect(contours[i])
      if float(w/h)>2 and float(h/w)<4:
        s=w*h

      if(w>80 and w<250 and h>15 and h<40):
          cv.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),1)
          self.imgBienSo=self.image[y:y+h,x:x+w]
    # cv.imshow('image',self.image)
    cv.imshow("imgBienSo",self.imgBienSo)

  def tachBienSo(self):
    grayscaled = cv.cvtColor(self.imgBienSo,cv.COLOR_BGR2GRAY)
    kernel = np.ones((5,10),np.uint8)
    w,h,chanel=self.imgBienSo.shape
    size = w, h, chanel
    closing = cv.morphologyEx(grayscaled, cv.MORPH_BLACKHAT, kernel)
    cv.normalize(self.closing,self.closing,0,255,cv.NORM_MINMAX)
    retval,th=cv.threshold(closing,100,255,cv.THRESH_BINARY)

    cv.imshow('th',th)

    # cv.imshow("image bien so grayscaled",grayscaled)
    im2, contours, hierarchy = cv.findContours(th,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
    print(contours)
    for i in range(0,len(contours)):
      x,y,w,h = cv.boundingRect(contours[i])
      if h>w:
        if(h>5 and w>5):
          img=[]
          img=th[y:y+h,x:x+w]
          cv.imshow('imso'+str(i),img)
      # cv.rectangle(image3,(x,y),(x+w,y+h),(0,255,0),1)

root = Tk()
root.geometry("800x500")
app = Example(root)
root.mainloop()