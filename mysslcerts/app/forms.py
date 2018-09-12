from django import forms

class generate_ca_and_certificateForm(forms.Form):
    ca_common_name = forms.CharField(label='Common Name (CN)', max_length=50)
    ca_country = forms.CharField(label='Country (C)', max_length=2)
    ca_state = forms.CharField(label='State (ST)', max_length=30)
    ca_city = forms.CharField(label='City (L)', max_length=30)
    ca_organization = forms.CharField(label='Organization (O)', max_length=30)
    ca_organizational_unit = forms.CharField(label='Organizational Unit (OU)', max_length=30, required=False)
    ca_days = forms.IntegerField(label='Days to Expire', min_value=1)
    ca_email = forms.EmailField(label='Email')

    #certificate
    cert_common_name = forms.CharField(label='Common Name (CN)', max_length=50)
    cert_country = forms.CharField(label='Country (C)', max_length=2)
    cert_state = forms.CharField(label='State (ST)', max_length=30)
    cert_city = forms.CharField(label='City (L)', max_length=30)
    cert_organization = forms.CharField(label='Organization (O)', max_length=30)
    cert_organizational_unit = forms.CharField(label='Organizational Unit (OU)', max_length=30, required=False)
    cert_days = forms.IntegerField(label='Days to Expire', min_value=1)
    cert_email = forms.EmailField(label='Email')
    alt_names = forms.CharField(widget=forms.Textarea, label='Alternatives DNS Names', required=False)

class generate_certificate_from_uploaded_CAForm(forms.Form):
    #ca
    ca_certificate = forms.FileField()
    ca_key = forms.FileField()

    #certificate
    cert_common_name = forms.CharField(label='Common Name (CN)', max_length=50)
    cert_country = forms.CharField(label='Country (C)', max_length=2)
    cert_state = forms.CharField(label='State (ST)', max_length=30)
    cert_city = forms.CharField(label='City (L)', max_length=30)
    cert_organization = forms.CharField(label='Organization (O)', max_length=30)
    cert_organizational_unit = forms.CharField(label='Organizational Unit (OU)', max_length=30, required=False)
    cert_days = forms.IntegerField(label='Days to Expire', min_value=1)
    cert_email = forms.EmailField(label='Email')
    alt_names = forms.CharField(widget=forms.Textarea, label='Alternatives DNS Names', required=False)

