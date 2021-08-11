from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from cocinaapp.db_models.ingredient import Ingredient
from cocinaapp.db_serializers.ingredient_serializer import IngredientSerializer
from cocinaapp.db_helpers.json_helpers import get_indexed_json
from cocinaapp.db_helpers.ingredient_helpers import check_repeated_ingredient


@api_view(['GET', 'POST'])
def ingredient_list(request):
    """Returns all the ingredients."""
    # ingredients/

    if request.method == 'GET':
        ingredients = Ingredient.objects.all().order_by('name')
        ingredients_serializer = IngredientSerializer(ingredients, many=True)
        return JsonResponse(get_indexed_json(ingredients_serializer.data), safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        ingredient_data = JSONParser().parse(request)
        try:
            ingredient_data["name"]
        except KeyError:
            return JsonResponse({"error": "missing field name"}, status=status.HTTP_400_BAD_REQUEST)
        ingredient_data["name"] = ingredient_data["name"].capitalize()
        if check_repeated_ingredient(ingredient_data["name"]):
            ingredient_serializer = IngredientSerializer(data=ingredient_data)
            if ingredient_serializer.is_valid():
                ingredient = ingredient_serializer.save()
                ingredient.save()
                return JsonResponse(ingredient_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(ingredient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error": "repeated ingredient"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def ingredient_one(request, pk):
    """Work with one ingredient."""
    # ingredient/<pk>/

    try:
        ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        return JsonResponse({"error": "The ingredient does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        ingredient_serializer = IngredientSerializer(ingredient)
        return JsonResponse(ingredient_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        ingredient_data = JSONParser().parse(request)
        ingredient_serializer = IngredientSerializer(ingredient, data=ingredient_data)
        if ingredient_serializer.is_valid():
            ingredient = ingredient_serializer.save()
            ingredient.save()
            return JsonResponse(ingredient_serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(ingredient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pass
        