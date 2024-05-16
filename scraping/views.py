from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()

    context = {
        "form": form,
    }
    return render(request, 'scraping/home.html', context)


def list_view(request):
    form = FindForm()
    city = request.GET.get("city")
    language = request.GET.get("language")
    page_obj = []
    context = {
        'city': city,
        'language': language,

        "form": form,
    }
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)

        paginator = Paginator(qs, 10)
        pages = request.GET.get('page')
        page_obj = paginator.get_page(pages)
    context["object_list"] = page_obj
    return render(request, 'scraping/list.html', context)
