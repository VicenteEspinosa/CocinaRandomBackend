from cocinaapp.db_models.ingredient import Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    """ingredient serializer."""

    class Meta:
        """Meta."""

        model = Ingredient
        fields = (
            "id",
            "name"
        )
