from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home_view, contacts_view, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_view, name='home'),
    path('contacts/', contacts_view, name='contacts'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
]