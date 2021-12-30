#encoding:utf-8
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.conf import settings
from django.db.models import Max
from principal.models import Pokemon, Poke_photo
from principal.collect import *
from principal.search import *
from principal.forms import equipo_form, recomendacion
from django.http import HttpResponseRedirect
from principal.recomendaciones import *

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
    print(recomendacion_colaborativa_basado_en_items("Pikachu"))
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
    
#muestra un formulario para crear un equipo pokemon muy competitivo
def recomendacion_colaborativa_usuarios(request):
    if request.method == 'POST':
        form = recomendacion(request.POST)
        if form.is_valid(): 
            entrada = form.cleaned_data['entrada']
            
            equipo = recomendacion_colaborativa_basado_en_usuarios(entrada)
            equipo_2_send = []
            for i in range(1, len(equipo)):
                pokemon = buscar_por_id(equipo[i])
                pokemon.foto_url = buscar_foto_pokemon_id(pokemon.id).url
                equipo_2_send.append(pokemon)
            

            return render(request, 'recomendacion_usuarios.html', {"equipo": equipo_2_send})

    else:
        form = recomendacion()

    return render(request, 'recomendacion_usuarios.html', {'form': form, "equipo": []})
     
#muestra un formulario para crear un equipo pokemon muy competitivo
def recomendacion_colaborativa_items(request):
    if request.method == 'POST':
        form = recomendacion(request.POST)
        if form.is_valid(): 
            entrada = form.cleaned_data['entrada']
            
            resultado = recomendacion_colaborativa_basado_en_items(entrada)
            pokemon = buscar_por_id(resultado)
            foto = buscar_foto_pokemon_id(pokemon.id)
            

            return render(request, 'recomendacion_items.html', {"pokemon": pokemon, "foto": foto})

    else:
        form = recomendacion()

    return render(request, 'recomendacion_items.html', {'form': form, "pokemon": []})
    