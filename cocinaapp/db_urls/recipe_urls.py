from django.conf.urls import url
from django.urls import path
from cocinaapp.db_views.recipe_view import ( 
    recipe_list,
    recipe_one,
    random_recipe
)


recipe_urls = [
    url('recipes/', recipe_list),
    path('recipe/<pk>/', recipe_one),
    url('recipe_random/', random_recipe)
]
