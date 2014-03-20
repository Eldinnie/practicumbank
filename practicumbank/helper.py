'''
Created on 20 mrt. 2014

@author: Pieter
'''
import sqlite3

def dbcheck():

    conn=sqlite3.connect(r'data\pracdb.db')
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS practica (prac_id INTEGER PRIMARY KEY, klas NUMERIC, hoofdstuk TEXT, name TEXT, cb BOOLEAN, bestandsids TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS Bestanden (bestands_id INTEGER PRIMARY KEY, bestandsnaam TEXT, extensie TEXT);")

    conn.commit()
    c.close()