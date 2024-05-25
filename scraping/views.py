from typing import Any
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from .models import Vacancy
from .forms import FindForm, VForm
from django.contrib import messages


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


def v_detail(request, pk):
    # object_ = Vacancy.objects.get(pk=pk)
    object_ = get_object_or_404(Vacancy, pk=pk)
    context = {
        'object': object_,
    }
    return render(request, 'scraping/detail.html', context)


class VDetail(DetailView):
    queryset = Vacancy.objects.all()
    # model = VDetail
    template_name = 'scraping/detail.html'
    # context_object_name = ''


class VList(ListView):
    model = Vacancy
    template_name = 'scraping/detail.html'
    form = FindForm()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []

        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language

            qs = Vacancy.objects.filter(**_filter)
        return qs


class VCreate(CreateView):
    model = Vacancy
    fields = '__all__'
    form_class = VForm
    template_name = "scraping/create.html"
    success_url = reverse_lazy('home')


class VUpdate(UpdateView):
    model = Vacancy
    fields = '__all__'
    form_class = VForm
    template_name = "scraping/create.html"
    success_url = reverse_lazy('home')


class VDelete(DeleteView):
    model = Vacancy
    # template_name = "scraping/delete.html"
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, "Запись успешно удалена.")

        return self.post(request, *args, **kwargs)
