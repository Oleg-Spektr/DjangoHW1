from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render
from catalog.models import Product, ContactMessage

# Переводим home_view на ListView
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

# Переводим product_detail на DetailView
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# Переводим contacts_view на базовый TemplateView с обработкой POST
class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and phone and message:
            ContactMessage.objects.create(
                name=name,
                phone=phone,
                message=message
            )
            context['message_sent'] = True
        else:
            context['error'] = "Пожалуйста, заполните все поля формы!"

        return render(request, self.template_name, context)
