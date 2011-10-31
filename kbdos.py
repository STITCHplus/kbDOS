#!/usr/bin/env python


## 
##  kbdos - kbdos.py
##  copyright (c) 2009-2010 Koninklijke Bibliotheek - Nationale bibliotheek van Nederland).
##
##  this program is free software: you can redistribute it and/or modify
##  it under the terms of the gnu general public license as published by
##  the free software foundation, either version 3 of the license, or
##  (at your option) any later version.
##
##  this program is distributed in the hope that it will be useful,
##  but without any warranty; without even the implied warranty of
##  merchantability or fitness for a particular purpose.  see the
##  gnu general public license for more details.
##
##  you should have received a copy of the gnu general public license
##  along with this program.  if not, see <http://www.gnu.org/licenses/>.
##

__author__ = "Willem Jan Faber"

import urllib, os, sys
from BeautifulSoup import BeautifulSoup    
from pprint import pprint
from PIL import Image
import uu

DOS_FULLTEXT = 2
DOS_LINKS = 2
DOS_IMAGES = 3

class Get_Dossier(object):
    def __init__(self, url):
        self.url=url


    def title(self):
        data=BeautifulSoup(urllib.urlopen(self.url).read())
        return(data.find("h1").renderContents().strip())

    def gen_icon(self,url):
        data=urllib.urlopen(url).read()
        fh=open("/tmp/thumb", "w")
        fh.write(data)
        fh.close()


        size = 150,150
        im = Image.open("/tmp/thumb")
        im.thumbnail(size, Image.ANTIALIAS)
        im.save("/tmp/thumb.png", "PNG")

        uu.encode("/tmp/thumb.png" , "/tmp/thumb.xml")
        fh=open("/tmp/thumb.xml", "r")
        data=fh.read()
        fh.close()
        return([data,im.size])

    def img_to_xml(self, url):
        url=url.replace("-small", "")
        data=urllib.urlopen(url).read()
        fh=open("/tmp/img.jpg", "w")
        fh.write(data)
        fh.close()

        im = Image.open("/tmp/img.jpg")

        uu.encode("/tmp/img.jpg" , "/tmp/img.xml")

        fh=open("/tmp/img.xml", "r")
        data=fh.read()
        fh.close()

        return([data, im.size])


    def make_itterator(self, ttype):
        data=urllib.urlopen(self.url).read()
        soup=BeautifulSoup(data, fromEncoding="utf-8")
        i=0
        res=""

        for item in soup.findAll('div', attrs={"class" : "padding"}):
            i+=1
            if i == ttype:
                j=BeautifulSoup(item.encode('utf-8'))

                return(j)


    def fulltext(self):
        res=""
        j=self.make_itterator(DOS_FULLTEXT)
        for tag in j.findAll(True):
            if tag.name=="p" or tag.name.startswith("h"):
                if not tag.renderContents().find("<a") > -1:
                    if len(tag.renderContents().strip()) > 0:
                        res+="<p>"+tag.renderContents()+"</p>"
                else:
                    if not tag.renderContents().find("Literatuur") > -1 and not tag.renderContents().find("Links") > -1:
                        res+="\n<h3>"+tag.renderContents().split("<a")[0]+"</h3>"
        return(res)


    def links(self):
        links=[]
        j=self.make_itterator(DOS_LINKS)
        for tag in j.findAll(True):
            if tag.name == "a":
                if len(tag.renderContents())>  0:
                    t=tag.renderContents()
                    a=tag['href']
                    if not ((a.find("http://") > -1) or (a.find("www.") > -1)):
                        a="/".join(self.url.split("/")[:-1])+"/"+a
                    links.append([t,a])
        return(links)

    def images(self):
        j=self.make_itterator(DOS_IMAGES)
        links=[]
        link=[]
        for tag in j.findAll(True):
            if tag.name == "img":
                if not tag['src'].find("icon_zoom.gif") > -1:
                    baseurl="/".join(self.url.split("/")[:-1])
                    link.append(baseurl+"/"+tag['src'].split('/')[-1])
            if tag.name == "tr":
                a=BeautifulSoup(tag.renderContents())
                for name in a.findAll(True):
                    if name.name == "span":
                        link.append(name.renderContents())
        if len(link)> 0:
            links.append(link)
            link=[]
        return(links)
                        
 
if __name__ == "__main__":
    if (len(os.sys.argv)) > 1:
        dos=Get_Dossier(os.sys.argv[1])



        pprint(dos.get_fulltext())
        pprint(dos.get_links())
        pprint(dos.get_images())
    else:
        print("Please enter the dossier url")
        os._exit(-1)
