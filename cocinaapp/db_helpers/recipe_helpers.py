from cocinaapp.db_models.category import Category
from cocinaapp.db_models.ingredient import Ingredient
from cocinaapp.db_models.recipe import Recipe
from unicodedata import normalize
import cloudinary
import cloudinary.uploader
import cloudinary.api
from config import CLOUD_NAME, API_KEY, API_SECRET


def filter_query(request):
    
    recipes = list(Recipe.objects.all().order_by('name'))

    name = request.query_params.get('name', False)
    categories = request.query_params.get('categories', False)
    ingredients = request.query_params.get('ingredients', False)

    if name:
        trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
        name = normalize('NFKC', normalize('NFKD', name).translate(trans_tab))
        for recipe in recipes.copy():
            if not (name.lower() in normalize('NFKC', normalize('NFKD', recipe.name).translate(trans_tab)).lower()):
                recipes.remove(recipe)
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

def check_categories_exist(category_list):
    for category_id in category_list:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return False
    return True

def process_ingredients_and_categories(data):
    ingredients = {}
    for ingredient in Ingredient.objects.all():
        ingredients[str(ingredient.id)] = ingredient

    categories = {}
    for category in Category.objects.all():
        categories[str(category.id)] = category

    for recipe in data:
        ingredient_list = []
        for ingredient_id in recipe['ingredients']:
            try:
                ingredient_list.append({
                        "id": ingredient_id,
                        "name": ingredients[ingredient_id].name,
                    })
            except KeyError:
                pass
        recipe["ingredients"] = ingredient_list

        category_list = []
        for category_id in recipe["categories"]:
            try:
                category_list.append({
                    "id": category_id,
                    "name": categories[category_id].name,
                    "color": categories[category_id].color
                })
            except KeyError:
                pass
        recipe["categories"] = category_list
    return data


def process_ingredients_and_categories_one(data):
    ingredients = {}
    for ingredient in Ingredient.objects.all():
        ingredients[str(ingredient.id)] = ingredient

    categories = {}
    for category in Category.objects.all():
        categories[str(category.id)] = category

    ingredient_list = []
    for ingredient_id in data["ingredients"]:
        try:
            ingredient_list.append({
                    "id": ingredient_id,
                    "name": ingredients[ingredient_id].name,
                })
        except KeyError:
            pass
    data["ingredients"] = ingredient_list

    category_list = []
    for category_id in data["categories"]:
        try:
            category_list.append({
                "id": category_id,
                "name": categories[category_id].name,
                "color": categories[category_id].color
            })
        except KeyError:
            pass
    data["categories"] = category_list
    return data

def UploadImage(file, recipe_id):

    cloudinary.config(
        cloud_name = CLOUD_NAME, 
        api_key = API_KEY, 
        api_secret = API_SECRET,
        secure = True
    )

    folder = "Cocina/recipe_pictures/"

    cloudinary.uploader.upload(file,
    folder = folder,
    public_id = recipe_id,
    overwrite = True,
    notification_url = "https://mysite.example.com/notify_endpoint", 
    resource_type = "image")

    return f"https://res.cloudinary.com/{CLOUD_NAME}/{folder}{recipe_id}"

def deleteImage(url):
    cloudinary.config(
        cloud_name = CLOUD_NAME, 
        api_key = API_KEY, 
        api_secret = API_SECRET,
        secure = True
    )

    path = url.replace(f"https://res.cloudinary.com/{CLOUD_NAME}/", "")
    cloudinary.uploader.destroy(path)