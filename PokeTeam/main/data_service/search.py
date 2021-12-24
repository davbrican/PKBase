from models import *
from collect import *
import whoosh.query
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD, ID, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
import re, os, shutil


def almacenar_datos():
    schem = Schema(id=ID(stored=True,unique=True), nombre=TEXT(stored=True), tipos=KEYWORD(stored=True,commas=True,lowercase=True),
    salud=NUMERIC(stored=True),ataque=NUMERIC(stored=True),defensa=NUMERIC(stored=True),ataque_especial=NUMERIC(stored=True),
    defensa_especial=NUMERIC(stored=True),total=NUMERIC(stored=True), velocidad=NUMERIC(stored=True))

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    i=0
    lista=extraer_datos()
    for pokemon in lista:
        writer.add_document(id=pokemon.id, nombre=pokemon.nombre, tipos=",".join(pokemon.tipos), salud=pokemon.salud, ataque=pokemon.ataque, defensa=pokemon.defensa, ataque_especial=pokemon.ataque_especial, defensa_especial=pokemon.defensa_especial, total=pokemon.total, velocidad=pokemon.velocidad)
        i+=1
    writer.commit()



def buscar_pokemon_nombre(entrance):
    ix=open_dir("Index")

    with ix.searcher() as searcher:
        query = QueryParser("nombre", ix.schema).parse(entrance)#MultifieldParser(["nombre","bodega"], ix.schema, group=OrGroup).parse(str(input()))

        results = searcher.search(query)

        pokemon = None
        for res in results:
            pokemon = Pokemon(res["id"], res["nombre"], res["tipos"], res["salud"], res["ataque"], res["defensa"], res["velocidad"], res["ataque_especial"], res["defensa_especial"], res["total"])
    
        return pokemon



def busar_pokemon_stats(entrance):
    ix=open_dir("Index")
    
    busqueda = "[ 150 TO 255 ]"

    with ix.searcher() as searcher:
        if entrance == "Daño":
            query = MultifieldParser(["ataque","ataque_especial"], ix.schema, group=OrGroup).parse(busqueda)
        elif entrance == "Vida":
            query = QueryParser("salud", ix.schema).parse(busqueda)
        elif entrance == "Velocidad":
            query = QueryParser("velocidad", ix.schema).parse(busqueda)
        elif entrance == "Defensa":
            query = MultifieldParser(["defensa","defensa_especial"], ix.schema, group=OrGroup).parse(busqueda)
        else:
            query = MultifieldParser(["salud","velocidad","defensa","defensa_especial","ataque","ataque_especial"], ix.schema, group=OrGroup).parse(busqueda)

        results = searcher.search(query,limit=802)

        pokemon_list = []
        for res in results:
            pokemon_list.append(Pokemon(res["id"], res["nombre"], res["tipos"], res["salud"], res["ataque"], res["defensa"], res["velocidad"], res["ataque_especial"], res["defensa_especial"], res["total"]))
    
        return pokemon_list
    
    
def buscar_pokemon_tipo(entrance):
    ix=open_dir("Index")      
    with ix.searcher() as searcher:
        lista_tipos = [i.decode('utf-8') for i in searcher.lexicon('tipos')]

        entrada = str(entrance.lower())

        if entrada not in lista_tipos:
            return []
        
        query = QueryParser("tipos", ix.schema).parse(entrada)
        results = searcher.search(query,limit=802) 
        
        pokemon_list = []
        for res in results:
            pokemon_list.append(Pokemon(res["id"], res["nombre"], res["tipos"], res["salud"], res["ataque"], res["defensa"], res["velocidad"], res["ataque_especial"], res["defensa_especial"], res["total"]))
    
        return pokemon_list


def buscar_stats_por_tipo(stats, tipo):
    tipos_ls = buscar_pokemon_tipo(tipo)
    tipos_names = [i.nombre for i in tipos_ls]
    ix=open_dir("Index")
    
    busqueda = "[ 1 TO 255 ]"

    with ix.searcher() as searcher:
        if stats == "Daño":
            query = MultifieldParser(["ataque","ataque_especial"], ix.schema, group=OrGroup).parse(busqueda)
        elif stats == "Vida":
            query = QueryParser("salud", ix.schema).parse(busqueda)
        elif stats == "Velocidad":
            query = QueryParser("velocidad", ix.schema).parse(busqueda)
        elif stats == "Defensa":
            query = MultifieldParser(["defensa","defensa_especial"], ix.schema, group=OrGroup).parse(busqueda)
        else:
            query = MultifieldParser(["salud","velocidad","defensa","defensa_especial","ataque","ataque_especial"], ix.schema, group=OrGroup).parse(busqueda)
            
        results = searcher.search(query,limit=802)

        pokemon_list = []
        for res in results:
            pokemon_list.append(Pokemon(res["id"], res["nombre"], res["tipos"], res["salud"], res["ataque"], res["defensa"], res["velocidad"], res["ataque_especial"], res["defensa_especial"], res["total"]))
    
        if stats == "Daño":
            pokemon_list.sort(key=lambda x: (x.ataque, x.ataque_especial), reverse=True)
        elif stats == "Vida":
            pokemon_list.sort(key=lambda x: x.salud, reverse=True)
        elif stats == "Velocidad":
            pokemon_list.sort(key=lambda x: x.velocidad, reverse=True)
        elif stats == "Defensa":
            pokemon_list.sort(key=lambda x: (x.defensa, x.defensa_especial), reverse=True)
        
        
        for res in pokemon_list:
            if res.nombre in tipos_names:
                return res
            
        return pokemon_list[0]
    
    
def crear_equipo():
    pokemon_favorito = input()
    stat_pk_1 = input("Daño/Vida/Velocidad/Defensa    ")
    tipo_pk_1 = input("Acero/Agua/Bicho/Dragón/Eléctrico/Fantasma/Fuego/Hada/Hielo/Lucha/Normal/Planta/Psíquico/Roca/Siniestro/Tierra/Veneno/Volador   ")
    stat_pk_2 = input("Daño/Vida/Velocidad/Defensa    ")
    tipo_pk_2 = input("Acero/Agua/Bicho/Dragón/Eléctrico/Fantasma/Fuego/Hada/Hielo/Lucha/Normal/Planta/Psíquico/Roca/Siniestro/Tierra/Veneno/Volador   ")
    
    pokemon_fav = buscar_pokemon_nombre(pokemon_favorito)
    pokemon_1 = buscar_stats_por_tipo(stat_pk_1, tipo_pk_1)
    pokemon_2 = buscar_stats_por_tipo(stat_pk_2, tipo_pk_2)
    
    print(pokemon_fav)
    print(pokemon_1)
    print(pokemon_2)

    