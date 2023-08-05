### Vault8 Python lib

#### Installation

```
pip3 install vault8
```

#### Example
```python
import os
import sys
import vault8

pubkey = os.getenv('VAULT8_PUBLIC_KEY', '')
privkey = os.getenv('VAULT8_SECRET_KEY', '')
url = os.getenv('VAULT8_URL', 'https://vault8.io')

vault = vault8.Vault8(public_key=pubkey, secret_key=privkey, service_url=url)

# upload file from localhost
image = open('pypi.png', 'rb')
# or remote
# image = 'https://example.com/pypi.png'

uploaded = vault.upload_image(image)

if uploaded.get('status') == 'error':
    print(uploaded.get('response'))
    sys.exit(0)

uid = uploaded.get('image_uid')

print(vault.image_url(uid=uid, filters=[('resize_fill',1000,500), ('grayscale',)]))
```