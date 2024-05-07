from django.shortcuts import render
from .models import Vacancy


def home_view(request):
    qs = Vacancy.objects.all()
    context = {
        "object_list": qs,
    }
    return render(request, 'scraping/home.html', context)
