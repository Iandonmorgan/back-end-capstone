from django.urls import include, path
from .views import *

app_name = "songwrytrapp"

urlpatterns = [
    path('', home, name='home'),
    path('writers/', writer_list, name='writers'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('writer/form', writer_form, name='writer_form'),
    path('writers/<int:writer_id>/form/', writer_edit_form, name='writer_edit_form'),
    path('writers/<int:writer_id>/', writer_details, name='writer'),
]