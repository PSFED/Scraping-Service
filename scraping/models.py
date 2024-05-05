from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название города')
    slug = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Названия городов'
