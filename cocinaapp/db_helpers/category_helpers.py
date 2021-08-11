from cocinaapp.db_models.category import Category

def check_repeated_category(name):
    try:
        Category.objects.get(name__iexact=name)
        return False
    except Category.DoesNotExist:
        return True