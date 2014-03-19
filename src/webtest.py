'''
Created on 18 mrt. 2014

@author: Pieter
'''
import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import db
import sqlite3

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

def dbcheck():

    conn=sqlite3.connect(r'd:\Bibliotheek\Documenten\python\Worspace\web_test\src\data\pracdb.db')
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS practica (ArtistID TEXT UNIQUE, ArtistName TEXT, ArtistSortName TEXT, DateAdded TEXT, Status TEXT, IncludeExtras INTEGER, LatestAlbum TEXT, ReleaseDate TEXT, AlbumID TEXT, HaveTracks INTEGER, TotalTracks INTEGER, LastUpdated TEXT, ArtworkURL TEXT, ThumbURL TEXT, Extras TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS albums (ArtistID TEXT, ArtistName TEXT, AlbumTitle TEXT, AlbumASIN TEXT, ReleaseDate TEXT, DateAdded TEXT, AlbumID TEXT UNIQUE, Status TEXT, Type TEXT, ArtworkURL TEXT, ThumbURL TEXT, ReleaseID TEXT, ReleaseCountry TEXT, ReleaseFormat TEXT, SearchTerm TEXT)')   # ReleaseFormat here means CD,Digital,Vinyl, etc. If using the default Headphones hybrid release, ReleaseID will equal AlbumID (AlbumID is releasegroup id)
    c.execute('CREATE TABLE IF NOT EXISTS tracks (ArtistID TEXT, ArtistName TEXT, AlbumTitle TEXT, AlbumASIN TEXT, AlbumID TEXT, TrackTitle TEXT, TrackDuration, TrackID TEXT, TrackNumber INTEGER, Location TEXT, BitRate INTEGER, CleanName TEXT, Format TEXT, ReleaseID TEXT)')    # Format here means mp3, flac, etc.
    c.execute('CREATE TABLE IF NOT EXISTS allalbums (ArtistID TEXT, ArtistName TEXT, AlbumTitle TEXT, AlbumASIN TEXT, ReleaseDate TEXT, AlbumID TEXT, Type TEXT, ReleaseID TEXT, ReleaseCountry TEXT, ReleaseFormat TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS alltracks (ArtistID TEXT, ArtistName TEXT, AlbumTitle TEXT, AlbumASIN TEXT, AlbumID TEXT, TrackTitle TEXT, TrackDuration, TrackID TEXT, TrackNumber INTEGER, Location TEXT, BitRate INTEGER, CleanName TEXT, Format TEXT, ReleaseID TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS snatched (AlbumID TEXT, Title TEXT, Size INTEGER, URL TEXT, DateAdded TEXT, Status TEXT, FolderName TEXT, Kind TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS have (ArtistName TEXT, AlbumTitle TEXT, TrackNumber TEXT, TrackTitle TEXT, TrackLength TEXT, BitRate TEXT, Genre TEXT, Date TEXT, TrackID TEXT, Location TEXT, CleanName TEXT, Format TEXT, Matched TEXT)') # Matched is a temporary value used to see if there was a match found in alltracks
    c.execute('CREATE TABLE IF NOT EXISTS lastfmcloud (ArtistName TEXT, ArtistID TEXT, Count INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS descriptions (ArtistID TEXT, ReleaseGroupID TEXT, ReleaseID TEXT, Summary TEXT, Content TEXT, LastUpdated TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS blacklist (ArtistID TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS newartists (ArtistName TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS releases (ReleaseID TEXT, ReleaseGroupID TEXT, UNIQUE(ReleaseID, ReleaseGroupID))')
    c.execute('CREATE INDEX IF NOT EXISTS tracks_albumid ON tracks(AlbumID ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS album_artistid_reldate ON albums(ArtistID ASC, ReleaseDate DESC)')
    #Below creates indices to speed up Active Artist updating
    c.execute('CREATE INDEX IF NOT EXISTS alltracks_relid ON alltracks(ReleaseID ASC, TrackID ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS allalbums_relid ON allalbums(ReleaseID ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS have_location ON have(Location ASC)')
    #Below creates indices to speed up library scanning & matching
    c.execute('CREATE INDEX IF NOT EXISTS have_Metadata ON have(ArtistName ASC, AlbumTitle ASC, TrackTitle ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS have_CleanName ON have(CleanName ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS tracks_Metadata ON tracks(ArtistName ASC, AlbumTitle ASC, TrackTitle ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS tracks_CleanName ON tracks(CleanName ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS alltracks_Metadata ON alltracks(ArtistName ASC, AlbumTitle ASC, TrackTitle ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS alltracks_CleanName ON alltracks(CleanName ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS tracks_Location ON tracks(Location ASC)')
    c.execute('CREATE INDEX IF NOT EXISTS alltracks_Location ON alltracks(Location ASC)')

    conn.commit()
    c.close()