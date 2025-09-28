from DrissionPage import ChromiumPage, ChromiumOptions
from proxy import runProxyServer

PORT = runProxyServer()

print('Server Running...')

opts = ChromiumOptions()
opts \
    .auto_port() \
    .set_argument('--start-maximized') \
    .set_argument('--ignore-certificate-errors') \
    .set_proxy(f'http://127.0.0.1:{PORT}') \

page = ChromiumPage(opts)

page.get('https://payment.ivacbd.com/')
# page.get('https://ip.oxylabs.io/')

input('Enter to exit')

