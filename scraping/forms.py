from django import forms
from .models import City, Language, Vacancy


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')


class VForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')
    url = forms.CharField(widget=forms.URLInput(
        attrs={'class': 'form-control'}), label='URL')
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label='Заголовок вакансии')
    company = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), label='Компания')
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), label='Описание вакансии')

    class Meta:
        model = Vacancy
        fields = '__all__'
