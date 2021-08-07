from cocinaapp.db_urls.recipe_urls import recipe_urls

from django.contrib import admin
from django.urls import include, path

# Every url must end with a slash ( / )
urlpatterns = []

urlpatterns += recipe_urls

