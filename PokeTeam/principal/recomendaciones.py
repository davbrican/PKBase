from principal.models import Pokemon, Poke_photo
from principal.collect import *
from principal.search import *
import os


def get_equipos():
    equipos = []
    file = open("./Data/u.teams", "r")
    for i in file.readlines():
        equipo = i.split("|")
        equipo[6] = equipo[6].replace("\n", "")
        equipos.append(equipo)
    file.close()

    recomendacion = {}

    for j in range(1, 802):
        if j < 10:
            recomendacion["#00"+str(j)] = 0
        elif j < 100:
            recomendacion["#0"+str(j)] = 0
        else:
            recomendacion["#"+str(j)] = 0

    return [equipos, recomendacion]
    

def recomendacion_colaborativa_basado_en_items(pokemon):
    equipos, recomendacion = get_equipos()[0], get_equipos()[1]
    for i in equipos:
        if i[1] == pokemon or i[2] == pokemon or i[3] == pokemon or i[4] == pokemon or i[5] == pokemon or i[6] == pokemon:
            recomendacion[i[1]] += 1
            recomendacion[i[2]] += 1
            recomendacion[i[3]] += 1
            recomendacion[i[4]] += 1
            recomendacion[i[5]] += 1
            recomendacion[i[6]] += 1
            
    new_dict = {k: v for k, v in sorted(recomendacion.items(), key=lambda item: item[1])}

    return list(new_dict.keys())[-2]

def get_tipos_equipo(equipo):
    set_tipos_i = []
    for j in range(1,len(equipo)):
        set_tipos_i.append(buscar_por_id(equipo[j]).tipos.split(",")[0])
        set_tipos_i.append(buscar_por_id(equipo[j]).tipos.split(",")[1])
    return list(set(set_tipos_i))
        
def recomendacion_colaborativa_basado_en_usuarios(usuario_id):
    equipos = get_equipos()[0]
    
    for i in equipos:
        if i[0] == usuario_id:
            usuario = i
            break
        else:
            usuario = None
            
    ponderacion_usuarios = {}
    set_tipos_usuario = get_tipos_equipo(usuario[1:])
    for i in equipos:
        user_points = 0
        if usuario[0] != i[0]:
            if usuario[1] in i:
                user_points += 1
            if usuario[2] in i:
                user_points += 1
            if usuario[3] in i:
                user_points += 1
            if usuario[4] in i:
                user_points += 1
            if usuario[5] in i:
                user_points += 1
            if usuario[6] in i:
                user_points += 1
                
                ponderacion_usuarios[i[0]] = user_points
                
            
    
    new_dict = {k: v for k, v in sorted(ponderacion_usuarios.items(), key=lambda item: item[1])}
    
    for key in list(new_dict.keys())[-3:]:
        if new_dict[key] > 0:
            for i in equipos:
                if i[0] == key:
                    usuario2 = i
                    break
                else:
                    usuario2 = None
                    
            set_tipos_i = get_tipos_equipo(usuario2[1:])
            for j in set_tipos_usuario:
                if j in set_tipos_i:
                    new_dict[key] += 1
                    
                    
    new_dict2 = {k: v for k, v in sorted(new_dict.items(), key=lambda item: item[1])}
    
    for i in equipos:   
        if i[0] == list(new_dict2.keys())[-1]:
            return i
    return None
