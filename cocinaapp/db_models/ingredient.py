from djongo import models


class Ingredient(models.Model):
    """All igredient info."""

    name = models.CharField(max_length=100)
