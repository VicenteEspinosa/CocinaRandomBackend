from django.conf.urls import url
from django.urls import path
from cocinaapp.db_views.category_view import ( 
    category_list,
    category_one
)


category_urls = [
    url('categories/', category_list),
    path('category/<pk>/', category_one),
]
