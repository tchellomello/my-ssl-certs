# my-ssl-certs
Simple based Django application to request and sign custom SSL certificates

![](https://github.com/tchellomello/my-ssl-certs/blob/master/my-ssl-certs.png)

## Docker
```bash
docker run -p 8000:8000 tchellomello/mysslcerts:latest
```

## Environment Variables

### CA_C
Define the default country for CA

### CA_ST
Define the default state for CA

### CA_L
Define the default city for CA

### CA_O
Define the default organization for CA

### CA_OU
Define the default organization unit for CA

### CA_EMAIL
Define the default email for CA

### CA_DAYS
Define the default expiration days for CA

### CERT_C
Define the default country for CERT

### CERT_ST
Define the default state for CERT

### CERT_L
Define the default city for CERT

### CERT_O
Define the default organization for CERT

### CERT_OU
Define the default organization unit for CERT

### CERT_EMAIL
Define the default email for CERT

### CERT_DAYS
Define the default expiration days for CERT

```bash
docker run -d -p 8000:8000 \
    -e CA_C='US' -e CA_ST='North Carolina' \
    -e CA_L='Raleigh' -e CA_O='IT' -e CA_OUT='DTI' \
    -e CA_EMAIL='me@example.com' -e CA_DAYS=365 \
    tchellomello/mysslcerts:latest
```
