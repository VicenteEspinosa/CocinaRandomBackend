from cocinaapp.db_models.recipe import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer."""

    categories = serializers.JSONField(required=True)
    ingredients = serializers.JSONField(required=True)

    class Meta:
        """Meta."""

        model = Recipe
        fields = (
            "id",
            "name",
            "description",
            "categories",
            "ingredients",
            "image"
        )
