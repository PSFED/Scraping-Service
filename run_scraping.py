from django.db import DatabaseError
from scraping.models import Vacancy, City, Language, Error
from scraping.parsers import *
import django
import codecs
import os
import sys
django.setup()
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'


parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (djinni, 'djinni'),
    (rabota, 'rabota')
)

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except:
        pass
if errors:
    er = Error(data=errors).save()

# h = codecs.opne('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
