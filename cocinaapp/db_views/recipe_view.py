from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from cocinaapp.db_models.recipe import Recipe
from cocinaapp.db_serializers.recipe_serializer import RecipeSerializer


@api_view(['POST'])
def recipe_list(request):
    """Save a new answer."""

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        recipe_data = JSONParser().parse(request)
        recipe_serializer = RecipeSerializer(data=recipe_data)
        if recipe_serializer.is_valid():
            recipe = recipe_serializer.save()
            recipe.save()
            return JsonResponse(recipe_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)