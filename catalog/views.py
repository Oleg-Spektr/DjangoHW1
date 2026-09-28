from django.shortcuts import render, get_object_or_404
from catalog.models import Product, ContactMessage

def home_view(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'catalog/home.html', context)

def contacts_view(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Защита от ошибок и валидация: проверяем, что все поля заполнены
        if name and phone and message:
            # Сохраняем обращение напрямую в базу данных PostgreSQL
            ContactMessage.objects.create(
                name=name,
                phone=phone,
                message=message
            )
            context['message_sent'] = True
        else:
            context['error'] = "Пожалуйста, заполните все поля формы!"

    return render(request, 'catalog/contacts.html', context)

def product_detail(request, pk):
    # Извлекаем объект по pk или возвращаем 404, если не найден
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})