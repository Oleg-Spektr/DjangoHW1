from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from catalog.models import Product, ContactMessage
from catalog.forms import ProductForm


# 1. Главная страница каталога (Доступна всем без авторизации - Критерий 9)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


# 2. Детальный просмотр товара (Защищен от анонимов - Критерий 8)
@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# 3. Страница контактов с обработкой формы (Доступна всем)
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


# 4. Создание нового продукта (Защищено от анонимов - Критерий 8)
@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


# 5. Редактирование продукта (Защищено от анонимов - Критерий 8)
@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


# 6. Удаление продукта (Защищено от анонимов - Критерий 8)
@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
