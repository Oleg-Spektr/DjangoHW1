from django.shortcuts import render

def home_view(request):
    return render(request, 'catalog/home.html')

def contacts_view(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')  # Получение телефона
        message = request.POST.get('message')

        # Вывод в консоль
        print(f"Новое обращение!\nИмя: {name}\nТелефон: {phone}\nСообщение: {message}\n---")
        context['message_sent'] = True

    return render(request, 'catalog/contacts.html', context)
