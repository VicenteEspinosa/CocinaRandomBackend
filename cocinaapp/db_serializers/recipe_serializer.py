from cocinaapp.db_models.recipe import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer."""

    categories = serializers.JSONField(required=True)

    class Meta:
        """Meta."""

        model = Recipe
        fields = (
            "id",
            "name",
            "description",
            "categories",
            "image"
        )

# class BlockPutSerializer(serializers.ModelSerializer):
#     """Block serializer without for_form and category."""

#     questions = serializers.JSONField(required=False)

#     class Meta:
#         """Meta."""

#         model = Block
#         fields = (
#             "id",
#             "name",
#             "status",
#             "questions"
#         )