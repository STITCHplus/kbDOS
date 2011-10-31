#!/usr/bin/env python

## 
##  analyze_dossier.py - analyze_dossier
##  copyright (c) 2009-2010 Koninklijke Bibliotheek - National library of the Netherlands.
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


import urllib
import hashlib, pickle
import os, sys, re
from pprint import pprint

__author__ = "Willem Jan Faber"


def fetch_parse():

    data=urllib.urlopen("http://www.kb.nl/dossiers/index.html").read()

    doss = {}

    for line in data.split('\n'):
        if line.find('class="link"') > -1:
            category_url=(line.strip().split('"')[1])
            name=(line.strip().split('>')[1].split("<")[0])
            if category_url.startswith("/dossiers"):
                #print(category_url, name)
                url=("http://www.kb.nl"+category_url)

                name1=hashlib.md5(url).hexdigest()
                
                try:
                    file=open('/tmp/'+name1, "r")
                    avail=data.read()
                    file.close()
                except:
                    file=open('/tmp/'+name1, "w")
                    avail = urllib.urlopen(url).read()
                    file.write(avail)
                    file.close()
                for line in avail.split('\n'):
                    if line.find("a href") > -1 and line.find('class="link"') > -1:
                        if (line.split('"')[1]).startswith('/dossiers'):
                            link=(line.split('"')[1])
                            if not name in doss.keys():
                                doss[name]={}
                                doss[name][line.split('>')[1].split('<')[0]]=link
                            else:
                                doss[name][line.split('>')[1].split('<')[0]]=link
    dossier={}

    for item in doss.keys():
        for dos in doss[item]:
            name="/tmp/"+hashlib.md5(doss[item][dos]).hexdigest()
            try:
                file=open(name, "r")
                data=file.read()
                file.close()
            except:
                file=open(name, "w")
                data=urllib.urlopen("http://www.kb.nl/"+doss[item][dos]).read()
                file.write(data)
                file.close()
            for line in data.split('\n'):
                line=line.replace('\xc2\xa0', ' ')
                if line.find('bijgewerkt') > -1:
                    line=line.strip().replace('</em>', ' ').replace('<em>', ' ').replace('<p>', ' ')
                    dow=(re.match('.+?(\d+).+(\d+).+', line.split('<')[0].strip()).group(1))
                    jr=(re.match('.*(\d\d\d\d).*', line.split('<')[0].strip()).group(1))

                    name=hashlib.md5(doss[item][dos]).hexdigest()

                    dossier[name]={}
                    dossier[name]['url']="http://www.kb.nl"+doss[item][dos]
                    dossier[name]['name']=dos
                    dossier[name]['cat']=item
                    dossier[name]['date']=(dow, line[line.find(dow)+2:].strip().split(' ')[0], jr)


    cat_list={}
    for item in dossier.keys():
        if dossier[item]['cat'] not in cat_list.keys():
            cat_list[dossier[item]['cat']]={}
            cat_list[dossier[item]['cat']][item]=[]
            cat_list[dossier[item]['cat']][item].append(dossier[item])
        else:
            cat_list[dossier[item]['cat']][item]=[]
            cat_list[dossier[item]['cat']][item].append(dossier[item])

    output = open('data.pkl', 'wb')
    pickle.dump(cat_list, output)
    pprint(cat_list)


if __name__ == "__main__":
    try:
        data = pickle.load(open("data.pkl", "r"))
        for item in data.keys():
            print(item)
            dos=data[item]
            for key in dos.keys():
                print("\t"+data[item][key][0]["name"].replace('\n','')+" : "+data[item][key][0]["url"])
    except:
        fetch_parse()

    
