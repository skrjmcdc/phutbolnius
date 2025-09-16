from django.urls import path
from main.views import show_main_page, add_product

app_name = 'main'

urlpatterns = [
    path('', show_main_page),
    path('add_product/', add_product, name='add_product'),
]
