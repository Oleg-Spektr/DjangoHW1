import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Очищает БД и загружает тестовые данные из фикстур'

    def handle(self, *args, **options):
        # 1. Предварительное удаление данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # 2. Загрузка категорий
        with open('catalog/fixtures/category_data.json', 'r', encoding='utf-8') as f:
            categories_data = json.load(f)

        categories_to_create = []
        for item in categories_data:
            categories_to_create.append(
                Category(id=item['pk'], name=item['fields']['name'], description=item['fields']['description'])
            )
        Category.objects.bulk_create(categories_to_create)

        # 3. Загрузка продуктов
        with open('catalog/fixtures/product_data.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)

        products_to_create = []
        for item in products_data:
            # Находим категорию по id, чтобы выстроилась связь ForeignKey
            category = Category.objects.get(id=item['fields']['category'])
            products_to_create.append(
                Product(
                    id=item['pk'],
                    name=item['fields']['name'],
                    description=item['fields']['description'],
                    image=item['fields']['image'],
                    category=category,
                    price=item['fields']['price'],
                )
            )
        Product.objects.bulk_create(products_to_create)

        self.stdout.write(self.style.SUCCESS('База данных успешно перезаписана!'))
