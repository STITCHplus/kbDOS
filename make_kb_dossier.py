#!/usr/bin/env python
# -*- coding: utf-8 -*-

## 
##  make_kb_dossier - make_kb_dossier.py
##
##  copyright (c) 2009-2010 Faber, Willem Jan 
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


from xml.etree import ElementTree as et
from pprint import pprint

from kbdos import Get_Dossier as dos

curdos=dos("http://www.kb.nl/dossiers/wijn/index.html")


title = curdos.title()
fulltext = curdos.fulltext()
links = curdos.links()
images = curdos.images()

leadtext= ".".join(fulltext.split(".")[1:])[0:200]

subject=title

icon_data, icon_size = curdos.gen_icon(images[0][0])

doc = et.Element("dossier")
add = et.SubElement(doc, 'dc')

dtype = et.SubElement(add, 'type', {'xml:lang':  'nl'})
dtype.text="dossier"

dtype = et.SubElement(add, 'title')
dtype.text=title

dtype = et.SubElement(add, 'subject')
dtype.text=subject

dtype = et.SubElement(add, 'identifier', {'type':'dcterms:URI'})
dtype.text=curdos.url

dtype = et.SubElement(add, 'isPartOf', {'type':'dcx:collectionIdentifier'})
dtype.text="Dossier"

dtype = et.SubElement(add, 'issued')
dtype.text="22-06-2009"

dtype = et.SubElement(add, 'contributor')
dtype.text="Naam medewerker"

dtype = et.SubElement(add, 'publisher')
dtype.text="KB"

dtype = et.SubElement(doc, 'icon', {'type':  'png', 'size' : str(icon_size[0])+"x"+str(icon_size[1]), 'encoding' : 'uuencode'})
dtype.text=icon_data

dtype = et.SubElement(doc, 'leadtext')
dtype.text=leadtext

dtype = et.SubElement(doc, 'fulltext')
dtype.text=fulltext

linkname = et.SubElement(doc, 'related_links')

for item in links:
    dtype = et.SubElement(linkname, 'link')
    dtype.text=item.pop()
    dtype = et.SubElement(linkname, 'linkname')
    dtype.text=item.pop()

images=images[0]

for item in images:
    if item.endswith(".jpg"):
        data, size = curdos.img_to_xml(item)
    else:
        dtype = et.SubElement(doc, 'image', { 'type' : 'jpg', 'size' : str(size[0])+"x"+str(size[1]), "encoding" : 'uuencode', "description":item})
        dtype.text=data


print(et.tostring(doc))


