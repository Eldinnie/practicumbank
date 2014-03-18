'''
Created on 18 mrt. 2014

@author: Pieter
'''
import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
conf = {
        '/': {
            'tools.staticdir.root': r'D:\Bibliotheek\Documenten\python\Worspace\web_test\src\data'
        },
        '/interfaces':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "interfaces"
        },
        '/images':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "images"
        },
        '/css':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "css"
        },
        '/js':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "js"
        }
    }
def serve_template(templatename, **kwargs):

    _hplookup = TemplateLookup(directories=['data/interfaces/my_own/'])

    try:
        template = _hplookup.get_template(templatename)
        return template.render(**kwargs)
    except:
        return exceptions.html_error_template().render()

class test():
    exposed=True
    def __call__(self,num,**kwargs):
        print num,kwargs
        if num.isdigit() and 0<int(num)<5:
            return serve_template("test.html",number=num)
        else:
            raise cherrypy.HTTPRedirect("/test/1")

class webtest():
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("home")
    @cherrypy.expose
    def home(self):
        return serve_template("home.html")
    @cherrypy.expose
    def upload(self):
        return serve_template("upload.html")
    @cherrypy.expose
    def download(self):
        return serve_template("download.html")

if __name__=="__main__":
    root = webtest()
    root.test=test()
    cherrypy.quickstart(root,config=conf)