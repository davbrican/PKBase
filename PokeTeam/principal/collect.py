import urllib.request as urllib2
from bs4 import BeautifulSoup
import sqlite3
import json
import os
from urllib.request import Request, urlopen
from principal.models import *


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

def get_legendary_pokemon():
    link = "https://www.serebii.net/pokemon/legendary.shtml"
    
    response = urllib2.urlopen(link)
    soup = BeautifulSoup(response, 'lxml')
    
    lista_legendarios = []
    legendary_tables = soup.find("body").find_all("div")[1].find_all("table", "trainer")
    for i in range(len(legendary_tables)):
        pokes = legendary_tables[i].find_all("table")
        for z in pokes:
            nombre = z.find_all("tr")[1].find("td").find("a").string
            lista_legendarios.append(nombre)
        
    return lista_legendarios


def leer_pagina():
    lista_imgs_tipos = get_tipos()
    lista_legendarios = get_legendary_pokemon()
    
    link = "https://www.pkparaiso.com/pokemon/lista-pokemon.php"
    
    response = urllib2.urlopen(link)
    soup = BeautifulSoup(response, 'lxml')
    
    pokemons = soup.find("table", ["dex","sortable"]).find_all("tr")

    lista = []
    imagenes = []
    
    for i in range(1, len(pokemons)):
        data = pokemons[i].find_all("td")

        url = "https://pkparaiso.com" + data[1].find("span").find("a")["href"]

        tipos_urls = []
        tipos_pkm = [j.split("/")[-1].split(".")[0] for j in [i["src"] for i in data[3].find_all("img")]]
        for j in tipos_pkm:
            tipos_urls.append(lista_imgs_tipos[j])
        json_pokemon = {
            "id": data[2].find("a").string.split(" ")[0],
            "nombre": " ".join(data[2].find("a").string.split(" ")[1:]),
            "tipos": tipos_urls,
            "salud": int(data[-7].string),
            "ataque": int(data[-6].string),
            "defensa": int(data[-5].string),
            "velocidad": int(data[-4].string),
            "ataque_especial": int(data[-3].string),
            "defensa_especial":  int(data[-2].string),
            "total": int(data[-1].string)
        }

        #new_pokemon = Pokemon(json_pokemon["id"], json_pokemon["nombre"], json_pokemon["tipos"], json_pokemon["salud"], json_pokemon["ataque"], json_pokemon["defensa"], json_pokemon["velocidad"], json_pokemon["ataque_especial"], json_pokemon["defensa_especial"], json_pokemon["total"])
        #nombre_url = json_pokemon["nombre"].lower().replace(" ", "-").replace("♀", "-f").replace("♂", "-m").replace("’", "").replace(".", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        
        nombre_url = json_pokemon["nombre"].replace(" ", "_")
        
        try:
            req = Request('https://pokemon.fandom.com/es/wiki/'+nombre_url)
            response2 = urlopen(req).read()
            #req = Request('https://pokemondb.net/pokedex/'+nombre_url, headers={'User-Agent': 'Mozilla/5.0'})
            #response2 = urlopen(req).read()

            soup2 = BeautifulSoup(response2, 'lxml')
            #pic = soup2.find_all("div",["grid-col","span-md-6","span-lg-4","text-center"])[2].find("a").find("img")["src"]
            pic = soup2.find("img", "pi-image-thumbnail")["src"]
            print(pic)
        except:
            pic = ""
            
        json_pokemon["foto"] = pic
        
        print(json_pokemon["id"] + " - " + json_pokemon["nombre"])
        redireccion = "/loading/" + json_pokemon["id"]
        lista.append(json_pokemon)
        
    
    with open(os.path.dirname(__file__) + "/pokemons.json", "w", encoding="UTF-8") as file:
        json.dump({"lista_pokemons": lista, "lista_legendarios": lista_legendarios}, file)





def extraer_datos():
    with open(os.path.dirname(__file__) + "/pokemons.json", "r", encoding="UTF-8") as file:
        archivo = json.load(file)
        lista_pokemons = archivo["lista_pokemons"]
        lista_legendarios = archivo["lista_legendarios"]
        
    lista = []
    lista_photos = []
    for i in lista_pokemons:
        new_photo = Poke_photo(i["id"], i["foto"])
        new_pokemon = Pokemon(i["id"], i["nombre"], i["tipos"], i["salud"], i["ataque"], i["defensa"], i["velocidad"], i["ataque_especial"], i["defensa_especial"], i["total"])
        lista.append(new_pokemon)
        lista_photos.append(new_photo)


    return [lista, lista_photos, lista_legendarios]
