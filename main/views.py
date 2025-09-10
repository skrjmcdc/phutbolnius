from django.shortcuts import render

# Create your views here.

def show_main_page(request):
    context = {
        'name'  : 'Muhammad Ibaadi Ilmi',
        'class' : 'PBP A',
    }
    return render(request, "index.html", context)
