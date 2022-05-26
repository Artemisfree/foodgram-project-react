import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        ingredients_file = open(
            'recipes/management/commands/data/ingredients.json',
            encoding='utf-8'
        )
        ingredients_str = ingredients_file.read()
        ingredients_data = json.loads(ingredients_str)
        for ingredient in ingredients_data:
            name = ingredient['name']
            measurement_unit = ingredient['measurement_unit']
            Ingredient.objects.create(
                name=name,
                measurement_unit=measurement_unit,
            )

    # def handle(self, *args, **options):
    #     with open('data/ingredients.json', 'rb') as f:
    #         data = json.load(f)
    #         for i in data:
    #             ingredient = Ingredient()
    #             ingredient.name = i['name']
    #             ingredient.measurement_unit = i['measurement_unit']
    #             ingredient.save()
    #             print(i['name'], i['measurement_unit'])
