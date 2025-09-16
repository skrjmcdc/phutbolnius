from django.shortcuts import render, redirect
from main.forms import ProductForm

# Create your views here.

def show_main_page(request):
    context = {
        'name'  : 'Muhammad Ibaadi Ilmi',
        'class' : 'PBP A',
    }
    return render(request, "index.html", context)

def add_product(request):

    form = ProductForm(request.POST or None)

    # Form submission
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    # Form filling out
    context = {'form': form}
    return render(request, "add_product.html", context)
