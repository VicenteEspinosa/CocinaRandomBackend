from cocinaapp.db_models.recipe import Recipe
from cocinaapp.db_models.ingredient import Ingredient


def filter_query(request):
    
    recipes = list(Recipe.objects.all().order_by('name'))
    categories = request.query_params.get('categories', False)
    ingredients = request.query_params.get('ingredients', False)

    if categories:
        categories = str(categories).split(",")
        for recipe in recipes.copy():
            if not check_repeated(recipe.categories, categories):
                recipes.remove(recipe)
    if ingredients:
        ingredients = str(ingredients).split(",")
        for recipe in recipes.copy():
            if not check_repeated(recipe.ingredients, ingredients):
                recipes.remove(recipe)
    return recipes


def check_repeated(list1, list2):

    for x in list1:
        for y in list2:
            if x == y:
                return True
    return False

def stringify_list(list_input):
    new_list = []
    for element in list_input:
        new_list.append(str(element))
    return new_list

def check_ingredients_exist(ingredient_list):
    for ingredient_id in ingredient_list:
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
        except Ingredient.DoesNotExist:
            return False
    return True