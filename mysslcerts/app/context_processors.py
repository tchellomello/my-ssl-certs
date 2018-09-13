from django.conf import settings

def app_version(context):
    return {'APP_VERSION': settings.APP_VERSION}

