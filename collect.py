import urllib.request as urllib2
from bs4 import BeautifulSoup
import sqlite3
from models import *


def leer_pagina():
    link = "https://www.pkparaiso.com/pokemon/lista-pokemon.php"
    
    response = urllib2.urlopen(link)
    soup = BeautifulSoup(response, 'lxml')
    
    pokemons = soup.find("table", ["dex","sortable"])
    print(pokemons.find_all("tr")[1].find_all("td"))


leer_pagina()

'''
<td class="row1">001</td>
<td class="row1"><span><a href="/pokedex/bulbasaur.php"><img alt="-" height="32" src="http://www.pkparaiso.com/imagenes/pokedex/sm-icons/001.png" style="border:0px; display: inline; vertical-align: middle; margin-top: -6px;" width="32"/></a></span></td>
<td class="row1" style="text-align: left;"><a href="/pokedex/bulbasaur.php" style="padding-left: 16px;">#001 Bulbasaur</a></td>
<td class="row1"><span><img src="http://www.pkparaiso.com/imagenes/xy/sprites/tipos/planta.gif" style="display: inline; vertical-align: middle;"/>
<img src="http://www.pkparaiso.com/imagenes/xy/sprites/tipos/veneno.gif" style="display: inline; vertical-align: middle;"/></span></td>
<td class="row1">45</td>
<td class="row1">49</td>
<td class="row1">49</td>
<td class="row1">45</td>
<td class="row1">65</td>
<td class="row1">65</td>
<td class="row1">318</td>
</tr>
'''