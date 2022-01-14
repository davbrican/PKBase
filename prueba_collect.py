import urllib.request as urllib2
from bs4 import BeautifulSoup
import sqlite3
import json
import os
from urllib.request import Request, urlopen


def get_tipos():
    link = "https://pokemon.fandom.com/es/wiki/Tipos_elementales"
    
    response = urllib2.urlopen(link)
    soup = BeautifulSoup(response, 'lxml')
    
    dic_tipos = {}
    types_tables = soup.find("div", "resizable-container").find("div", ["page","has-right-rail"]).find("div", "page-content").find("div", "mw-parser-output").find("table", "galeria").find_all("tr")
    for i in range(1,len(types_tables)-1):
        tipo = types_tables[i].find_all("td")[0].find("a").string
        try:
            tipo_url = types_tables[i].find_all("td")[1].find("img")['data-src']
        except:
            tipo_url = types_tables[i].find_all("td")[1].find("img")['src']
            
        tipo = tipo.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        dic_tipos[tipo] = tipo_url
    
    return dic_tipos
print(get_tipos())