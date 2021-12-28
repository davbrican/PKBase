from django import forms

class equipo_form(forms.Form):
    pokemon_favorito = forms.CharField(label='Pokemon favorito', max_length=100)
    stats_pk_1 = forms.CharField(label='Stats Pokemon 1', max_length=100)
    tipo_pk_1 = forms.CharField(label='Tipo Pokemon 1', max_length=100)
    stats_pk_2 = forms.CharField(label='Stats Pokemon 2', max_length=100)
    tipo_pk_2 = forms.CharField(label='Tipo Pokemon 1', max_length=100)