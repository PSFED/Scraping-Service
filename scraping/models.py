from django.db import models
import jsonfield
from .utils import from_cyrillic_to_eng


def defaults_urls():
    return {'work': '', 'rabota': '', 'djinni': '', 'dou': ''}


class City(models.Model):
    name = models.CharField(
        max_length=50, verbose_name='Название города', unique=True)
    slug = models.SlugField(blank=True, max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Названия городов'


class Language(models.Model):
    name = models.CharField(
        max_length=50, verbose_name='Язык программирования', unique=True)
    slug = models.SlugField(blank=True, max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(
        max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(
        max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name="Описание вакансии")
    city = models.ForeignKey(
        "City", verbose_name="Город", on_delete=models.CASCADE)
    language = models.ForeignKey(
        "Language", verbose_name="Язык программирования", on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    city = models.ForeignKey(
        "City", verbose_name="Город", on_delete=models.CASCADE)
    language = models.ForeignKey(
        "Language", verbose_name="Язык программирования", on_delete=models.CASCADE)
    url_data = jsonfield.JSONField(default=defaults_urls)

    class Meta:
        unique_together = ('city', 'language')
