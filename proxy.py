from mitmproxy import http
from mitmproxy.connection import Server
from mitmproxy.net.server_spec import ServerSpec
from time import sleep
import subprocess, atexit, socket, json, random

USER = 'd50ded41de92755b'
PASS = 'hduAyxiF'
HOST = 'res.proxy-seller.com'
PORT = random.randint(10000, 10049)


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


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
    PORT = get_free_port()
    p = subprocess.Popen(f'mitmdump -s "{__file__}" --listen-port {PORT} --upstream-auth {USER}:{PASS}'.split(
    ),  stderr=subprocess.STDOUT)
    atexit.register(p.kill)

    while 1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            if s.connect_ex(('127.0.0.1', PORT)) == 0: break
        sleep(1)
        print('Waiting for the server to be run')

    if wait:
        print('ProxyServer is running on port', PORT)
        p.wait()
    else:
        return PORT

if __name__ == '__main__':
    runProxyServer(1)

