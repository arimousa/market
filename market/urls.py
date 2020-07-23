from market import views
from django.urls import path

urlpatterns = [
    path('', views.product, name='product'),
    path('delete/<product_code>', views.delete_product, name='delete_product'),
    path('edit/<product_code>', views.edit_product, name='edit_product'),
]
