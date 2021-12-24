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
    defensa_especial=NUMERIC(stored=True),total=NUMERIC(stored=True))

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    i=0
    lista=extraer_datos()
    for pokemon in lista:
        writer.add_document(id=pokemon.id, nombre=pokemon.nombre, tipos=",".join(pokemon.tipos), salud=pokemon.salud, ataque=pokemon.ataque, defensa=pokemon.defensa, ataque_especial=pokemon.ataque_especial, defensa_especial=pokemon.defensa_especial, total=pokemon.total)
        i+=1
    writer.commit()



def buscar_pokemon_nombre():
    ix=open_dir("Index")

    with ix.searcher() as searcher:
        query = QueryParser("nombre", ix.schema).parse(str(input()))#MultifieldParser(["nombre","bodega"], ix.schema, group=OrGroup).parse(str(input()))

        results = searcher.search(query)

        for r in results:
            print(r["id"] + " - " + r["nombre"])
