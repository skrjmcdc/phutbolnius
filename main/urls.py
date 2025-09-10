from django.urls import path
from main.views import show_main_page

urlpatterns = [
    path('', show_main_page)
]
