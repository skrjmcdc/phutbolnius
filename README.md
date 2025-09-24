**Nama:** Muhammad Ibaadi Ilmi  
**NPM:** 2406357684  
**Kelas:** PBP A

**Link aplikasi:** <https://muhammad-ibaadi-phutbolnius.pbp.cs.ui.ac.id/>

# Tugas 4

## Step-by-step checklist

### Registrasi, login, dan logout

Pertama saya membuat view baru untuk registrasi user.

(File: `main/templates/register.html` **(file baru)**)
```html
{% extends 'base.html' %}

{% block meta %}
<title>Register</title>
{% endblock meta %}

{% block content %}

<h1>Register</h1>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" name="submit" value="Daftar" />
</form>

{% endblock content %}
```
(File: `main/views.py`)
```py
...
from django.contrib.auth.forms import UserCreationForm
...
```
```
...

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_main_page')

    context = { 'form': form }
    return render(request, 'register.html', context)
```

Selanjutnya saya membuat view untuk login.

(File: `main/templates/login.html` **(file baru)**)
```html
{% extends 'base.html' %}

{% block meta %}
<title>Login</title>
{% endblock meta %}

{% block content %}
<div class="login">
    <h1>Login</h1>

    <form method="POST" action="">
        {% csrf_token %}
        <table>
            {{ form.as_table }}
            <tr>
                <td></td>
                <td><input class="btn login_btn" type="submit" value="Login" /></td>
            </tr>
        </table>
    </form>

    Belum punya akun? <a href="{% url 'main:register' %}">Daftar Akun</a>
</div>

{% endblock content %}
```
(File: `main/views.py`)
```py
...
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
...
```
```
...

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse("main:show_main_page"))
    else:
        form = AuthenticationForm(request)
    context = { 'form': form }
    return render(request, 'login.html', context)
```

Terakhir, saya membuat mekanisme logout.
(File: `main/views.py`)
```py
...

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:show_main_page'))
```

Saya juga tidak lupa melakukan routing untuk semua views telah yang saya buat.
(File: `main/urls.py`)
```py
from django.urls import path
from main.views import \
        show_main_page, view_product, add_product, \
        show_xml, show_xml_by_id, show_json, show_json_by_id, \
        register, login_user, logout_user

app_name = 'main'

urlpatterns = [
    ...
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
```

### Penghubungan model Product dengan User

Selanjutnya saya menghubungkan model Product dengan User.

Saya menambahkan atribut `user` dalam model Product.

(File: `main/models.py`)
```py
...
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    ...
    
```

Perubahan model tersebut mengharuskan saya melakukan migrasi database:

(bash)
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Kemudian saya menambahkan informasi pembuat produk ke dalam model produk saat pengguna men-submit form pembuatan produk.

(File: `main/views.py`)
```py
...

def add_product(request):

    form = ProductForm(request.POST or None)

    # Form submission
    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return redirect('main:show_main_page')

    # Form filling out
    context = {'form': form}
    return render(request, "add_product.html", context)

...
```

Terakhir, saya membuat halaman pembuatan produk hanya bisa diakses apabila pengguna telah melakukan login.

(File: `main/views.py`)
```py
...
from django.contrib.auth.decorators import login_required
...

...

@login_required(login_url='/login')
def add_product(request):
    ...

...
```

Saya juga memodifikasi halaman detail produk agar juga menampilkan nama penjual produk.

### Penggunaan cookies

Kemudian saya meng-implementasi cookie `last_login`.

Saya memodifikasi view login agar menyimpan waktu login dalam cookie `last_login` saat pengguna men-submit form login.
(File: `main/views.py`)
```py
import datetime
...

```
```py
...

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main_page"))
            response.set_cookie('last_login', 
                                datetime.datetime.now()
                                .strftime("%A, %d %B %Y, %H:%M:%S.%f"))
            return response
    else:
        form = AuthenticationForm(request)
    context = { 'form': form }
    return render(request, 'login.html', context)

...
```
```py
...

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main_page'))
    response.delete_cookie('last_login')
    return response
```

Kemudian saya menggunakan cookie tersebut di halaman utama.

(File: `main/views.py`)
```py
...

def show_main_page(request):

    products = Product.objects.all()

    context = {
        'name': 'Muhammad Ibaadi Ilmi',
        'class': 'PBP A',
        'products': products,
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated,
        'last_login': request.COOKIES.get('last_login', 'Belum Pernah'),
    }

    return render(request, "index.html", context)

...
```

(File: `main/templates/index.html`)
```html
...

{% if username %}
<br/>

<p>Halo, {{ username }}</p>
<p>Waktu login: {{ last_login }}</p>

{% endif %}

...
```

## `AuthenticationForm` di Django

`AuthenticationForm` adalah template form login bawaan Django.

Kelebihan `AuthenticationForm` adalah mudah untuk digunakan; cukup dengan memanggil `AuthenticationForm` dengan data request yang diterima server. `AuthenticationForm` juga meng-handle login invalid secara otomatis, sehingga pengembang tidak perlu repot-repot membuat display message untuk login invalid.

Kelemahannya yaitu kurang feksibel dan agak minimalis. Sebagai contoh, form yang dihasilkan tidak mencantumkan petunjuk bagi pengguna yang belum memiliki akun.

## Autentikasi vs. otorisasi

Autentikasi adalah proses memastikan identitas pengguna (siapakah pengguna itu), sedangkan otorisasi adalah proses memastikan kewenangan pengguna (apa saja yang bisa diakses oleh pengguna itu.)

Dalam Django, autentikasi ditangani oleh model User yang menyimpan username serta password pengguna. Sedangkan otorisasi ditangani dengan atribut flag dalam User, dan bisa juga dilakukan secara manual oleh aplikasi.

## Kelebihan dan kekurangan session dan cookies

Kelebihan server-side session dibandingkan cookies adalah relatif lebih aman, karena data hanya disimpan di server dan tidak terlihat oleh pengguna. Selain itu, ukuran maksimum session sangat tinggi; hanya bergantung pada kapasitas server.

Kekurangannya adalah dari segi performa, karena server harus menangani session untuk banyak user sekaligus. Selain itu, data session akan hilang jika server dimatikan.

Kelebihan cookies dibandingkan session adalah performa yang lebih tinggi, karena data hanya disimpan di device pengguna. Selain itu, data bisa tetap ada walaupun server atau device pengguna dimatikan.

Kekurangannya adalah relatif kurang aman, karena data disimpan di browser pengguna sehingga pengguna bebas membacanya dan memodifikasinya. Selain itu, ukuran maksimum suatu cookie terbatas dan jauh lebih kecil dari ukuran maksimum session.

## Resiko penggunaan cookies

Salah satu resiko potensial dari penggunaan cookies yaitu pencurian dan/atau pemalsuan cookie, yang memungkinkan penyerang untuk berpura-pura menjadi seorang pengguna yang sah. Untuk memitigasi resiko tersebut,

# Tugas 3

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

Sekarang saya sudah memilki form untuk menambahkan produk, namun belum ada cara untuk melihat produk.

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
    path('xml/', show_xml, name='show_xml'),
    path('xml/<str:product_id>', show_xml_by_id, name='show_xml_by_id'),
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
    path('json/', show_json, name='show_json'),
    path('json/<str:product_id>', show_json_by_id, name='show_json_by_id'),
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

Selanjutnya saya mengimplementasi halaman untuk melihat detail masing-masing produk. Untuk itu saya membuat template baru di `main/templates/view_product.html`:
```html
{% extends 'base.html' %}
{% block content %}

<p><a href="{% url 'main:show_main_page' %}">Kembali ke halaman utama</a></p>

<h1>{{ product.name }}</h1>

<p><span class="bold">Kategori: </span>{{ product.category }}</p>

<p><span class="bold">Harga: </span>{{ product.price }}</p>

<p>{{ product.description }}</p>

{% endblock content %}
```
Implementasi view:
```py
from django.shortcuts import render, redirect, get_object_or_404
...

...

def view_product(request, id):

    product = get_object_or_404(Product, pk=id)
    
    context = {
        'product': product,
    }

    return render(request, "view_product.html", context)

...
```
Routing:
```py
from django.urls import path
from main.views import \
        show_main_page, view_product, add_product, \
        show_xml, show_xml_by_id, show_json, show_json_by_id

app_name = 'main'

urlpatterns = [
    ...
    path('product/<str:id>/', view_product, name="view_product"),
    ...
]
```
Terakhir, saya juga sedikit memodifikasi halaman utama agar nama setiap produk menjadi link menuju halaman detail produk tersebut:
```html
...

{% for product in products %}

<tr>
    <td><a href="{% url 'main:view_product' product.id %}">
            <span class="bold">{{ product.name }}</span>
        </a></td>
    <td><span class="bold">{{ product.price }}</span></td>
</tr>

{% endfor %}

...
```
## Mengapa *data delivery* diperlukan dalam pengimplementasian sebuah platform

Secara konseptual Internet dan World Wide Web berfungsi sebagai jaringan transfer data raksasa, jadi *data delivery* sudah pasti penting.

## XML vs. JSON

Secara pribadi saya lebih menyukai XML karena syntax-nya lebih kaku, dan lebih aman dibandingkan JSON.

Menurut saya alasan JSON lebih popular adalah karena JSON meniru syntax JavaScript (sesuai namanya), yang mana JavaScript adalah salah satu programming language paling popular dalam pengembangan web.

## Fungsi dari method `is_valid()` pada form Django

Sesuai namanya, method `is_valid()` akan memvalidasi input form yang diterima oleh server. Fungsi ini penting karena bisa saja pengguna secara sengaja maupun tidak disengaja mengirimkan data yang tidak sesuai constraint, yang dapat menyebabkan kerusakan data atau kebobolan.

## Mengapa `csrf_token` dibutuhkan

Tag `csrf_token` dalam template Django merupakan bagian dari sistem proteksi Django terhadap serangan *Cross Site Request Forgery* (CSRF). CSRF token berfungsi untuk memastikan bahwa pengguna memang mengakses website yang benar. Tanpa adanya `csrf_token`, penyerang bisa saja membuat website yang seolah menyerupai website asli dan memanfaatkan kredensial pengguna untuk membuat pengguna melakukan hal yang tidak diinginkan.

## Feedback Asdos

-

## Screenshot Postman

XML: <https://drive.google.com/file/d/11PDK46HPgUw6iGfzcFhNJ_faf4-kr5Ur/view>
XML *by ID*: <https://drive.google.com/file/d/1-Ab8z-JmT5ueWasiHxtpZNBPWR4JyK90/view>
JSON: <https://drive.google.com/file/d/1_II7N-dgsKAi1QxQBn_msp5GtgLMwPHo/view>
JSON *by ID*: <https://drive.google.com/file/d/1OwDZKNc8PigSeNX9fMCzcTPzfpJ7nJtt/view>

# Tugas 2

## Step-by-step checklist

- Pertama, saya membuat direktori bernama `tugas` yang bersebelahan dengan direktori `football-news` yang berisi proyek tutorial.
- Di dalam direktori `tugas`, saya membuat dan menyalakan *virtual environment* Python:
```
python3 -m venv env
. env/bin/activate
```
- Selanjutnya saya menyalin file `requirements.txt` pada proyek tutorial ke proyek tugas:
```
cp ../football-news/requirements.txt requirements.txt
```
- File `requirements.txt` berisi daftar modul Python yang akan saya perlukan untuk membuat proyek Django:
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
python-dotenv
```
- Saya meng-install semua modul Python tersebut dalam *virtual environment* saya:
```
pip install -r requirements.txt
```
- Setelah meng-install semua modul yang diperlukan, saya memulai proyek Django dengan nama `phutbolnius`:
```
python3 -m django startproject phutbolnius'
```
- Selanjutnya saya membuat aplikasi bernama `main`:
```
python3 manage.py startapp main
```
- Agar memastikan tidak ada error, saya menjalankan server pada laptop saya:
```
python3 manage.py runserver 8123
```
- Kemudian saya mengaksesnya dengan mengetik `localhost:8123` pada *web browser* saya. Untungnya tidak ada error yang ditampilkan.
- Namun, ternyata di terminal muncul peringatan serta anjuran agar saya melakukan migrasi database terlebih dahulu, jadi saya menjalankan perintah yang disebutkan di terminal:
```
python3 manage.py migrate
```
- Setelah itu, saya mulai mengerjakan halaman utama. Saya membuat direktori `templates` di folder aplikasi `main`, lalu di dalamnya saya membuat file `index.html` dengan isi sebagai berikut:
```
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <h1>Halo Dunia</h1>
</body>
</html>
```
- Kemudian saya mulai mengerjakan mekanisme routing agar pengguna dapat mengakses halaman utama.
  - Saya membuat fungsi `show_main_page` di file `views.py` pada aplikasi `main`. Fungsi ini bertugas mem-format file `index.html` ke dalam bentuk response HTTP.
  - Selanjutnya, saya membuat daftar pola URL yang akan di-cek di file `urls.py` aplikasi `main`. Saat ini satu-satunya anggotanya adalah root URL, yang akan memanggil fungsi `show_main_page` pada file `views.py`.
  - Terakhir, saya meng-include daftar pola URL pada file `urls.py` aplikasi `main` di file `urls.py` proyek.
- Saya kembali melakukan `runserver`, namun ternyata muncul error: <https://drive.google.com/file/d/1V7ombRweWjwVZoDyhrz4ryPhePNqlSwe/view>
- Setelah saya telusuri, ternyata masalahnya adalah saya belum menambahkan `main` ke dalam list `INSTALLED_APPS` di file proyek `settings.py`. Setelah saya tambahkan `main` ke dalam list `INSTALLED_APPS`, akhirnya halaman utama dapat ditampilkan.
- Setelah itu, saya menambahkan model `Product` di file `models.py`, lalu saya melakukan migrasi database agar model tersebut terekam oleh Django.
- Setelah sedikit mengubah halaman utama agar sesuai dengan requirement tugas, saya melakukan deployment ke PWS.
- Terakhir, saya menonaktifkan *virtual environment* Python:
```
deactivate
```

## Bagan alur *request* *client*

<https://drive.google.com/file/d/1AkQjLgdl9LWFaNF0YXXtmxelDPh8jlZY/view?usp=drive_link>

## Peran `settings.py`

Dalam proyek Django, `settings.py` sesuai namanya berfungsi untuk meng-konfigurasi proyek secara keseluruhan. Pengaturan yang tersedia antara lain:

## Cara kerja migrasi database di Django

Saat kita ingin melakukan migrasi database di Django, pertama kita perlu membuat daftar tindakan migrasi yang perlu dilakukan. Kita melakukannya dengan perintah berikut:
```
python3 manage.py makemigrations
```
Setelah daftar tersebut dibuat, kita dapat melaksanakannya dengan perintah berikut:
```
python3 manage.py migrate
```

## Alasan Django dijadikan permulaan pembelajaran pengembangan perangkat lunak

Menurut saya, alasan Django dijadikan permulaan pembelajaran pengembangan perangkat lunak adalah karena bahasa yang digunakan hanya satu, yaitu Python (selain bahasa-bahasa web), yang mana bahasa Python sangat mudah untuk dipelajari dan memang sudah dipelajari pada mata kuliah sebelumnya.
