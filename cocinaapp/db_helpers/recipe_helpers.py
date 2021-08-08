from cocinaapp.db_models.recipe import Recipe


def filter_query(request):
    
    recipes = list(Recipe.objects.all())
    categories = request.query_params.get('categories', False)
    ingredients = request.query_params.get('ingredients', False)

    if categories:
        categories = str(categories).split(",")
        print(categories)
        print("---")
        for recipe in recipes.copy():
            if not check_repeated(recipe.categories, categories):
                recipes.remove(recipe)
            print("---")
    if ingredients:
        ingredients = str(ingredients).split(",")
        for recipe in recipes.copy():
            if not check_repeated(recipe.ingedientes, ingredients):
                recipes.remove(recipe)
    return recipes


def check_repeated(list1, list2):

    for x in list1:
        print(x)
        for y in list2:
            if x == y:
                print("True")
                return True
    return False

def stringify_list(list_input):
    new_list = []
    for element in list_input:
        new_list.append(str(element))
    return new_list