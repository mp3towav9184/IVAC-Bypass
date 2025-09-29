from DrissionPage import ChromiumPage, ChromiumOptions, errors
from proxy import runProxyServer
import time, traceback

PORT = runProxyServer()

with open('script.js') as f:
    SCRIPT = f.read()

print('[+] Bypass Server Running...')

opts = ChromiumOptions()
opts \
    .auto_port() \
    .set_argument('--start-maximized') \
    .set_argument('--ignore-certificate-errors') \
    .set_argument('--auto-open-devtools-for-tabs') \
    .set_proxy(f'http://127.0.0.1:{PORT}')

page = ChromiumPage(opts)

page.get('https://payment.ivacbd.com/')
# page.get('https://ip.oxylabs.io/')

while 1:
    try: page.run_js(SCRIPT)
    except (errors.PageDisconnectedError): break
    except Exception as err:
        # traceback.print_exc()
        # print(f'[-] ERROR ({type(err)}): {err}')
        pass
    time.sleep(2)



