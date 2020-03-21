# coding=gbk
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont
import pdb
import os
import re

from config import *
from finalsmap import *

#### Open File
articleName = None
for fileName in os.listdir():
    if re.match(r'\w*\.txt', fileName) :
        articleName = fileName
        break
if articleName == None:
    exit()
articleContent = open(articleName, 'r').read()
articleKanjiNumber = len(articleContent)
articleLineNumber = articleKanjiNumber // y_size

from zhon import hanzi
import string
for i in hanzi.punctuation:
    articleContent = articleContent.replace(i,'')
for i in string.punctuation:
    articleContent = articleContent.replace(i,'')
articleContent = articleContent.replace('\n', '')
articleContent = articleContent.replace(' ', '')

#### Window Init
typeWindow = Tk()
typeWindow.title("汉字轰炸")
normalFont = tkFont.Font(family=fontName,
                         size=fontSize)

#### Font Init
kanjiWidth=int(normalFont.measure('你'))
realfontHeight = 1*fontSize
realFontSize = 1*fontSize

#### Display Widget(Binded)
displayArray = [StringVar() for i in range(min(y_size, articleLineNumber))]
for i in range(min(y_size, articleLineNumber)):
    displayBar = Label(typeWindow)
    displayBar.config(justify="right",
                      font="{} {}".format(fontName, fontSize),
                      textvariable=displayArray[i])
    displayBar.pack(padx=padding,pady=margin)
    displayArray[i].set(articleContent[i*x_size:(i+1)*x_size])

#### Pinyin Preparation
from pypinyin import pinyin, Style
x_pointer = 0
y_pointer = 0
positionFlag = 0
def getAvaliableList(x,y):
    avaliableList = []
    tempAvaliableList = []
    kanji = displayArray[y].get()[x]
    initialsList = pinyin(kanji, strict=False,
                              style=Style.INITIALS, heteronym=True)[0]
    finalsList = pinyin(kanji,strict=False,
                            style=Style.FINALS, heteronym=True)[0]
    firstKeyList=[]
    if initialsList[0] != '':
        firstKeyList = [doubleFinalsMap[i] for i in initialsList]
    if len(firstKeyList) != 0:#Normal
        secondKeyList = [doubleFinalsMap[i] for i in finalsList]
        return [firstKeyList, secondKeyList]

    firstKeyList = []
    secondKeyList = []

    for i in finalsList:
        firstKeyList.append((singleFinalsMap[i])[0])
        secondKeyList.append((singleFinalsMap[i])[1])
    return [firstKeyList, secondKeyList]
        
avaliableList = getAvaliableList(0,0)
def keyListener(event):
    global avaliableList
    global positionFlag
    global x_pointer
    global y_pointer
    global typeWindow
    key = event.char
    if key not in avaliableList[positionFlag]:
        return
    positionFlag += 1
    if positionFlag == 2:
        positionFlag = 0
        tempList = list(displayArray[y_pointer].get())
        tempList[x_pointer] = '　'
        displayArray[y_pointer].set(''.join(tempList))
        x_pointer += 1
        if x_pointer == x_size:
            x_pointer = 0
            y_pointer += 1
            if(y_pointer == y_size):
                import time
                for i in range(20):
                    time.sleep(0.01)
                    typeWindow.attributes("-alpha", (20-i)/20)
                exit()
        avaliableList = getAvaliableList(x_pointer, y_pointer)
typeWindow.bind("<Key>", keyListener)
mainloop()
        
