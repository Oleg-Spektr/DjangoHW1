from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from catalog.models import Product, ContactMessage
from catalog.forms import ProductForm

# Главная страница (Каталог) остается общедоступной по условию ТЗ
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


# Задание 3: Закрываем доступ к просмотру деталей для анонимов
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# Контакты остаются открытыми для всех
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


# Задание 3: Закрываем создание продуктов
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


# Задание 3: Закрываем редактирование продуктов
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


# Задание 3: Закрываем удаление продуктов
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
