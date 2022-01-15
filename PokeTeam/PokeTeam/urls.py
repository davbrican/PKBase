
from django.contrib import admin
from django.urls import path
from principal import views

urlpatterns = [  
    path('', views.inicio),
    path('cargar/', views.cargar),
    path('pokemons/', views.lista_pokemons),
    path('pokemons/<str:tipo>', views.lista_pokemons_tipo),
    path('pokemons/pokemon/<str:pokemon_id>', views.detalle_pokemon),
    path('admin/', admin.site.urls),
    path('equipo/', views.equipo),
    path('recomendacion_usuarios/', views.recomendacion_colaborativa_usuarios),
    path('recomendacion_items/', views.recomendacion_colaborativa_items),
    path('administration/', views.administration),
]
