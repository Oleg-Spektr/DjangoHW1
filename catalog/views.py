from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from catalog.models import Product, ContactMessage
from catalog.forms import ProductForm

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

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm  # Привязываем нашу валидную форму
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm  # Привязываем форму для редактирования
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        # Перенаправляем на детальный просмотр обновленного товара
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')