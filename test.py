from requests import get

pr = 'socks5h://mariam:mariam1@103.137.161.128:9169'
proxies = None
proxies = dict(http=pr, https=pr)
r = get('https://payment.ivacbd.com/', proxies=proxies)
print(r.text)
