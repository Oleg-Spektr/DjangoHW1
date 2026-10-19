from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):
    # Список запрещенных слов вынесен в константу класса (Критерий оценки)
    FORBIDDEN_WORDS = [
        'казино', 'биржа', 'обман', 'криптовалюта',
        'дешево', 'бесплатно', 'полиция', 'радар', 'крипта'
    ]

    class Meta:
        model = Product
        # Указываем поля, которые пользователь сможет заполнять в форме
        fields = ('name', 'description', 'image', 'category', 'price')

    def __init__(self, *args, **kwargs):
        """Кастомный метод инициализации для стилизации под Bootstrap (Задание 3)"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Проверяем тип поля, чтобы не ломать стили чекбоксов (Критерий оценки)
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        """Валидация поля name (Задание 1)"""
        cleaned_data = self.cleaned_data['name']

        # Проверка отсутствия запрещенных слов в любом регистре (Критерий оценки)
        for word in self.FORBIDDEN_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f"Название продукта содержит запрещенное слово: '{word}'")
        return cleaned_data

    def clean_description(self):
        """Валидация поля description (Задание 1)"""
        cleaned_data = self.cleaned_data['description']

        # Проверка отсутствия запрещенных слов в описании
        if cleaned_data:
            for word in self.FORBIDDEN_WORDS:
                if word in cleaned_data.lower():
                    raise forms.ValidationError(f"Описание продукта содержит запрещенное слово: '{word}'")
        return cleaned_data

    def clean_price(self):
        """Кастомная валидация для поля price через метод clean_price (Задание 2)"""
        price = self.cleaned_data['price']

        # Проверка, что цена продукта не может быть отрицательной (Критерий оценки)
        if price < 0:
            raise forms.ValidationError("Цена продукта не может быть отрицательной!")
        return price
