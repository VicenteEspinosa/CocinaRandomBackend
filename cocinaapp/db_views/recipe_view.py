from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from cocinaapp.db_models.recipe import Recipe
from cocinaapp.db_serializers.recipe_serializer import RecipeSerializer
from cocinaapp.db_helpers.json_helpers import get_indexed_json
import random


@api_view(['GET', 'PATCH', 'DELETE'])
def recipe_one(request, pk):
    """Work with one recipe."""

    try:
        recipe = Recipe.objects.get(pk=pk)

        if request.method == 'GET':
            recipe_serializer = RecipeSerializer(recipe)
            return JsonResponse(recipe_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            recipe_data = JSONParser().parse(request)
            recipe_serializer = RecipeSerializer(recipe, partial= True, data=recipe_data)
            if recipe_serializer.is_valid(raise_exception=True):
                data = recipe_serializer.save()
                data.save()
            return JsonResponse(recipe_serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            recipe.delete()
            return JsonResponse({'message': 'Recipe was deleted successfully!'}, status=status.HTTP_200_OK)

    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'The recipe do not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def recipe_list(request):
    """Show all recipes or post new."""

    if request.method == 'GET':
        recipes = Recipe.objects.all()
        recipe_serializer = RecipeSerializer(recipes, many=True)
        return JsonResponse(get_indexed_json(recipe_serializer.data), safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        recipe_data = JSONParser().parse(request)
        recipe_serializer = RecipeSerializer(data=recipe_data)
        if recipe_serializer.is_valid():
            recipe = recipe_serializer.save()
            recipe.save()
            return JsonResponse(recipe_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def random_recipe(request):
    """Pick random recipe."""

    recipes = list(Recipe.objects.all())
    random_recipe = random.choice(recipes)
    recipe_serializer = RecipeSerializer(random_recipe)
    return JsonResponse(recipe_serializer.data, status=status.HTTP_200_OK)
