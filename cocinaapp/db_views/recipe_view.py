from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from cocinaapp.db_models.recipe import Recipe
from cocinaapp.db_serializers.recipe_serializer import RecipeSerializer
from cocinaapp.db_paginators.recipe_paginator import RecipePaginator
from cocinaapp.db_helpers.json_helpers import get_indexed_json
from cocinaapp.db_helpers.recipe_helpers import (
    filter_query,
    stringify_list,
    check_categories_exist,
    check_ingredients_exist,
    process_ingredients_and_categories
)
import random
from django.db.models import Q


@api_view(['GET', 'PATCH', 'DELETE'])
def recipe_one(request, pk):
    """Work with one recipe."""
    # recipe/<pk>/

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
    # recipes/

    if request.method == 'GET':
        recipes = Recipe.objects.all().order_by('name')
        recipe_serializer = RecipeSerializer(recipes, many=True)
        data = recipe_serializer.data
        data = process_ingredients_and_categories(data)
        return JsonResponse(get_indexed_json(data), safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        recipe_data = JSONParser().parse(request)
        recipe_serializer = RecipeSerializer(data=recipe_data)
        if recipe_serializer.is_valid():
            if check_ingredients_exist(recipe_data["ingredients"]):
                if check_categories_exist(recipe_data["categories"]):
                    recipe = recipe_serializer.save()
                    recipe.categories = stringify_list(recipe.categories)
                    recipe.ingredients = stringify_list(recipe.ingredients)
                    recipe.save()
                    return JsonResponse(recipe_serializer.data, safe=False, status=status.HTTP_201_CREATED)
                return JsonResponse({'error': 'Some categories do not exist'}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({'error': 'Some ingredients do not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def random_recipe(request):
    """Pick random recipe."""
    # recipe_random/

    last_recipe = request.query_params.get('last', False)
    recipes = list(Recipe.objects.filter(~Q(id=last_recipe)))
    random_recipe = random.choice(recipes)
    recipe_serializer = RecipeSerializer(random_recipe)
    data = recipe_serializer.data
    data = process_ingredients_and_categories(data)
    return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def random_filter(request):
    """Pick random recipe/s with filters."""
    # recipe_filter_random/

    recipes = Recipe.objects.all().order_by('name')
    length = len(recipes)
    page_size = request.query_params.get('page_size', False)
    if page_size:
        recipe_paginator = RecipePaginator(page_size)
        response = recipe_paginator.generate_response(recipes, RecipeSerializer, request, length)
        return response
    return JsonResponse({'error': 'The page_size must be in the path values.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def paginated_recipes(request):
    """Pick random recipe/s with filters."""
    # recipes_paginated/

    recipes = filter_query(request)
    length = len(recipes)
    page_size = request.query_params.get('page_size', False)
    if page_size:
        recipe_paginator = RecipePaginator(page_size)
        response = recipe_paginator.generate_response(recipes, RecipeSerializer, request, length)
        return response
    return JsonResponse({'error': 'The page_size must be in the path values.'}, status=status.HTTP_400_BAD_REQUEST)

