from django.conf.urls import url
from django.urls import path
from cocinaapp.db_views.ingredient_view import ( 
    ingredient_list,
    ingredient_one
)


ingredient_urls = [
    url('ingredients/', ingredient_list),
    path('ingredient/<pk>/', ingredient_one),
]
