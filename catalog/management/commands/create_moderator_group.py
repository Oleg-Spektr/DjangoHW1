from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу Модератор продуктов и назначает права доступа'

    def handle(self, *args, **options):
        # 1. Создаем или находим группу (Критерий)
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # 2. Находим наши кастомные права доступа
        content_type = ContentType.objects.get_for_model(Product)

        # Наше кастомное право на отмену публикации
        can_unpublish = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
        # Встроенное право Django на удаление любого продукта
        can_delete = Permission.objects.get(codename='delete_product', content_type=content_type)

        # 3. Назначаем оба указанных права группе (Критерий)
        moderator_group.permissions.add(can_unpublish, can_delete)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана с правами!'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует.'))
