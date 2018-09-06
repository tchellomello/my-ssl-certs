from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from random import randint
from time import gmtime, mktime
from datetime import timedelta, datetime
from os.path import exists, join
import zipfile
from io import BytesIO

cert_dir = "/tmp"
CA_CERT_FILE = "CA_crt.pem"
CA_KEY_FILE = "CA_key.pem"
CERT_FILE = "cert_crt.pem"
KEY_FILE = "cert_key.pem"
CSR_FILE = "cert_csr.pem"

class CustomSat6Certs():

    def __init__(self, zip_filename=None):

        # define CA args
        self.ca_certificate = None
        self.ca_key = None

        if zip_filename and isinstance(zip_filename, str) and not zip_filename.endswith('zip'):
            self.zip_filename = zip_filename + '.zip'
        else:
            self.zip_filename = 'certificates.zip'

    def create_ca(self, ca_country="", ca_state="", ca_city="",
            ca_organization="", ca_organizational_unit="", ca_common_name="", ca_days=365, algo_hash="sha256"):

        #create key
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        #create a self-signed cert for CA use
        cert = crypto.X509()
        cert.get_subject().C = ca_country
        cert.get_subject().ST = ca_state
        cert.get_subject().L = ca_city
        cert.get_subject().O = ca_organization
        cert.get_subject().CN = ca_common_name

        #add CA extension CA:True
        cert.add_extensions([
            OpenSSL.crypto.X509Extension(
                "basicConstraints", True, "CA:TRUE, pathlen:0"),
            OpenSSL.crypto.X509Extension(
                "keyUsage", True, "keyCertSign, cRLSign"),
            OpenSSL.crypto.X509Extension(
                "subjectKeyIdentifier", False, "hash", subject=cert),
        ])
        cert.add_extensions([
            OpenSSL.crypto.X509Extension(
                "authorityKeyIdentifier", False, "keyid:always",issuer=cert)
        ])

        #optional
        if ca_organizational_unit:
            cert.get_subject().OU = ca_organizational_unit

        cert.set_serial_number(randint(1,99))
        cert.gmtime_adj_notBefore(0)
        #notAfter must be in seconds
        cert.gmtime_adj_notAfter(int(((datetime.now()+timedelta(days=ca_days))-(datetime.now())).total_seconds()))
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, algo_hash)

        #open(join(cert_dir, CA_CERT_FILE), "wt").write(
        #        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        #open(join(cert_dir, CA_KEY_FILE), "wt").write(
        #        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

        self.ca_certificate = cert
        self.ca_key = k
        return True

    def load_ca_certificate(self, ca_certificate=None):
        '''load the CA certificate'''

        ## type will be str when request.FILES is uploaded to memory
        try:
            self.ca_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, ca_certificate)
            return True
        except:
            self.ca_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, open(ca_certificate).read())
            return True
        return False

    def load_ca_key(self, ca_key=None):
        '''load the CA key'''

        ## type will be str when request.FILES is uploaded to memory
        try:
            self.ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key)
            return True
        except:
            self.ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(ca_key).read())
            return True
        return False

    def load_certificate(self, certificate=None):
        '''load SSL certificate'''

        ## type will be str when request.FILES is uploaded to memory
        try:
            c = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)
            return c
        except:
            c = crypto.load_certificate(crypto.FILETYPE_PEM, open(certificate).read())
            return c
        return False

    def verify_certificate_chain(self, ca_certificate=None, trusted_certificate=None):
        '''verify SSL trust chain'''
        #TODO
        pass

    def create_cert(self, cert_country="", cert_state="", cert_city="",
            cert_organization="", cert_organizational_unit="", cert_common_name="", cert_days=365, algo_hash="sha256"):

        if self.ca_certificate == None or self.ca_key == None:
            return "Missing CA certificate and key"

        #create CSR
        req = crypto.X509Req()
        req.get_subject().C = cert_country
        req.get_subject().ST = cert_state
        req.get_subject().L = cert_city
        req.get_subject().O = cert_organization
        req.get_subject().CN = cert_common_name

        #optional
        if cert_organizational_unit:
            req.get_subject().OU = cert_organizational_unit

        #create key
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        #create csr PEM
        req.set_pubkey(k)
        req.sign(k, algo_hash)
        self.certificate_csr = req

        #sign CSR using CA
        cert = crypto.X509()
        cert.set_serial_number(randint(1,99))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(int(((datetime.now()+timedelta(days=cert_days))-(datetime.now())).total_seconds()))
        cert.set_issuer(self.ca_certificate.get_subject())
        cert.set_subject(req.get_subject())
        cert.set_pubkey(req.get_pubkey())
        cert.sign(self.ca_key, algo_hash)

        self.certificate_key = k
        self.certificate_crt = cert

        #open(join(cert_dir, CERT_FILE), "wt").write(
        #        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        #open(join(cert_dir, KEY_FILE), "wt").write(
        #        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

        return True

    def get_zip(self):
        zipIO = BytesIO()
        with zipfile.ZipFile(zipIO, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(CA_CERT_FILE, crypto.dump_certificate(crypto.FILETYPE_PEM, self.ca_certificate))
            zf.writestr(CA_KEY_FILE, crypto.dump_privatekey(crypto.FILETYPE_PEM, self.ca_key))
            zf.writestr(KEY_FILE, crypto.dump_privatekey(crypto.FILETYPE_PEM, self.certificate_key))
            zf.writestr(CERT_FILE, crypto.dump_certificate(crypto.FILETYPE_PEM, self.certificate_crt))
            zf.writestr(CSR_FILE, crypto.dump_certificate_request(crypto.FILETYPE_PEM, self.certificate_csr))
            zf.close()
        zipIO.seek(0)
        return zipIO.read()
