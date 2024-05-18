from django.urls import path
from accounts.views import login_view, logout_view, registration_view, update_view, delete_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('update/', update_view, name='update'),
    path('delete/', delete_view, name='delete'),
]
