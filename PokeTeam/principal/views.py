#encoding:utf-8
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.conf import settings
from django.db.models import Max
from principal.models import Pokemon, Poke_photo
from principal.collect import *
from principal.search import *
from principal.forms import equipo_form
from django.http import HttpResponseRedirect

#LOAD
def cargar(request):    
    leer_pagina()
    almacenar_datos()
    html="<html><body>Datos cargados correctamente</body></htm>"
    return HttpResponse(html)

#muestra la pagina de inicio
def inicio(request):
    return render(request,'inicio.html')

#muestra la lista de todos los pokemon
def lista_pokemons(request):
    pokemons=extraer_datos()[0]
    for i in pokemons:
        i.id = i.id[1:]
    return render(request,'pokemons.html', {'pokemons':pokemons})

#muestra detalles de un pokemon
def detalle_pokemon(request, pokemon_id):
    pokemon = buscar_por_id("#"+pokemon_id)
    foto = buscar_foto_pokemon_id("#"+pokemon_id)
    return render(request,'pokemon.html',{'pokemon':pokemon, "foto": foto})

#muestra un formulario para crear un equipo pokemon muy competitivo
def equipo(request):
    return render(request,'equipo.html')



def equipo(request):
    lista_tipos = "Acero/Agua/Bicho/Dragón/Electrico/Fantasma/Fuego/Hada/Hielo/Lucha/Normal/Planta/Psiquico/Roca/Siniestro/Tierra/Veneno/Volador".lower().split("/")
    lista_stats = ["Daño", "Vida", "Velocidad", "Defensa"]
    if request.method == 'POST':
        form = equipo_form(request.POST)
        if form.is_valid(): 
            pokemon_favorito = form.cleaned_data['pokemon_favorito']
            stats_pk_1 = form.cleaned_data['stats_pk_1']
            tipo_pk_1 = form.cleaned_data['tipo_pk_1'].lower()
            stats_pk_2 = form.cleaned_data['stats_pk_2']
            tipo_pk_2 = form.cleaned_data['tipo_pk_2'].lower()
            
            equipo = crear_equipo(pokemon_favorito,stats_pk_1,tipo_pk_1,stats_pk_2,tipo_pk_2)
            for i in equipo:
                i.id = i.id[1:]
                i.foto_url = buscar_foto_pokemon_id("#"+i.id).url
            

            return render(request, 'equipo.html', {"equipo": equipo, "lista_stats": lista_stats,  "lista_tipos": lista_tipos})

    else:
        form = equipo_form()

    return render(request, 'equipo.html', {'form': form, "equipo": [], "lista_stats": lista_stats,  "lista_tipos": lista_tipos})