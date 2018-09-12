from django.shortcuts import render_to_response, redirect, render, HttpResponse
from app.forms import *
from app.models import Question, Tag, Topic
from app.libs import CustomSat6Certs
from app.vars import *

def cheatsheet(request):
    questions = Question.objects.filter(enabled=True).order_by('sort_order')
    return render(request, 'app/cheat_sheet.html', locals())

def generate_ca_and_certificate(request):
    if request.method == 'POST':
        form = generate_ca_and_certificateForm(request.POST)
        if form.is_valid():

            ca_common_name = form.cleaned_data['ca_common_name']
            ca_country = form.cleaned_data['ca_country']
            ca_state = form.cleaned_data['ca_state']
            ca_city = form.cleaned_data['ca_city']
            ca_organization = form.cleaned_data['ca_organization']
            ca_organizational_unit = form.cleaned_data['ca_organizational_unit']
            ca_days = form.cleaned_data['ca_days']
            ca_email = form.cleaned_data['ca_email']

            cert_common_name = form.cleaned_data['cert_common_name']
            cert_country = form.cleaned_data['cert_country']
            cert_state = form.cleaned_data['cert_state']
            cert_city = form.cleaned_data['cert_city']
            cert_organization = form.cleaned_data['cert_organization']
            cert_organizational_unit = form.cleaned_data['cert_organizational_unit']
            cert_days = form.cleaned_data['cert_days']
            cert_email = form.cleaned_data['cert_email']
            alt_names_list = form.cleaned_data['alt_names']

            obj = CustomSat6Certs(zip_filename=cert_common_name)

            #create CA
            obj.create_ca(ca_country=ca_country, ca_state=ca_state, ca_city=ca_city,
                    ca_organization=ca_organization, ca_organizational_unit=ca_organizational_unit,
                    ca_common_name=ca_common_name, ca_days=ca_days)

            #create certificate
            obj.create_cert(cert_country=cert_country, cert_state=cert_state, cert_city=cert_city,
                    cert_organization=cert_organization, cert_organizational_unit=cert_organizational_unit,
                    cert_common_name=cert_common_name, cert_days=cert_days,
                    alt_names_list=alt_names_list)

            zipfile = obj.get_zip()
            response = HttpResponse(zipfile, content_type='application/x-zip-compressed')
            response['Content-Disposition'] = 'attachment; filename=%s' % obj.zip_filename
            return response
    else:
        form = generate_ca_and_certificateForm(initial={
                                        'ca_country' : DEFAULT_CA_C,
                                        'ca_state'   : DEFAULT_CA_ST,
                                        'ca_city'    : DEFAULT_CA_L,
                                        'ca_organization'  : DEFAULT_CA_O,
                                        'ca_organizational_unit' : DEFAULT_CA_OU,
                                        'ca_days'    : DEFAULT_CA_DAYS,
                                        'ca_email': DEFAULT_CA_EMAIL,

                                        'cert_country' : DEFAULT_CERT_C,
                                        'cert_state'   : DEFAULT_CERT_ST,
                                        'cert_city'    : DEFAULT_CERT_L,
                                        'cert_organization'  : DEFAULT_CERT_O,
                                        'cert_organizational_unit' : DEFAULT_CERT_OU,
                                        'cert_email': DEFAULT_CERT_EMAIL,
                                        'cert_days'    : DEFAULT_CERT_DAYS,
                                        })
    return render(request, 'app/generate_ca_and_certificate.html', locals())

def generate_certificate_from_uploaded_CA(request):
    if request.method == 'POST':
        form = generate_certificate_from_uploaded_CAForm(request.POST, request.FILES)
        if form.is_valid():

            #load CA
            ca_certificate = request.FILES['ca_certificate'].read()
            ca_key = request.FILES['ca_key'].read()

            cert_common_name = form.cleaned_data['cert_common_name']
            cert_country = form.cleaned_data['cert_country']
            cert_state = form.cleaned_data['cert_state']
            cert_city = form.cleaned_data['cert_city']
            cert_organization = form.cleaned_data['cert_organization']
            cert_organizational_unit = form.cleaned_data['cert_organizational_unit']
            cert_days = form.cleaned_data['cert_days']
            cert_email = form.cleaned_data['cert_email']
            alt_names_list = form.cleaned_data['alt_names']

            obj = CustomSat6Certs(zip_filename=cert_common_name)

            #load CA
            obj.load_ca_certificate(ca_certificate)
            obj.load_ca_key(ca_key)

            #create certificate
            obj.create_cert(cert_country=cert_country, cert_state=cert_state, cert_city=cert_city,
                    cert_organization=cert_organization, cert_organizational_unit=cert_organizational_unit,
                    cert_common_name=cert_common_name, cert_days=cert_days,
                    alt_names_list=alt_names_list)

            zipfile = obj.get_zip()
            response = HttpResponse(zipfile, content_type='application/x-zip-compressed')
            response['Content-Disposition'] = 'attachment; filename=%s' % obj.zip_filename
            return response
    else:
        form = generate_certificate_from_uploaded_CAForm(initial={
                                        'cert_country' : DEFAULT_CERT_C,
                                        'cert_state'   : DEFAULT_CERT_ST,
                                        'cert_city'    : DEFAULT_CERT_L,
                                        'cert_organization'  : DEFAULT_CERT_O,
                                        'cert_organizational_unit' : DEFAULT_CERT_OU,
                                        'cert_days'    : DEFAULT_CERT_DAYS,
                                        'cert_email'   : DEFAULT_CERT_EMAIL,
                                        })
    return render(request, 'app/generate_certificate_from_uploaded_CA.html', locals())

def verify_certificate(request):
    #TODO
    return redirect(generate_ca_and_certificate)
