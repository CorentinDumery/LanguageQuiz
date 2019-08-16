

# TODO

# améliorer la reconnaissance de texte 
# pondérer la fréquence d'apparition en fonction de la fréquence d'échec de chaque mot


import ezodf
from random import *
from time import sleep
from tkinter import *
from PIL import Image, ImageTk

doc = ezodf.opendoc('resources/hsk3.ods')


sheet = doc.sheets[0]

sino = []
pinyin = []
english = []

def testStr(str1,str2):
    return str1.lower() == str2.lower()

for i, row in enumerate(sheet.rows()):
    # row is a list of cells
    # assume the header is on the first row
    if i == 0:
        # columns as lists in a dictionary
        # create index for the column headers
        col_index = {j:cell.value for j, cell in enumerate(row)}
        continue
    skip = False
    for j, cell in enumerate(row):
        if j>3:
            break
        if j==0:
            skip = False
            sino.append(cell.value)
        if j==1:
            if cell.value=="zz":
                sino.pop()
                skip = True
            else:
                pinyin.append(cell.value)
        if j==2 and not(skip):
            english.append(cell.value)

        
hintsGiven = 0
totalLetters = 0

fen = Tk() #creation de la fenetre
     
tickI = Image.open("resources/tick.png")
tickI.thumbnail((48,48))
tickImage = ImageTk.PhotoImage(tickI)
crossI = Image.open("resources/cross.png")
crossI.thumbnail((48,48))
crossImage = ImageTk.PhotoImage(crossI)
        
entr1 = Entry(fen)
entr2 = Entry(fen)
entr3 = Entry(fen)

txt1Var = ""
txt2Var = ""
txt3Var = ""


pin1Var = ""
pin2Var = ""
pin3Var = ""

hintVar = "" #this one's for the ratio
hint1Var= ""
hint2Var=""
hint3Var=""
hintRatio = StringVar(fen)

entrList = [entr1,entr2,entr3]
sinoList = []
pinList = []
reponses = [] 
tickList = []
hintList = []

def onOkButton(): #note : this is also triggered with the enter key
    global reponses,totalLetters,hintsGiven
    
    fail = False
    
    for i in range(len(entrList)):
        answer = entrList[i].get()
        if len(reponses)==0:
            break
        if answer.lower() == reponses[i].lower():
            tickList[i].configure(image=tickImage)
            tickList[i].image = tickImage
        else:
            fail = True
            tickList[i].configure(image=crossImage)
            tickList[i].image = crossImage
            #hintList[i] = hintList[i]+reponses[i][len(hintList[i])]
            if len(hintList[i].get()) < len(reponses[i]):
                hintList[i].set(hintList[i].get()+reponses[i][len(hintList[i].get())])
                hintsGiven += 1
    
    
    #new test :
    if not(fail):
        reponses = []
        for i in range(len(sinoList)):
            totalLetters += len(english[i])
            entrList[i].delete(0, 'end')
            a = randrange(len(pinyin)) 
            sinoList[i].set(sino[a])
            pinList[i].set(pinyin[a])
            reponses.append(english[a])
            hintList[i].set("")
        if totalLetters :
            if len(str(hintsGiven/totalLetters)) > 4:
                hintRatio.set("Score : " +str((1- hintsGiven/totalLetters)*100)[0:3]+"%")
            else: 
                hintRatio.set("Score : " +str((1- hintsGiven/totalLetters)*100)+"%")
 

tick1 = Label(image=tickImage,width=130)
tick2 = Label(image=tickImage,width=130)
tick3 = Label(image=tickImage,width=130)

tickList = [tick1,tick2,tick3]

nbQ = 3

txt1Var = StringVar(fen)
txt2Var = StringVar(fen)
txt3Var = StringVar(fen)
hintVar = StringVar(fen)
pin1Var = StringVar(fen)
pin2Var = StringVar(fen)
pin3Var = StringVar(fen)

hint1Var = StringVar(fen)
hint2Var = StringVar(fen)
hint3Var = StringVar(fen)

sinoList.append(txt1Var)
sinoList.append(txt2Var)
sinoList.append(txt3Var)

pinList.append(pin1Var)
pinList.append(pin2Var)
pinList.append(pin3Var)

hintList.append(hint1Var)
hintList.append(hint2Var)
hintList.append(hint3Var)


txt1 = Label(fen, textvariable=txt1Var,height=0,width=5,font=("Courier", 70))
txt2 = Label(fen, textvariable=txt2Var,height=0,width=5,font=("Courier", 70))
txt3 = Label(fen, textvariable=txt3Var,height=0,width=5,font=("Courier", 70))
hintRatioLabel = Label(fen, textvariable=hintRatio,height=0,width=15,font=("Courier", 10))

txt1.grid(row = 0,column=1, sticky = "E")
txt2.grid(row = 1,column=1, sticky = "E")
txt3.grid(row = 2,column=1, sticky = "E")

pin1 = Label(fen, textvariable=pin1Var,height=0,width=10,font=("Courier", 20))
pin2 = Label(fen, textvariable=pin2Var,height=0,width=10,font=("Courier", 20))
pin3 = Label(fen, textvariable=pin3Var,height=0,width=10,font=("Courier", 20))

pin1.grid(row = 0,column=2, sticky = "E")
pin2.grid(row = 1,column=2, sticky = "E")
pin3.grid(row = 2,column=2, sticky = "E")

entr1.grid(row=0,column =3,sticky = "W")
entr2.grid(row=1,column =3)
entr3.grid(row=2,column =3)

tick1.grid(row=0,column=4)
tick2.grid(row=1,column=4)
tick3.grid(row=2,column=4)

hint1 = Label(fen, textvariable=hint1Var,height=0,width=10,font=("Courier", 20))
hint2 = Label(fen, textvariable=hint2Var,height=0,width=10,font=("Courier", 20))
hint3 = Label(fen, textvariable=hint3Var,height=0,width=10,font=("Courier", 20))
hint1.grid(row = 0,column=5, sticky = "E")
hint2.grid(row = 1,column=5, sticky = "E")
hint3.grid(row = 2,column=5, sticky = "E")

bou5 = Button(fen,text='OK', command = onOkButton)
bou5.grid(row=3, column= 1,columnspan=3, pady=5, padx= 10, ipadx = 50)
hintRatioLabel.grid(row = 3,column=5, sticky = "W")
#boup3 = Checkbutton(fen, text='Mode vert', command= modebr)
#boup3.grid(row =3, column=2,columnspan=1)

def onReturnKey(event): 
    onOkButton()

fen.bind('<Return>',    onReturnKey)  

fen.mainloop()


    
            
            





