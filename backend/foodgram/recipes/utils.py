from django.http import HttpResponse

from .models import ShoppingCart


def get_shopping_list(user):
    shopping_cart = ShoppingCart.objects.filter(user=user).all()
    shopping_list = {}
    for item in shopping_cart:
        for recipe_ingredient in item.recipe.recipe_ingredients.all():
            name = recipe_ingredient.ingredient.name
            measurement = recipe_ingredient.ingredient.measurement
            amount = recipe_ingredient.amount
            if name not in shopping_list:
                shopping_list[name] = {
                    'name': name,
                    'measurement': measurement,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
    content = (
        [
            f'{item["name"]} ({item["measurement"]}) '
            f'- {item["amount"]}\n'
            for item in shopping_list.values()
        ]
    )
    filename = 'shopping_list.txt'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename={0}'.format(filename)
    )
    return response
