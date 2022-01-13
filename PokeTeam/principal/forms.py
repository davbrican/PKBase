from email.policy import default
from django import forms

class equipo_form(forms.Form):
    pokemon_favorito = forms.CharField(label='Pokemon favorito', max_length=100)
    stats_pk_1 = forms.CharField(label='Stats Pokemon 1', max_length=100)
    tipo_pk_1 = forms.CharField(label='Tipo Pokemon 1', max_length=100)
    stats_pk_2 = forms.CharField(label='Stats Pokemon 2', max_length=100)
    tipo_pk_2 = forms.CharField(label='Tipo Pokemon 1', max_length=100)

class recomendacion(forms.Form):
    entrada = forms.CharField(label='Entrada', max_length=100)
    
class busqueda_estandard(forms.Form):
    palabra = forms.CharField(label="Palabra", max_length=100)
    
class filtrado(forms.Form):
    tipo_pkm = forms.CharField(label="Tipo", max_length=100)