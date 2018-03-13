from django.urls import re_path
from app.views import *

urlpatterns = [
    re_path(r'^$', generate_ca_and_certificate, name='generate_ca_and_certificate'),
    re_path(r'^cheat_sheet/$', cheatsheet, name='cheatsheet'),
    re_path(r'^verify/$', verify_certificate, name='verify_certificate'),
    re_path(r'^sign_with_external_CA/$', generate_certificate_from_uploaded_CA, name='generate_certificate_from_uploaded_CA'),
]
