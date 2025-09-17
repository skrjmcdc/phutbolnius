# Tugas 3

**Nama:** Muhammad Ibaadi Ilmi  
**NPM:** 2406357684  
**Kelas:** PBP A

**Link aplikasi:** <https://muhammad-ibaadi-phutbolnius.pbp.cs.ui.ac.id/>

## Step-by-step checklist

Saya memutuskan untuk mengerjakan checklist tanpa mengikuti urutan.

### Skeleton

Pertama, saya membuat *skeleton* sebagai kerangka *views* dalam file `templates/base.html`.

Kemudian, saya mengedit isi variabel `TEMPLATES` pada file `settings.py` untuk menambahkan directory `templates` ke daftar tempat template:

```py
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    }
]
```

Sebenarnya saya bisa saja meletakkan file `base.html` pada root proyek, namun akan membuat file saya menjadi berantakan.

Setelah menambahkan *skeleton*, saya memodifikasi file `index.html` agar menggunakan *skeleton* tersebut:

```html
{% extends 'base.html' %}
{% block content %}

<h1>Halo Dunia</h1>

<h1>Football Shop</h1>

<p><span class="bold">Nama:</span> {{ name }}</p>
<p><span class="bold">Kelas:</span> {{ class }}</p>

{% endblock content %}

```

### Form

Selanjutnya saya membuat halaman form untuk menambahkan produk ke toko.

Saya membuat template baru, yaitu `main/templates/add_product.html`:

```html
{% extends 'base.html' %}
{% block content %}

<h1>Tambah Produk</h1>

<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td>
                <input type="submit" value="Tambah Produk">
            </td>
        </tr>
</form>

{% endblock %}
```

Selanjutnya saya membuat `ModelForm` untuk model `Product` dalam file `main/forms.py`:

```py
from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "description",
            "thumbnail",
            "category",
            "is_featured",
        ]
```

Kemudian saya membuat view baru dalam file `main/views.py` untuk menampilkan form:

```py
from django.shortcuts import render, redirect
from main.forms import Product Form

...

def add_product(request):

    form = ProductForm(request.POST or None)

    # Form submission
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main_page')

    # Form filling out
    context = {'form': form}
    return render(request, "add_product.html", context)
```

Terakhir, saya melakukan routing di file `main/urls.py`:

```py
from django.urls import path
from main.views import show_main_page, add_product

app_name = 'main'

urlpatterns = [
    path('', show_main_page),
    path('add_product/', add_product, name='add_product'),
]
```

### XML dan JSON

Sekarang saya sudah memilki form untuk menambahkan produk, namun belum ada cara untuk melihat produk..

Oleh karena itu, selanjutnya saya mengimplementasi *data delivery* dalam format XML.

Pertama, saya membuat view untuk menyajikan data semua produk yang tersimpan di database dalam format XML:

```py
...
from django.http import HttpResponse
from django.core import serializers
...

...

def show_xml(request):

    products = Product.objects.all()
    xml_data = serializers.serialize("xml", products)
    return HttpResponse(xml_data, content_type="application/xml")

```

Saya juga mengimplementasi penyajian data satu produk melalui id produk tersebut:

```py
...

def show_xml_by_id(request, product_id):

    try:
        product = Product.objects.get(pk=product_id)
        xml_data = serializers.serialize("xml", [product])
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

```

Kemudian saya melakukan routing:

```py
...

urlpatterns = [
    ...
    path('json/', show_json, name='show_json'),
    path('json/<str:product_id>', show_json_by_id, name='show_json_by_id'),
]
```

Setelah memastikan semuanya berjalan lancar, saya mengimplementasi hal serupa dalam format JSON:

```py
...

def show_json(request):

    products = Product.objects.all()
    json_data = serializers.serialize("json", products)
    return HttpResponse(json_data, content_type="application/json")

def show_json_by_id(request, product_id):

    try:
        product = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
```

```py
...

urlpatterns = [
    ...
    path('xml/', show_xml, name='show_xml'),
    path('xml/<str:product_id>', show_xml_by_id, name='show_xml_by_id'),
]
```

### Detail produk

Sekarang kita punya cara mengakses data produk, namun masih belum bersifat visual.

Oleh karena itu, sekarang kita akan mengimplementasi penampilan data produk dalam web page.

Saya mengedit halaman utama agar menampilkan nama dan harga setiap produk:

```html
...

<table>
{% for product in products %}

<tr>
    <td><span class="bold">{{ product.name }}</span></td>
    <td><span class="bold">{{ product.price }}</span></td>
</tr>

{% endfor %}
</table>

...
```
```py
...

def show_main_page(request):

    products = Product.objects.all()

    context = {
        'name': 'Muhammad Ibaadi Ilmi',
        'class': 'PBP A',
        'products': products,
    }

    return render(request, "index.html", context)

...
```

## Mengapa *data delivery* diperlukan

## XML vs. JSON

## Fungsi dari method `is_valid()` pada form Django

## Mengapa `csrf_token` dibutuhkan

## Feedback asdos
