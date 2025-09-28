from requests import get

pr = 'http://YPKN9q5sVocz4aMv:01306004290_country-bd_session-ITIdDt_lifetime-15m_skipispstatic-1@geo.iproyal.com:11200'
# pr = 'socks5h://mariam:mariam1@103.137.161.128:9169'
proxies = None
# proxies = dict(http=pr, https=pr)
# r = get('https://payment.ivacbd.com/', proxies=proxies)
# print(r.text)
r = get('https://abacus.jasoncameron.dev/get/ivac/bypass', proxies=proxies)
print(r.json().get('value'))

from requests import get
import os

if get('https://abacus.jasoncameron.dev/get/ivac/bypass').json().get('value') > 10:
    os._exit(1)

    
