'''
Created on 18 mrt. 2014

@author: Pieter
'''
import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
from practicumbank import db, helper
import practicumbank
import os

def initialize():
    practicumbank.PAD = os.path.abspath(__file__)
    practicumbank.DIR = os.path.dirname(practicumbank.PAD)
    practicumbank.CONF  = {
                       '/': {
                             'tools.staticdir.root':  os.path.join(practicumbank.DIR,'data')
                             },
                       '/interfaces':{
                             'tools.staticdir.on': True,
                             'tools.staticdir.dir': "interfaces"
                             }
                       }
    helper.dbcheck()



def serve_template(templatename, **kwargs):

    _hplookup = TemplateLookup(directories=['data/interfaces/my_own/'])

    try:
        template = _hplookup.get_template(templatename)
        return template.render(**kwargs)
    except:
        return exceptions.html_error_template().render()


class pracdb():
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("home")
    @cherrypy.expose
    def home(self):
        return serve_template("home.html")
    @cherrypy.expose
    def upload(self,*args,**kwargs):
        invul={}
        error=[]
        if kwargs:
            errorflag=False
            #check voor compleetheid
            if len(kwargs["klas"])==0:
                error.append("Geen klas ingevuld")
                errorflag=True
                invul['klas']="0"
            elif (kwargs['klas']=="nieuw" and len(kwargs['klasnieuw'])==0) or \
                 (kwargs['klas']=="nieuw" and not kwargs['klasnieuw'].isdigit()) or \
                 (kwargs['klas']=="nieuw" and not int(kwargs['klasnieuw']) in range(1,7)):
                error.append("Geen geldige nieuwe klas ingevuld")
                errorflag=True
                invul['klas']="nieuw"
            else:
                invul['klas']=kwargs['klas']

            if len(kwargs["hoofdstuk"])==0:
                error.append("Geen hoofdstuk gekozen")
                errorflag=True
                invul['hoofdstuk']=''
            elif (kwargs['hoofdstuk']=="nieuw" and len(kwargs['hoofdstuknieuw'])==0):
                error.append("Geen nieuw hoofdstuk ingevuld hoofdstuk gekozen")
                errorflag=True
                invul['hoofdstuk']="nieuw"
            else:
                invul['hoofdstuk']=kwargs['hoofdstuk']
            if len(kwargs["naam"])==0:
                error.append("Geen naam ingevuld")
                errorflag=True
            else:
                invul['naam']=kwargs['naam']

            if 'cb' in kwargs.keys():
                print kwargs['cb']
                invul['cb']=kwargs['cb']
            else:
                invul['cb']="off"

            if not helper.checkFile(kwargs['docxfile']):
                error.append("Geen geldig word-bestand")
                errorflag=True

            if len(kwargs['pdffile'].filename)>0 and not helper.checkFile(kwargs['pdffile'],"pdf"):
                error.append("Geen geldig pdf-bestand")
                errorflag=True

            if errorflag:
                myDB=db.DBConnection()
                items = myDB.select("SELECT hoofdstuk, klas FROM practica")
                return serve_template("upload.html",erro=error,bekenden=dict(items),ingevuld=invul)
            else:
                bestandsnamen = helper.processUpload(kwargs)
                print bestandsnamen
        myDB=db.DBConnection()
        items = myDB.select("SELECT hoofdstuk, klas FROM practica")
        return serve_template("upload.html",erro="",bekenden=dict(items),ingevuld={"klas":"0","hoofdstuk":"","Naam":"","cb":"off"})
    @cherrypy.expose
    def download(self):
        return serve_template("download.html")

if __name__=="__main__":
    initialize()
    root = pracdb()
    cherrypy.quickstart(root,config=practicumbank.CONF)
