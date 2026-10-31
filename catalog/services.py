from django.core.cache import cache
from django.conf import settings
from catalog.models import Product

def get_products_by_category(category_id):
    """
    Сервисная функция.
    Возвращает список продуктов указанной категории.
    Критерий: Использует низкоуровневое кеширование с ключом category_{id}.
    """
    # Если кеширование отключено в настройках, берем данные напрямую из БД
    if not settings.CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True)

    # Формируем ключ согласно критериям ТЗ
    key = f'category_{category_id}'

    # Пробуем получить данные из Redis
    products_list = cache.get(key)

    # Если данных в Redis нет — берем из БД и записываем в кеш на 60 секунд
    if products_list is None:
        products_list = list(Product.objects.filter(category_id=category_id, is_published=True))
        cache.set(key, products_list, timeout=60)  # TTL = 60 секунд

    return products_list
