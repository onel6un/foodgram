import csv
import os

from recipes.models import Ingredients

script_dir = os.path.dirname(__file__)
rel_path = "../data/ingredients.csv"
abs_file_path = os.path.join(script_dir, rel_path)


def run():
    with open(os.path.join(script_dir, rel_path), encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        Ingredients.objects.all().delete()

        for row in reader:
            print(row)

            ingredient = Ingredients(name=row[0], measurement_unit=row[1])
            ingredient.save()
