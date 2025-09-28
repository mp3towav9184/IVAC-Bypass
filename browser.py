from DrissionPage import ChromiumPage, ChromiumOptions
from proxy import runProxyServer
import time, traceback

PORT = runProxyServer()

print('[+] Bypass Server Running...')

opts = ChromiumOptions()
opts \
    .auto_port() \
    .set_argument('--start-maximized') \
    .set_argument('--ignore-certificate-errors') \
    .set_proxy(f'http://127.0.0.1:{PORT}')

page = ChromiumPage(opts)

page.get('https://payment.ivacbd.com/')
# page.get('https://ip.oxylabs.io/')

while 1:
    try: page.run_js("console.log('PING: Bypass Server')")
    except Exception as err:
        # traceback.print_exc()
        print(f'[-] QUITTING BECAUSE OF ERROR: {err}')
        break
    time.sleep(1)



