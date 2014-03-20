'''
Created on 20 mrt. 2014

@author: Pieter
'''
import sqlite3
import practicumbank
import os

def dbcheck():

    conn=sqlite3.connect(r'data\pracdb.db')
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS practica (prac_id INTEGER PRIMARY KEY, klas NUMERIC, hoofdstuk TEXT, name TEXT, cb BOOLEAN, bestandsids TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS Bestanden (bestands_id INTEGER PRIMARY KEY, bestandsnaam TEXT, extensie TEXT);")

    conn.commit()
    c.close()

def checkFile(myfile,wantedext="docx"):
    if myfile.filename.split(".")[-1] == wantedext:
        return True
    else:
        return False

def saveFile(myfile,pad,naam):
    echtenaam=naam+"."+myfile.filename.split(".")[-1]
    echtpad=os.path.normpath(os.path.join(practicumbank.DIR,pad))
    save_file = os.path.normpath(os.path.join(practicumbank.DIR,echtenaam))
    if not os.path.exists(echtpad):
            try:
                os.makedirs(echtpad)
            except:
                pass
    while True:
        data = myfile.file.read(8192)
        if not data:
            break
    with open(save_file, "wb") as f:  # Important to set mode to wb
        f.write(data)

def processUpload(kwargs):
    if kwargs['klas']=="nieuw":
        klas = kwargs['klasnieuw']
    else:
        klas=kwargs['klas']
    if kwargs['hoofdstuk'] =="nieuw":
        hoofdstuk = kwargs['hoofdstuknieuw']
    else:
        hoofdstuk=kwargs['hoofdstuk']
    naam = kwargs['naam']
    if "cb" in kwargs.keys():
        cb = kwargs['cb']
    else:
        cb="off"
    bestandsnaamenpad = practicumbank.PRACTICUM_DIR+"\\klas "+klas+"\\"+hoofdstuk+"\\"+naam
    bestandspad = practicumbank.PRACTICUM_DIR+"\\klas "+klas+"\\"+hoofdstuk
    saveFile(kwargs['docxfile'],bestandspad,bestandsnaamenpad)
    retlist=[os.path.normpath(bestandsnaamenpad+".docx")]
    if checkFile(kwargs['pdffile'],"pdf"):
        saveFile(kwargs['pdffile'],bestandspad,bestandsnaamenpad)
        retlist.append(os.path.normpath(bestandsnaamenpad+".pdf"))
    return retlist


