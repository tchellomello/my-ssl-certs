import os

# Certificate Authority default values
DEFAULT_CA_C=os.environ.get('CA_C', 'US')
DEFAULT_CA_ST=os.environ.get('CA_ST', 'North Carolina')
DEFAULT_CA_L=os.environ.get('CA_L', 'Raleigh')
DEFAULT_CA_O=os.environ.get('CA_O', 'Home')
DEFAULT_CA_OU=os.environ.get('CA_OU', '')
DEFAULT_CA_EMAIL=os.environ.get('CA_EMAIL', 'me@example.com')
DEFAULT_CA_DAYS=os.environ.get('CA_DAYS', '365')

# Certificate default values
DEFAULT_CERT_C=os.environ.get('CERT_C', 'US')
DEFAULT_CERT_ST=os.environ.get('CERT_ST', 'North Carolina')
DEFAULT_CERT_L=os.environ.get('CERT_L', 'Raleigh')
DEFAULT_CERT_O=os.environ.get('CERT_O', 'Home')
DEFAULT_CERT_OU=os.environ.get('CERT_OU', '')
DEFAULT_CERT_EMAIL=os.environ.get('CERT_EMAIL', 'me@example.com')
DEFAULT_CERT_DAYS=os.environ.get('CERT_DAYS', '365')
