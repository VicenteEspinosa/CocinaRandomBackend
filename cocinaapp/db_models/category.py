from djongo import models


class Category(models.Model):
    """All category info."""

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
