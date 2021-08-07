from cocinaapp.db_models.recipe import Recipe


def filter_query(request):
    
    recipes = list(Recipe.objects.all())
    categories = request.query_params.get('categories', False)
    ingredients = request.query_params.get('ingredients', False)

    if categories:
        for recipe in recipes.copy():
            if not check_repeated(recipe.categories, categories):
                recipes.remove(recipe)
    if ingredients:
        for recipe in recipes.copy():
            if not check_repeated(recipe.ingedientes, ingredients):
                recipes.remove(recipe)
    return recipes


def check_repeated(list1, param):
  
    list2 = param.split(",")

    for x in list1:
        for y in list2:
            if x == y:
                return True
    return False