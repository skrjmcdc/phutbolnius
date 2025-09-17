from django.urls import path
from main.views import \
        show_main_page, add_product, \
        show_xml, show_xml_by_id, show_json, show_json_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main_page),
    path('add_product/', add_product, name='add_product'),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<str:product_id>', show_xml_by_id, name='show_xml_by_id'),
    path('json/', show_json, name='show_json'),
    path('json/<str:product_id>', show_json_by_id, name='show_json_by_id'),
]
