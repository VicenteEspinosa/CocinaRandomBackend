from cocinaapp.db_models.category import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """category serializer."""

    class Meta:
        """Meta."""

        model = Category
        fields = (
            "id",
            "name",
            "color"
        )
