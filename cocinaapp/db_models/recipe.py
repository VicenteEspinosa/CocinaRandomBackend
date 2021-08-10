from djongo import models


class Recipe(models.Model):
    """All recipe info."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.JSONField() # Lista de strings
    image =  models.URLField()
    ingredient = models.IntegerField()
