from django.urls import path
from .views import *

app_name = "songwrytrapp"

urlpatterns = [
    path('', writer_list, name='home'),
    path('writers/', writer_list, name='writers'),
]