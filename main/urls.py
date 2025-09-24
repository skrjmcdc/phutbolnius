from django.urls import path
from main.views import show_main_page
from main.views import view_product, add_product, edit_product
from main.views import show_xml, show_xml_by_id, show_json, show_json_by_id
from main.views import register, login_user, logout_user

app_name = 'main'

urlpatterns = [
    path('', show_main_page, name="show_main_page"),
    path('product/<str:id>/', view_product, name="view_product"),
    path('add_product/', add_product, name='add_product'),
    path('product/<str:id>/edit/', edit_product, name="edit_product"),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<str:product_id>', show_xml_by_id, name='show_xml_by_id'),
    path('json/', show_json, name='show_json'),
    path('json/<str:product_id>', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
