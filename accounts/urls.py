from django.urls import path, include
from accounts.views import login


urlpatterns = [
    path('login/', login, name='login'),
]