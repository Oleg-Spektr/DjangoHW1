from django.urls import path
from catalog.apps import CatalogConfig
from django.contrib.auth.decorators import login_required
from catalog.views import (
    ProductListView, ProductDetailView, ContactsTemplateView,
    ProductCreateView, ProductUpdateView, ProductDeleteView
)

app_name = 'catalog'

urlpatterns = [
    # Главная страница каталога доступна всем анонимным пользователям
    path('', ProductListView.as_view(), name='home'),

    # Страница контактов также открыта для всех
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),

    # Закрываем эндпоинты декоратором login_required прямо в маршрутах
    path('products/<int:pk>/', login_required(ProductDetailView.as_view()), name='product_detail'),
    path('products/create/', login_required(ProductCreateView.as_view()), name='product_create'),
    path('products/<int:pk>/update/', login_required(ProductUpdateView.as_view()), name='product_update'),
    path('products/<int:pk>/delete/', login_required(ProductDeleteView.as_view()), name='product_delete'),
]

