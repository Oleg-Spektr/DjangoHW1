from django.shortcuts import render

def home_view(request):
    # Рендер шаблона главной страницы
    return render(request, 'catalog/home.html')

def contacts_view(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        # Вывод данных в консоль
        print(f"Получено сообщение от {name}: {message}")
        context['message_sent'] = True

    return render(request, 'catalog/contacts.html', context)
