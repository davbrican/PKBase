from principal.models import Pokemon, Poke_photo
from principal.collect import *
import whoosh.query
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD, ID, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
import re, os, shutil


def almacenar_datos():
    schem = Schema(id=ID(stored=True,unique=True), nombre=TEXT(stored=True), tipos=KEYWORD(stored=True,commas=True,lowercase=True),
    salud=NUMERIC(stored=True),ataque=NUMERIC(stored=True),defensa=NUMERIC(stored=True),ataque_especial=NUMERIC(stored=True),
    defensa_especial=NUMERIC(stored=True),total=NUMERIC(stored=True), velocidad=NUMERIC(stored=True), url_photo=TEXT(stored=True))

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    i=0
    lista=extraer_datos()[0]
    for index in range(len(lista)):
        pokemon = lista[index]
        foto = extraer_datos()[1][index]
        writer.add_document(id=pokemon.id, nombre=pokemon.nombre, tipos=",".join(pokemon.tipos), salud=pokemon.salud, ataque=pokemon.ataque, defensa=pokemon.defensa, ataque_especial=pokemon.ataque_especial, defensa_especial=pokemon.defensa_especial, total=pokemon.total, velocidad=pokemon.velocidad, url_photo=foto.url)
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

def buscar_foto_pokemon_id(entrance):
    ix=open_dir("Index")
    
    with ix.searcher() as searcher:
        query = QueryParser("id", ix.schema).parse(entrance)

        results = searcher.search(query)

        for res in results:
            return Poke_photo(res["id"], res["url_photo"])


def buscar_pokemon_stats(entrance):
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
    pokemon_list = buscar_pokemon_stats(stats)
    if stats == "Daño":
        pokemon_list.sort(key=lambda x: (x.ataque, x.ataque_especial), reverse=True)
    elif stats == "Vida":
        pokemon_list.sort(key=lambda x: x.salud, reverse=True)
    elif stats == "Velocidad":
        pokemon_list.sort(key=lambda x: x.velocidad, reverse=True)
    elif stats == "Defensa":
        pokemon_list.sort(key=lambda x: (x.defensa, x.defensa_especial), reverse=True)


    tipos_ls = buscar_pokemon_tipo(tipo)
    tipos_names = [i.nombre for i in tipos_ls]
    
    lista_legendarios = extraer_datos()[2]
    
    for res in pokemon_list:
        if res.nombre in tipos_names and res.nombre not in lista_legendarios:
            return res

    return pokemon_list[0]


def buscar_por_id(entrance):
    ix=open_dir("Index")
    

    with ix.searcher() as searcher:
        query = QueryParser("id", ix.schema).parse(entrance)

        results = searcher.search(query)

        for res in results:
            return Pokemon(res["id"], res["nombre"], res["tipos"], res["salud"], res["ataque"], res["defensa"], res["velocidad"], res["ataque_especial"], res["defensa_especial"], res["total"])
    
def crear_equipo(pokemon_favorito,stat_pk_1,tipo_pk_1,stat_pk_2,tipo_pk_2):
    '''
    pokemon_favorito = input()
    stat_pk_1 = input("Daño/Vida/Velocidad/Defensa    ")
    tipo_pk_1 = input("Acero/Agua/Bicho/Dragón/Eléctrico/Fantasma/Fuego/Hada/Hielo/Lucha/Normal/Planta/Psíquico/Roca/Siniestro/Tierra/Veneno/Volador   ")
    stat_pk_2 = input("Daño/Vida/Velocidad/Defensa    ")
    tipo_pk_2 = input("Acero/Agua/Bicho/Dragón/Eléctrico/Fantasma/Fuego/Hada/Hielo/Lucha/Normal/Planta/Psíquico/Roca/Siniestro/Tierra/Veneno/Volador   ")
    '''
    pokemon_fav = buscar_pokemon_nombre(pokemon_favorito)
    pokemon_1 = buscar_stats_por_tipo(stat_pk_1, tipo_pk_1)
    pokemon_2 = buscar_stats_por_tipo(stat_pk_2, tipo_pk_2)
    

    lista_tipos = "Acero/Agua/Bicho/Dragón/Electrico/Fantasma/Fuego/Hada/Hielo/Lucha/Normal/Planta/Psiquico/Roca/Siniestro/Tierra/Veneno/Volador".lower().split("/")
    lista_stats = ["Daño", "Vida", "Velocidad", "Defensa"]
    lista_usado = [stat_pk_1, stat_pk_2]

    stat_pk_3 = [i for i in lista_stats if i not in lista_usado][0]
    lista_usado.append(stat_pk_3)

    stat_pk_4 = [i for i in lista_stats if i not in lista_usado][0]
    lista_usado.append(stat_pk_4)

    #Usar contrapuestos
    #Si ya llevo auga, y no fuego, usar fuego, usar scraping de la pagina de valores tabla de tipos

    lista_tipos_usados = [pokemon_fav.tipos.split(",")[0], pokemon_fav.tipos.split(",")[1], pokemon_1.tipos.split(",")[0], pokemon_1.tipos.split(",")[1], pokemon_2.tipos.split(",")[0], pokemon_2.tipos.split(",")[1]]

    tipo_pk_3 = ""
    for i in ["agua", "fuego", "dragon", "psiquico", "electrico", "planta", "volador"]:
        if i not in lista_tipos_usados:
            tipo_pk_3 = i
            break

    if tipo_pk_3 == "":
        if "lucha" not in lista_tipos_usados:
            tipo_pk_3 = "lucha"
        elif "fantasma" not in lista_tipos_usados:
            tipo_pk_3 = "fantasma"
        elif "acero" not in lista_tipos_usados:
            tipo_pk_3 = "acero"
        else:
            for tip in lista_tipos:
                if tip not in lista_tipos_usados:
                    tipo_pk_3 = tip
                    break


    pokemon_3 = buscar_stats_por_tipo(stat_pk_3, tipo_pk_3)
    lista_tipos_usados.append(pokemon_3.tipos.split(",")[0])
    lista_tipos_usados.append(pokemon_3.tipos.split(",")[1])

    
    tipo_pk_4 = ""
    for i in ["agua", "fuego", "dragon", "psiquico", "electrico", "planta", "volador"]:
        if i not in lista_tipos_usados:
            tipo_pk_4 = i
            break

    if tipo_pk_4 == "":
        if "lucha" not in lista_tipos_usados:
            tipo_pk_4 = "lucha"
        elif "fantasma" not in lista_tipos_usados:
            tipo_pk_4 = "fantasma"
        elif "acero" not in lista_tipos_usados:
            tipo_pk_4 = "acero"
        else:
            for tip in lista_tipos:
                if tip not in lista_tipos_usados:
                    tipo_pk_4 = tip
                    break
                
    pokemon_4 = buscar_stats_por_tipo(stat_pk_4, tipo_pk_4)
    lista_tipos_usados.append(pokemon_4.tipos.split(",")[0])
    lista_tipos_usados.append(pokemon_4.tipos.split(",")[1])

    lista_stats_usadas = [stat_pk_1, stat_pk_2, stat_pk_3, stat_pk_4]
    for i in lista_stats_usadas:
        if i in lista_stats:
            stat_pk_5 = "Daño"
        else:
            stat_pk_5 = i
            break

    tipo_pk_5 = ""
    for i in ["agua", "fuego", "dragon", "psiquico", "electrico", "planta", "volador"]:
        if i not in lista_tipos_usados:
            tipo_pk_5 = i
            break

    if tipo_pk_5 == "":
        if "lucha" not in lista_tipos_usados:
            tipo_pk_5 = "lucha"
        elif "fantasma" not in lista_tipos_usados:
            tipo_pk_5 = "fantasma"
        elif "acero" not in lista_tipos_usados:
            tipo_pk_5 = "acero"
        else:
            for tip in lista_tipos:
                if tip not in lista_tipos_usados:
                    tipo_pk_5 = tip
                    break
    
    pokemon_5 = buscar_stats_por_tipo(stat_pk_5, tipo_pk_5)


    return [pokemon_fav, pokemon_1, pokemon_2, pokemon_3, pokemon_4, pokemon_5]
