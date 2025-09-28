from requests import get

pr = 'http://YPKN9q5sVocz4aMv:01306004290_country-bd_city-dhaka_session-ITIdDt_lifetime-15m_skipispstatic-1@geo.iproyal.com:11200'
# pr = 'socks5h://mariam:mariam1@103.137.161.128:9169'
proxies = None
proxies = dict(http=pr, https=pr)
# r = get('https://payment.ivacbd.com/', proxies=proxies)
r = get('https://ip.oxylabs.io/', proxies=proxies)
print(r.text)

