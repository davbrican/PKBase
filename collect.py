import urllib.request as urllib2
from bs4 import BeautifulSoup
import sqlite3
from models import *
import json
import os


def leer_pagina():

    link = "https://www.pkparaiso.com/pokemon/lista-pokemon.php"
    
    response = urllib2.urlopen(link)
    soup = BeautifulSoup(response, 'lxml')
    
    pokemons = soup.find("table", ["dex","sortable"]).find_all("tr")

    lista = []
    for i in range(1, len(pokemons)):
        data = pokemons[i].find_all("td")

        url = "https://pkparaiso.com" + data[1].find("span").find("a")["href"]

        json_pokemon = {
            "id": data[2].find("a").string.split(" ")[0],
            "nombre": data[2].find("a").string.split(" ")[1],
            "tipos": [j.split("/")[-1].split(".")[0] for j in [i["src"] for i in data[3].find_all("img")]],
            "salud": int(data[-6].string),
            "ataque": int(data[-5].string),
            "defensa": int(data[-4].string),
            "ataque_especial": int(data[-3].string),
            "defensa_especial":  int(data[-2].string),
            "total": int(data[-1].string)
        }

        new_pokemon = Pokemon(json_pokemon["id"], json_pokemon["nombre"], json_pokemon["tipos"], json_pokemon["salud"], json_pokemon["ataque"], json_pokemon["defensa"], json_pokemon["ataque_especial"], json_pokemon["defensa_especial"], json_pokemon["total"])
        print("\n-------------------- " + json_pokemon["id"] + " --------------------")
        print(url)
        print(new_pokemon)
        lista.append(json_pokemon)
        
    with open(os.path.dirname(__file__) + "/pokemons.json", "w", encoding="UTF-8") as file:
        json.dump({"lista_pokemons": lista}, file)



def extraer_datos():
    with open(os.path.dirname(__file__) + "/pokemons.json", "r", encoding="UTF-8") as file:
        lista_pokemons = json.load(file)["lista_pokemons"]
        
    lista = []
    for i in lista_pokemons:
        new_pokemon = Pokemon(i["id"], i["nombre"], i["tipos"], i["salud"], i["ataque"], i["defensa"], i["ataque_especial"], i["defensa_especial"], i["total"])
        lista.append(new_pokemon)

    return lista
