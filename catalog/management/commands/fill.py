from django.core.management import BaseCommand
from catalog.models import Category, Product
import json
from django.db import connection

class Command(BaseCommand):

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;')

        Category.objects.all().delete()
        Product.objects.all().delete()
        product_for_create = []
        category_for_create = []

        with open('categories.json', encoding="UTF-8") as f:
            data = json.load(f)
        for category in data:
            if category["model"] == "catalog.category":
                category_for_create.append(
                Category(name=category["fields"]["name"], description=category["fields"]["description"])
            )
        Category.objects.bulk_create(category_for_create)

        for product in data:
            if product["model"] == "catalog.product":
                product_for_create.append(
                Product(name=product["fields"]["name"],
                        description=product["fields"]["description"],
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"])
            )
        Product.objects.bulk_create(product_for_create)