from django.urls import include, path
from .views import *

app_name = "songwrytrapp"

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('writers/', writer_list, name='writers'),
    path('writer/form', writer_form, name='writer_form'),
    path('writers/<int:writer_id>/form/', writer_edit_form, name='writer_edit_form'),
    path('writers/<int:writer_id>/', writer_details, name='writer'),
    path('publishingcompanies/', publishingcompany_list, name='publishingcompanies'),
    path('publishingcompany/form', publishingcompany_form, name='publishingcompany_form'),
    path('publishingcompanies/<int:publishingcompany_id>/form/', publishingcompany_edit_form, name='publishingcompany_edit_form'),
    path('publishingcompanies/<int:publishingcompany_id>/', publishingcompany_details, name='publishingcompany'),
    path('compositions/', composition_list, name='compositions'),
    path('composition/form', composition_form, name='composition_form'),
    path('compositions/<int:composition_id>/form/', composition_edit_form, name='composition_edit_form'),
    path('compositions/<int:composition_id>/', composition_details, name='composition'),
    path('compositions/<int:composition_id>/attachwriter/', composition_writer_form, name='composition_writer_form'),
    path('compositions/<int:composition_id>/attachpublisher/', composition_publishing_form, name='composition_publishing_form'),
    # path('compositions/<int:composition_id>/recording/form/', composition_recording_form, name='composition_recording_form'),
    # path('compositions/<int:composition_id>/recordings/<int:recording_id>/form/', composition_recording_edit_form, name='composition_recording_edit_form'),
]