from rest_framework import status
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination # Any other type works as well
from rest_framework.response import Response
from cocinaapp.db_models.recipe import Recipe
import math
from cocinaapp.db_helpers.recipe_helpers import (
    process_ingredients_and_categories
)
from cocinaapp.db_helpers.json_helpers import get_indexed_json

class RecipePaginator(PageNumberPagination):

    def __init__(self, page_size) -> None:
        super().__init__()
        self.page_size = page_size # Number of objects to return in one page
        self.last_page = 0 # The last page that you can access


    def generate_response(self, query_set, serializer_obj, request, length):
        recipe_count = length
        self.last_page = math.ceil(recipe_count / int(self.page_size))

        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({'length_error': int(self.last_page)}, status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)


        data = serialized_page.data # add the get_indexed_json here
        data = process_ingredients_and_categories(data)
        data = get_indexed_json(data)
        return self.get_paginated_response(data)


    def get_paginated_response(self, data):
        return Response({

            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': int(self.page_size),
            'last_page': self.last_page,
            'data': data
        })
