from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from cocinaapp.db_models.category import Category
from cocinaapp.db_serializers.category_serializer import CategorySerializer
from cocinaapp.db_helpers.json_helpers import get_indexed_json
from cocinaapp.db_helpers.category_helpers import check_repeated_category


@api_view(['GET', 'POST'])
def category_list(request):
    """Returns all the categories."""
    # categories/

    if request.method == 'GET':
        categories = Category.objects.all().order_by('name')
        categories_serializer = CategorySerializer(categories, many=True)
        return JsonResponse(get_indexed_json(categories_serializer.data), safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            if check_repeated_category(category_data["name"]):
                category = category_serializer.save()
                category.name = category.name.capitalize()
                category.save()
                return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({"error": "repeated category"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def category_one(request, pk):
    """Work with one category."""
    # category/<pk>/

    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return JsonResponse({"error": "The category does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        category_serializer = CategorySerializer(category)
        return JsonResponse(category_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(category, data=category_data)
        if category_serializer.is_valid():
            category = category_serializer.save()
            category.name = category.name.capitalize()
            category.save()
            return JsonResponse(category_serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pass
