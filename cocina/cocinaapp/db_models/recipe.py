from djongo import models


class Recipe(models.Model):
    """All recipe info."""

    name = models.CharField(max_length=100)
    desciption = models.TextField()
    categories = models.JSONField()
    image =  models.URLField()
