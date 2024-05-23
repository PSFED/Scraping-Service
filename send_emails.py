from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from scraping.models import Vacancy, Error, Url
from scraping_service.settings.local_settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
import django
import datetime
import os
import sys
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
ADMIN_USER = EMAIL_HOST_USER

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

django.setup()

today = datetime.date.today()
empty = '<h2>К сожалению, на сегодня по Вашим предпочтениям данных нет.</h2>'
subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий за {today}"
from_email = EMAIL_HOST_USER

User = get_user_model
qs = User.objects.filter(send_email=True).values('city', 'language', 'mail')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['mail'])
if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    # for i in qs:
    #     vacancies.setdefault((i['city_id'], i['language_id']), [])
    #     vacancies[(i['city_id'], i['language_id'])].append(i)
    # for keys, emails in users_dct.items():
    #     rows = vacancies.get(keys, [])
    #     html = ''
    #     for row in rows:
    #         html += f'<h2><a href="{row["url"]}">{row["title"]}</a></h2>'
    #         html += f'<p>"{row["description"]}"</p>'
    #         html += f'<p>"{row["company"]}"</p><br><hr>'
    #     _html = html if html else empty
    #     for email in emails:
    #         to = email
    #         msg = EmailMultiAlternatives(
    #             subject, text_content, from_email, [to])
    #         msg.attach_alternative(_html, "text/html")
    #         msg.send()
qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></p><br>'
    subject = f"Ошибки скрапинга {today}"
    text_content = f"Ошибки скрапинга {today}"
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
        for i in data:
            _html += f'<p>Город: {i["title"]}, Специальность: {
                i["language"]}, Е-мейл: {i["email"]}</p><br>'
        subject = f"Пожелания пользователей {today}"
        text_content = f"Пожелания пользователей {today}"

qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            urls_err += f'''<p>Для города: {keys[0]
                                            } и ЯП: {keys[1]} отсутствуют урлы</p><br>'''
if urls_err:
    subject += 'Отсутствующие урлы'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()


msg = MIMEMultipart('alternative')
msg['Subject'] = 'Список вакансий за {}.'.format(today)
msg['From'] = EMAIL_HOST_USER
mail = smtplib.SMTP()
mail.connect(EMAIL_HOST, 25)
mail.ehlo()
mail.starttls()
mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

html_m = "<h1>Hui</h1>"
part = MIMEText(html_m, 'html')
msg.attach(part)
mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
mail.quit()
