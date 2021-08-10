from cocinaapp.db_models.ingredient import Ingredient

def check_repeated_ingredient(name):
    try:
        Ingredient.objects.get(name__iexact=name)
        return False
    except Ingredient.DoesNotExist:
        return True