import datetime
import locale

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from main.forms import ProductForm
from main.models import Product

locale.setlocale(locale.LC_ALL, "id_ID.UTF-8")

# Create your views here.

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

def view_product(request, id):

    product = get_object_or_404(Product, pk=id)

    print("Halo")
    seller_name = product.user.username or "Halo Dunia Football Shop"
    
    context = {
        'product': product,
        'seller_name': seller_name,
    }

    return render(request, "view_product.html", context)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def edit_product(request, id):

    product = get_object_or_404(Product, pk=id)
    if request.user.id != product.user.id:
        return HttpResponse(status=403)

    form = ProductForm(request.POST or None, instance=product)

    # Form submission
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main_page')

    # Form filling out
    context = {'form': form}
    return render(request, "edit_product.html", context)

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.user != product.user:
        return HttpResponse(status=403)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main_page'))

def show_xml(request):

    products = Product.objects.all()
    xml_data = serializers.serialize("xml", products)
    return HttpResponse(xml_data, content_type="application/xml")

def show_xml_by_id(request, product_id):

    try:
        product = Product.objects.get(pk=product_id)
        xml_data = serializers.serialize("xml", [product])
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json(request):

    products = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
        }
        for product in products
    ]

    return JsonResponse(data, safe=False)

def show_json_by_id(request, product_id):

    try:

        product = Product.objects.select_related('user').get(pk=id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
        }
        return JsonResponse(data)

    except Product.DoesNotExist:
        return JsonRepsonse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_main_page')

    context = { 'form': form }
    return render(request, 'register.html', context)

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

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main_page'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
@require_POST
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    thumbnail = request.POST.get("thumbnail")
    category = request.POST.get("category")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    product = Product(
        name=name,
        price=price,
        description=description,
        thumbnail=thumbnail,
        category=category,
        is_featured=is_featured,
        user=user
    )
    product.save()

    return HttpResponse(b"CREATED", status=201)
