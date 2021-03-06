from .home import home
from .auth.logout import logout_user
from .writers.list import writer_list
from .writers.form import writer_form, writer_edit_form
from .writers.details import writer_details
from .publishingcompanies.list import publishingcompany_list
from .publishingcompanies.form import publishingcompany_form, publishingcompany_edit_form
from .publishingcompanies.details import publishingcompany_details
from .compositions.list import composition_list
from .compositions.form import composition_form, composition_edit_form, composition_writer_form, composition_publishing_form, composition_recording_form, composition_recording_delete, composition_recording_edit_form, composition_publishing_remove, composition_writer_remove, composition_publishing_edit_form, composition_writer_edit_form
from .compositions.details import composition_details
from .auth.register import CustomUserCreationForm, register