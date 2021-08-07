from django.conf.urls import url
from django.urls import path
from cocinaapp.db_views.recipe_view import ( 
    recipe_list
)


recipe_urls = [
    url('recipe/', recipe_list)
]
